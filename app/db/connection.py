from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ..config import settings

async_engine = create_async_engine(settings.POSTGRES_DSN)

async_session = async_sessionmaker(async_engine)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e


SessionDependency = Annotated[AsyncSession, Depends(get_session)]
