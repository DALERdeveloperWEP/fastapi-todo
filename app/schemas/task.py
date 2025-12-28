from typing import Annotated, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from ..models.task import Priority, TaskStatus
from sqlalchemy import Enum as SQLEnum


class TaskCreate(BaseModel):
    name: Annotated[str, Field(max_length=128, min_length=3)]
    description: Annotated[str | None, Field(max_length=255)] = None
    category_id: int
    due_date: datetime
    priority: Priority = Priority.PRIORITY05

    class Config:
        from_attributes = True


class TaskResponse(BaseModel):
    task_id: int
    name: Annotated[str, Field(max_length=128, min_length=3)]
    category_id: int
    user_id: int
    description: Annotated[str | None, Field(max_length=255)] = None
    due_date: datetime
    status: TaskStatus
    priority: Priority
    create_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    name: Optional[Annotated[str, Field(max_length=128, min_length=3)]] = None
    description: Optional[Annotated[str, Field(max_length=255)]] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    category_id: Optional[int] = None
