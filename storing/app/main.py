import io
import hashlib
from pathlib import Path

import anyio
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .db import async_session, engine, Base
from .models import File
from .s3 import client as s3, BUCKET, ensure_bucket
from .schemas import FileUploadResponse, FileOut

app = FastAPI(title="File Storing Service", version="1.0.5", openapi_version="3.0.3")

@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await ensure_bucket()

async def _read_and_hash(file: UploadFile) -> tuple[bytes, str]:
    data = await file.read()
    digest = hashlib.sha256(data).hexdigest()
    return data, digest


async def _put_object(location: str, data: bytes, content_type: str) -> None:
    size = len(data)

    def _inner():
        s3.put_object(
            bucket_name=BUCKET,
            object_name=location,
            data=io.BytesIO(data),
            length=size,
            content_type=content_type,
        )

    await anyio.to_thread.run_sync(_inner)

@app.post("/files", response_model=FileUploadResponse, status_code=201)
async def upload(file: UploadFile):
    data, digest = await _read_and_hash(file)
    size = len(data)
    filename = Path(file.filename).name
    location = f"{digest}_{filename}"

    async with async_session() as session:  # type: AsyncSession
        existing: File | None = await session.scalar(
            select(File).where(File.hash == digest)
        )
        if existing:
            return FileUploadResponse(
                id=existing.id,
                is_duplicate=True,
                name=existing.name,
                size=existing.size,
                location=existing.location,
            )

        try:
            await _put_object(
                location,
                data,
                file.content_type or "application/octet-stream",
            )
        except Exception as exc:
            raise HTTPException(500, f"Failed to upload to S3: {exc}")

        try:
            meta = File(
                name=filename, hash=digest, location=location, size=size
            )
            session.add(meta)
            await session.commit()
            await session.refresh(meta)
        except IntegrityError:
            await session.rollback()
            return FileUploadResponse(
                id=await session.scalar(
                    select(File.id).where(File.hash == digest)
                ),
                is_duplicate=True,
                name=filename,
                size=size,
                location=location,
            )

        return FileUploadResponse(
            id=meta.id,
            is_duplicate=False,
            name=meta.name,
            size=meta.size,
            location=meta.location,
        )

@app.get("/files/{file_id}", response_model=FileOut)
async def download(file_id: int):
    async with async_session() as session:
        meta: File | None = await session.get(File, file_id)
        if not meta:
            raise HTTPException(404, "File not found")

    obj = s3.get_object(bucket_name=BUCKET, object_name=meta.location)
    return StreamingResponse(
        obj.stream(64 * 1024),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{meta.name}"',
            "Content-Length": str(meta.size),
        },
    )
