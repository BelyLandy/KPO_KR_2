from pydantic import BaseModel
from typing import Optional

class AnalysisResponse(BaseModel):
    ready: bool
    paragraphs: Optional[int] = None
    words: Optional[int] = None
    characters: Optional[int] = None
    wordcloud_location: Optional[str] = None