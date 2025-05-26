import os, sys, types

# ENV
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
sys.modules["httpx"] = types.SimpleNamespace(AsyncClient=lambda *a, **k: None)
sys.modules["redis"] = types.SimpleNamespace(Redis=lambda *a, **k: None)
sys.modules["rq"]    = types.SimpleNamespace(Queue=lambda *a, **k: None)
sys.modules["minio"] = types.SimpleNamespace(
    Minio=lambda *a, **k: types.SimpleNamespace(
        bucket_exists=lambda b: True,
        make_bucket=lambda b: None,
        put_object=lambda *a, **k: None
    ),
    S3Error=Exception
)

import analysis.app.tasks as tasks_mod  # noqa:E402

def test_tasks_api_presence():
    assert callable(tasks_mod.enqueue)
    assert callable(tasks_mod.analyze_file)
