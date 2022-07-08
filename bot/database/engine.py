from sqlalchemy.ext.asyncio import create_async_engine


def get_engine(db_url: str):
    engine = create_async_engine(db_url, echo=False)
    return engine
