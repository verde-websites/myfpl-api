"""
Creates connections to the database at the top level
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .settings import get_settings

config = get_settings()

engine = create_async_engine(config.database_url)
SessionLocal = async_sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass