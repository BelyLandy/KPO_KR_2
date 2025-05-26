import os
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

import storing.app.db as db_mod  # noqa:E402

def test_storing_db_objects():
    assert hasattr(db_mod, "engine")
    assert hasattr(db_mod, "async_session")
    assert os.getenv("DATABASE_URL") is not None
