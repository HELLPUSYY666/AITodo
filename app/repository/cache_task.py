import json
from typing import List, Optional

import redis.asyncio as redis

from app.schemas.tasks import TaskSchema


class TaskCacheRepository:
    def __init__(self, cache_session: redis.Redis) -> None:
        self.cache_session = cache_session

    async def get_all_tasks(
        self, user_id: int, key: str = "all_tasks"
    ) -> List[TaskSchema]:
        tasks_json = await self.cache_session.get(key)
        if tasks_json is None:
            return []
        parsed = json.loads(tasks_json)
        filtered = [task for task in parsed if task.get("user_id") == user_id]
        return [TaskSchema.model_validate(task) for task in filtered]

    async def set_all_tasks(
        self, tasks: List[TaskSchema], key: str = "all_tasks", ex: int = 3600
    ) -> None:
        tasks_data = [task.model_dump(mode="json") for task in tasks]
        await self.cache_session.set(key, json.dumps(tasks_data), ex=ex)

    async def get_task(self, task_id: int) -> Optional[TaskSchema]:
        key = f"task:{task_id}"
        task_json = await self.cache_session.get(key)
        if task_json is None:
            return None
        return TaskSchema.model_validate(json.loads(task_json))

    async def set_task(self, task: TaskSchema, task_id: int, ex: int = 3600) -> None:
        key = f"task:{task_id}"
        task_data = task.model_dump(mode="json")
        await self.cache_session.set(key, json.dumps(task_data), ex=ex)

    async def delete_task_cache(self, task_id: int) -> None:
        key = f"task:{task_id}"
        await self.cache_session.delete(key)

    async def invalidate_all_tasks(self) -> None:
        await self.cache_session.delete("all_tasks")
