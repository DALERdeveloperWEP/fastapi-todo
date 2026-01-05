from pydantic import BaseModel, Field
from typing import Annotated, Optional

class SubTaskCreate(BaseModel):
    user_id: Annotated[int, Field(ge=1)]
    name: Annotated[str, Field(max_length=64, min_length=2)]
    description: Annotated[Optional[str], Field(max_length=255)] = None
    task_id: Annotated[int, Field(ge=1)]


class SubTaskResponse(BaseModel):
    user_id: int
    sub_task_id: int
    name: str
    description: Optional[str]
    task_id: int

    class Config:
        from_attributes = True


class SubTaskUpdate(BaseModel):
    name: Annotated[Optional[str], Field(max_length=64, min_length=2)] = None
    description: Annotated[Optional[str], Field(max_length=255)] = None
