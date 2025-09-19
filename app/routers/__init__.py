from fastapi import APIRouter

from .auth import router as auth_router
from .tasks import router as tasks_router

main_router = APIRouter()

main_router.include_router(auth_router)
main_router.include_router(tasks_router)
