import sys, types
import pytest

sys.modules["minio"] = types.SimpleNamespace(
    Minio=lambda *a, **k: types.SimpleNamespace(
        bucket_exists=lambda b: False,
        make_bucket=lambda b: None,
        put_object=lambda *a, **k: None,
        get_object=lambda **k: types.SimpleNamespace(stream=lambda _: iter([b""]))
    ),
    S3Error=Exception
)

import storing.app.s3 as s3_mod  # noqa: E402

@pytest.mark.asyncio
async def test_storing_s3_helpers_exist():
    assert hasattr(s3_mod, "client")
    assert hasattr(s3_mod, "ensure_bucket")
    await s3_mod.ensure_bucket()
