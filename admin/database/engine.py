from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from database import Base


def get_db() -> SQLAlchemy:
    db = SQLAlchemy(metadata=Base.metadata)
    return db


def get_engine(db_url: str):
    engine = create_async_engine(db_url, pool_size=20, max_overflow=0,
                                 poolclass=QueuePool)
    return engine


def get_async_session_maker(db_url: str):
    engine = get_engine(db_url=db_url)
    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
