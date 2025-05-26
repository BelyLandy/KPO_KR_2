from pydantic import BaseModel, Field

class FileOut(BaseModel):
    id: int
    name: str
    size: int
    location: str

class FileUploadResponse(BaseModel):
    id: int
    is_duplicate: bool
    name: str | None = None
    size: int | None = None
    location: str | None = None
