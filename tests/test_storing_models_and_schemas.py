import pytest

from storing.app.models import File  # noqa: E402
from storing.app.schemas import FileOut, FileUploadResponse  # noqa: E402

def test_models_and_schemas_exist():
    fo = FileOut(id=1, name="a", size=10, location="loc")
    assert fo.id == 1
    fur = FileUploadResponse(id=1, is_duplicate=False)
    assert not fur.is_duplicate
