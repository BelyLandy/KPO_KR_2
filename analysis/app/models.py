from sqlalchemy import Column, Integer, String, DateTime, func
from .db import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, unique=True, index=True)
    paragraphs = Column(Integer)
    words = Column(Integer)
    characters = Column(Integer)
    wordcloud_location = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())