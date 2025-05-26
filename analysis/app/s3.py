import os
from io import BytesIO
from minio import Minio

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
BUCKET = os.getenv("MINIO_BUCKET", "analysis")

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)

if not client.bucket_exists(BUCKET):
    client.make_bucket(BUCKET)

def upload_file(key: str, data: bytes, content_type: str = "application/octet-stream") -> None:
    client.put_object(
        BUCKET,
        key,
        BytesIO(data),
        length=len(data),
        content_type=content_type,
    )

def download_file(key: str) -> bytes:
    obj = client.get_object(BUCKET, key)
    try:
        return obj.read()
    finally:
        obj.close()
        obj.release_conn()