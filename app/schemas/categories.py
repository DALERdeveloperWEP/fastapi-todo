from pydantic import BaseModel, Field
from typing import Annotated


class CategoryResponse(BaseModel):
    category_id: int
    name: Annotated[str, Field(max_length=64, min_length=3)]
    color: Annotated[str, Field(min_length=7, max_length=7)]
    icon: Annotated[str, Field(max_length=255)]

    class Config:
        orm_mode = True


class CategoryUpdate(BaseModel):
    name: Annotated[str | None, Field(max_length=64, min_length=3)] = None
    color: Annotated[str | None, Field(min_length=7, max_length=7)] = None
    # icon: Annotated[str | None, Field(max_length=255)] = None
