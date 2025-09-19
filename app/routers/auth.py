from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.dependency import get_auth_service
from app.exceptions import NotFound, Unauthorized
from app.schemas.users import LoginSchema, UserLoginSchema
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserLoginSchema)
async def login(
    body: LoginSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    try:
        return await auth_service.login(body.username, body.password)
    except NotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Unauthorized as e:
        raise HTTPException(status_code=401, detail=str(e))
