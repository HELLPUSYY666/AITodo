from models.task import Task
from schemas.tasks import TaskCreateSchema
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.future import select


class TaskRepository:
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    async def get_tasks(self) -> list[Task]:
        async with self.session_maker() as session:
            result = await session.execute(select(Task))
            return result.scalars().all()

    async def get_task_by_id(self, task_id: int) -> Task | None:
        async with self.session_maker() as session:
            result = await session.execute(select(Task).where(Task.id == task_id))
            return result.scalar_one_or_none()

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> Task:
        task_model = Task(
            title=task.title,
            description=task.description,
            status=task.priority,
            due_date=task.due_date,
            user_id=user_id,
        )
        async with self.session_maker() as session:
            session.add(task_model)
            await session.commit()
            await session.refresh(task_model)
            return task_model

    async def delete_task(self, task_id: int, user_id: int) -> None:
        async with self.session_maker() as session:
            await session.execute(
                delete(Task).where(Task.id == task_id, Task.user_id == user_id)
            )
            await session.commit()
            await session.flush()

    async def update_task_title(self, task_id: int, title: str) -> Task:
        async with self.session_maker() as session:
            await session.execute(
                update(Task).where(Task.id == task_id).values(title=title)
            )
            await session.commit()
            result = await session.execute(select(Task).where(Task.id == task_id))
            task = result.scalar_one_or_none()
            if task is None:
                raise ValueError(f"Task with id {task_id} not found")
            return task

    async def get_user_task(self, task_id: int, user_id: int) -> Task | None:
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        async with self.session_maker() as session:
            result = await session.execute(query)
            task = result.scalar_one_or_none()
            return task
