import datetime
from dataclasses import dataclass
from datetime import timedelta

import jwt

from app.config import settings
from app.exceptions import (
    NotFound,
    Unauthorized,
)
from app.models.user import User
from app.repository.user import UserRepository
from app.schemas.users import UserLoginSchema


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: settings

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=token)

    @staticmethod
    def _validate_auth_user(user: User, password: str):
        if not user:
            raise NotFound
        if user.password != password:
            raise Unauthorized

    def generate_access_token(self, user_id: int) -> str:
        expires_date_unix = (datetime.datetime.now() + timedelta(days=7)).timestamp()
        payload = {
            "user_id": user_id,
            "expire": expires_date_unix,
        }
        return jwt.encode(
            payload,
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ENCODE_ALGORITHM,
        )

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(
                access_token,
                key=settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ENCODE_ALGORITHM],
            )
        except jwt.PyJWTError:
            raise Unauthorized

        if payload["expire"] < datetime.datetime.now().timestamp():
            raise Unauthorized

        return payload["user_id"]
