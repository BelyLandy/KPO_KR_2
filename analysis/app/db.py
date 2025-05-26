import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session: sessionmaker[AsyncSession] = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()