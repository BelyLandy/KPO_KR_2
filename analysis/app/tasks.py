# analysis/app/tasks.py
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io

import os, re, uuid, asyncio
import httpx
from redis import Redis
from rq import Queue
from sqlalchemy import select

from .db import async_session
from .models import AnalysisResult
from .s3 import upload_file

REDIS_HOST   = os.getenv("REDIS_HOST", "redis")
STORING_URL  = os.getenv("STORING_URL", "http://storing-service:8000")

redis_conn = Redis(host=REDIS_HOST, port=6379, db=0)
queue      = Queue("analysis", connection=redis_conn)

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
async def _fetch_file_text(file_id: int) -> str:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{STORING_URL}/files/{file_id}")
        r.raise_for_status()
        return r.text

def _stats(txt: str) -> tuple[int, int, int]:
    paragraphs = len([p for p in txt.splitlines() if p.strip()])
    words      = len(re.findall(r"\b\w+\b", txt, flags=re.UNICODE))
    characters = len(txt)
    return paragraphs, words, characters

async def _generate_wordcloud(txt: str) -> bytes | None:
    try:
        wc = WordCloud(width=500, height=500, background_color="white").generate(txt)
        buf = io.BytesIO()
        plt.figure(figsize=(5, 5), dpi=100)
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
        plt.close()
        buf.seek(0)
        return buf.read()
    except Exception as exc:
        print("local wordcloud failed:", exc)
        return None

def enqueue(file_id: int):
    queue.enqueue("app.tasks.analyze_file", file_id)

def analyze_file(file_id: int):
    asyncio.run(_async_analyze(file_id))

async def _async_analyze(file_id: int):
    async with async_session() as session:
        if await session.scalar(select(AnalysisResult).where(AnalysisResult.file_id == file_id)):
            return

    txt = await _fetch_file_text(file_id)
    paragraphs, words, characters = _stats(txt)
    wc_location: str | None = None

    png = await _generate_wordcloud(txt)
    if png:
        key = f"{uuid.uuid4().hex}_wordcloud.png"
        upload_file(key, png, "image/png")
        wc_location = key

    async with async_session() as session:
        ar = AnalysisResult(
            file_id=file_id,
            paragraphs=paragraphs,
            words=words,
            characters=characters,
            wordcloud_location=wc_location,
        )
        session.add(ar)
        await session.commit()
