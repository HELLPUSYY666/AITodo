from dataclasses import dataclass, field
from typing import Optional

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models.user import User
from app.schemas.users import UserCreateSchema


@dataclass
class UserRepository:
    session_maker: async_sessionmaker[AsyncSession]

    def __post_init__(self) -> None:
        if not callable(self.session_maker):
            raise TypeError(
                "session_maker должен быть async_sessionmaker, а не AsyncSession. "
                "Проверьте инициализацию репозитория."
            )

    async def get_user_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        async with self.session_maker() as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreateSchema) -> User:
        query = insert(User).values(**user_data.model_dump()).returning(User.id)
        async with self.session_maker() as session:
            result = await session.execute(query)
            user_id = result.scalar_one()
            await session.commit()
            return await self.get_user(user_id, session=session)

    async def get_user(
        self, user_id: int, session: Optional[AsyncSession] = None
    ) -> Optional[User]:
        query = select(User).where(User.id == user_id)
        if session is None:
            async with self.session_maker() as session:
                result = await session.execute(query)
                return result.scalar_one_or_none()
        else:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        query = select(User).where(User.username == username)
        async with self.session_maker() as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()
