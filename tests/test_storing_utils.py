import io
import sys, os, types
import pytest
from fastapi import UploadFile

# stub multipart so FastAPI.UploadFile can parse content-type
sys.modules["multipart"] = types.SimpleNamespace()

from storing.app.main import _read_and_hash  # noqa: E402

@pytest.mark.asyncio
async def test__read_and_hash_simple(tmp_path):
    data = b"hello world"
    fobj = io.BytesIO(data)
    upload = UploadFile(filename="hello.txt", file=fobj)
    buf, digest = await _read_and_hash(upload)
    assert isinstance(buf, bytes)
    import hashlib
    assert digest == hashlib.sha256(data).hexdigest()
    assert buf == data
