import os

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

import analysis.app.db as db_mod  # noqa: E402

def test_db_engine_and_session_exist():
    assert hasattr(db_mod, "engine")
    assert hasattr(db_mod, "async_session")
    assert os.getenv("DATABASE_URL") is not None
