from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from sqlalchemy import select

from .db import engine, Base, async_session
from .models import AnalysisResult
from .schemas import AnalysisResponse
from .tasks import enqueue
from .s3 import download_file

app = FastAPI(title="File Analysis Service", version="0.1.0", openapi_version="3.0.3")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/files/{file_id}", status_code=202)
async def trigger_analysis(file_id: int):
    async with async_session() as session:
        res = await session.execute(select(AnalysisResult).where(AnalysisResult.file_id == file_id))
        if res.scalar_one_or_none():
            return {"detail": "already analyzed", "ready": True}
    enqueue(file_id)
    return {"detail": "analysis scheduled", "ready": False}

@app.get("/files/{file_id}", response_model=AnalysisResponse)
async def get_analysis(file_id: int):
    async with async_session() as session:
        res = await session.execute(select(AnalysisResult).where(AnalysisResult.file_id == file_id))
        ar = res.scalar_one_or_none()
        if not ar:
            return AnalysisResponse(ready=False)
        return AnalysisResponse(
            ready=True,
            paragraphs=ar.paragraphs,
            words=ar.words,
            characters=ar.characters,
            wordcloud_location=ar.wordcloud_location,
        )

@app.get("/wordcloud/{key}")
async def get_wordcloud(key: str):
    try:
        data = download_file(key)
    except Exception:
        raise HTTPException(status_code=404, detail="Wordcloud not found")
    return Response(content=data, media_type="image/png")