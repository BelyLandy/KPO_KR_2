import sys, os, types
import pytest

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

sys.modules["wordcloud"] = types.SimpleNamespace(WordCloud=lambda *a, **k: None)
sys.modules["matplotlib"] = types.SimpleNamespace(pyplot=types.SimpleNamespace(
    figure=lambda *a, **k: None, imshow=lambda *a, **k: None,
    axis=lambda *a, **k: None, savefig=lambda *a, **k: None,
    close=lambda *a, **k: None
))
sys.modules["matplotlib.pyplot"] = sys.modules["matplotlib"].pyplot
sys.modules["httpx"] = types.SimpleNamespace(AsyncClient=lambda *a, **k: None)
sys.modules["redis"] = types.SimpleNamespace(Redis=lambda *a, **k: None)
sys.modules["rq"]    = types.SimpleNamespace(Queue=lambda *a, **k: None)
sys.modules["minio"] = types.SimpleNamespace(
    Minio=lambda *a, **k: types.SimpleNamespace(
        bucket_exists=lambda b: True, make_bucket=lambda b: None,
        put_object=lambda *a, **k: None, get_object=lambda **k: types.SimpleNamespace(read=lambda: b"")
    ), S3Error=Exception
)

from analysis.app.tasks import _stats  # noqa: E402

@pytest.mark.parametrize("text,exp", [
    ("", (0, 0, 0)),
    ("One two\n\nThree", (2, 3, len("One two\n\nThree"))),
    ("  A    B C ", (1, 3, len("  A    B C "))),
])
def test__stats_counts(text, exp):
    paragraphs, words, characters = _stats(text)
    assert (paragraphs, words, characters) == exp
