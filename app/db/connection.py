from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

async_engine = create_async_engine(
    settings.POSTGRES_DSN,
    echo=True,
)
async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


def get_session_maker() -> async_sessionmaker[AsyncSession]:
    return async_session


SessionMakerDependency = Annotated[
    async_sessionmaker[AsyncSession], Depends(get_session_maker)
]
SessionDependency = Annotated[AsyncSession, Depends(get_session)]
