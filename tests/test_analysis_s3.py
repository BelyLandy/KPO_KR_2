import sys, types
sys.modules["minio"] = types.SimpleNamespace(
    Minio=lambda *a, **k: types.SimpleNamespace(
        bucket_exists=lambda b: True,
        make_bucket=lambda b: None,
        put_object=lambda *a, **k: None,
        get_object=lambda **k: types.SimpleNamespace(read=lambda: b""),
    ),
    S3Error=Exception
)

import analysis.app.s3 as s3_mod  # noqa: E402

def test_analysis_s3_api():
    assert hasattr(s3_mod, "upload_file")
    assert hasattr(s3_mod, "download_file")
    assert callable(s3_mod.upload_file)
    assert callable(s3_mod.download_file)
