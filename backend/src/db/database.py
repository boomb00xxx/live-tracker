from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings


engine = create_async_engine(settings.DB_URL, echo=True)

async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


def session_manager(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            async with session.begin():
                res = await func(session, *args, **kwargs)
        return res

    return wrapper











