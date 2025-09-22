from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependency import get_request_user_id, get_task_service
from app.exceptions import NotFound
from app.schemas.tasks import TaskCreateSchema, TaskSchema
from app.services.task import TaskService

router = APIRouter(prefix="/task", tags=["tasks"])


@router.get("/all", response_model=List[TaskSchema])
async def get_all_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id),
):
    return await task_service.get_tasks(user_id=user_id)


@router.get("/{task_id}", response_model=TaskSchema)
async def get_task_by_id(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id),
):
    return await task_service.get_task(task_id, user_id=user_id)


@router.post("/task", response_model=TaskSchema)
async def create_task(
    body: TaskCreateSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id),
):
    task = await task_service.create_task(body, user_id)
    return TaskSchema.model_validate(task)


@router.patch("/{task_id}", response_model=TaskSchema)
async def update_task(
    task_id: int,
    name: str,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id),
):
    try:
        return await task_service.update_task_name(task_id, name, user_id)
    except NotFound(model_name="Task", ident=task_id) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id),
):
    try:
        await task_service.delete_task(task_id=task_id, user_id=user_id)
    except NotFound(model_name="Task", ident=task_id) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
