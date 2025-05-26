from sqlalchemy import Column, String, Integer, LargeBinary
from .db import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    hash = Column(String(64), index=True, nullable=False, unique=True)
    location = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
