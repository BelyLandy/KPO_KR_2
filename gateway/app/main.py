import os
from typing import Dict, Any

import httpx
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import Response, StreamingResponse

STORING_URL = os.getenv("STORING_URL", "http://storing-service:8000")
ANALYSIS_URL = os.getenv("ANALYSIS_URL", "http://analysis-service:8000")

app = FastAPI(title="API Gateway", version="0.1.0", openapi_version="3.0.3")


async def _proxy_json(method: str, url: str, **kwargs) -> Response:
    async with httpx.AsyncClient() as client:
        resp = await client.request(method, url, **kwargs)
    return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get("content-type"))

@app.post("/files")
async def upload_file(file: UploadFile):
    data = await file.read()
    files = {"file": (file.filename, data, file.content_type or "application/octet-stream")}
    return await _proxy_json("POST", f"{STORING_URL}/files", files=files)


@app.get("/files/{file_id}")
async def get_file(file_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{STORING_URL}/files/{file_id}", timeout=None)
    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="File not found")
    return StreamingResponse(resp.aiter_bytes(), media_type=resp.headers.get("content-type"), headers={
        k: v for k, v in resp.headers.items() if k.lower().startswith("content-disposition")
    })

@app.post("/analysis/{file_id}")
async def trigger_analysis(file_id: int):
    return await _proxy_json("POST", f"{ANALYSIS_URL}/files/{file_id}")

@app.get("/analysis/{file_id}")
async def get_analysis(file_id: int):
    return await _proxy_json("GET", f"{ANALYSIS_URL}/files/{file_id}")

@app.get("/wordcloud/{key}")
async def get_wordcloud(key: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{ANALYSIS_URL}/wordcloud/{key}")
    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Wordcloud not found")
    return StreamingResponse(resp.aiter_bytes(), media_type="image/png")