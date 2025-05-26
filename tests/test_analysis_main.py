import os, sys, types
from fastapi import FastAPI

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

sys.modules["wordcloud"] = types.SimpleNamespace(WordCloud=lambda *a, **k: None)
dummy_pyplot = types.SimpleNamespace(
    figure=lambda *a, **k: None,
    imshow=lambda *a, **k: None,
    axis=lambda *a, **k: None,
    savefig=lambda *a, **k: None,
    close=lambda *a, **k: None,
)
sys.modules["matplotlib"] = types.SimpleNamespace(pyplot=dummy_pyplot)
sys.modules["matplotlib.pyplot"] = dummy_pyplot
sys.modules["redis"] = types.SimpleNamespace(Redis=lambda *a, **k: None)
sys.modules["rq"]    = types.SimpleNamespace(Queue=lambda *a, **k: None)
sys.modules["minio"] = types.SimpleNamespace(
    Minio=lambda *a, **k: types.SimpleNamespace(
        bucket_exists=lambda b: True,
        make_bucket=lambda b: None,
        put_object=lambda *a, **k: None,
        get_object=lambda **k: types.SimpleNamespace(read=lambda: b""),
    ),
    S3Error=Exception
)

import analysis.app.main as an_mod  # noqa:E402

def test_analysis_app_defined():
    assert isinstance(an_mod.app, FastAPI)
    assert hasattr(an_mod, "trigger_analysis")
    assert hasattr(an_mod, "get_analysis")
    assert hasattr(an_mod, "get_wordcloud")
