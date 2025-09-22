import datetime as dt
import enum

from pydantic import BaseModel, model_validator


class TaskSchema(BaseModel):
    title: str
    user_id: int
    description: str
    status: str
    priority: str
    due_date: dt.date
    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    @classmethod
    def check_title_not_none(cls, values):
        if values.get("title") is None:
            raise ValueError("Title cannot be None")
        return values


class TaskCreateSchema(BaseModel):
    title: str
    description: str | None = None
    priority: str
    due_date: dt.date
