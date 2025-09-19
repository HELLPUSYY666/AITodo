from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependency import get_user_service
from app.schemas.users import UserCreateSchema, UserLoginSchema
from app.services.user import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post("", response_model=UserLoginSchema)
async def create_user(
    body: UserCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.create_user(body.username, body.password)
