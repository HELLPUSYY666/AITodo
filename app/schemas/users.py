from typing import Optional

from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str


class UserCreateSchema(BaseModel):
    username: str
    password: Optional[str] = None
    name: Optional[str] = None


class LoginSchema(BaseModel):
    username: str
    password: str
