import os
import sys
import types
import pytest

sys.modules["minio"] = types.SimpleNamespace(
    Minio=lambda *a, **k: types.SimpleNamespace(
        bucket_exists=lambda b: True,
        make_bucket=lambda b: None,
        put_object=lambda *a, **k: None,
        get_object=lambda *a, **k: types.SimpleNamespace(stream=lambda size: iter([b""])),
    ),
    S3Error=Exception
)

import storing.app.s3 as s3_mod  # noqa: E402

@pytest.mark.asyncio
async def test_ensure_bucket_and_client():
    await s3_mod.ensure_bucket()
    cli = s3_mod.client
    assert hasattr(cli, "bucket_exists")
    assert hasattr(cli, "make_bucket")
