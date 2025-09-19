from exceptions import Unauthorized
from fastapi import Depends, HTTPException, Security, security
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.cache.accesor import get_redis_connection
from app.config import settings
from app.db.connection import get_session
from app.repository.cache_task import TaskCacheRepository
from app.repository.task import TaskRepository
from app.repository.user import UserRepository
from app.services.task import TaskService


async def get_task_repository(
    session_maker: async_sessionmaker[AsyncSession] = Depends(get_session),
) -> TaskRepository:
    return TaskRepository(session_maker)


async def get_task_cache_repository() -> TaskCacheRepository:
    redis_connection = await get_redis_connection()
    return TaskCacheRepository(redis_connection)


def get_task_service(
    task_repository: TaskRepository = Depends(get_task_repository),
    task_cache: TaskCacheRepository = Depends(get_task_cache_repository),
) -> TaskService:
    return TaskService(task_repository=task_repository, task_cache=task_cache)


def get_user_repository(
    session_maker: async_sessionmaker[AsyncSession] = Depends(get_session),
) -> UserRepository:
    return UserRepository(session_maker)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=settings,
    )


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


reusable_oauth2 = security.HTTPBearer()


def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except Unauthorized as e:
        raise HTTPException(status_code=401, detail=e.detail)
    except Unauthorized as e:
        raise HTTPException(status_code=401, detail=e.detail)
    return user_id
