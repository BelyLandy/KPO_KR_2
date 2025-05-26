import sys, types
from fastapi import FastAPI

sys.modules["minio"] = types.SimpleNamespace(
    Minio=lambda *a, **k: types.SimpleNamespace(
        bucket_exists=lambda b: True,
        make_bucket=lambda b: None,
        put_object=lambda *a, **k: None,
        get_object=lambda **k: types.SimpleNamespace(stream=lambda _ : iter([b""])),
    ),
    S3Error=Exception
)

import storing.app.main as st_mod  # noqa:E402

def test_storing_app_defined():
    assert isinstance(st_mod.app, FastAPI)
    assert hasattr(st_mod, "upload")
    assert hasattr(st_mod, "download")
