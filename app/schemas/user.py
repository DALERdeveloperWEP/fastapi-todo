from typing_extensions import Self
from typing import Annotated
from pydantic import BaseModel, Field, model_validator

from ..models.user import Role


class UserRegister(BaseModel):
    username: Annotated[str, Field(min_length=5, max_length=64)]
    password: Annotated[str, Field(min_length=8, max_length=20)]
    confirm: Annotated[str, Field(min_length=8, max_length=20)]

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password != self.confirm:
            raise ValueError("Passwords do not match")
        return self


class UserResponse(BaseModel):
    user_id: int
    username: Annotated[str, Field(min_length=5, max_length=64)]
    password: Annotated[str, Field(min_length=8, max_length=128)]
    role: Role
    
    class config:
        from_atributes = True


class ProfileResults(BaseModel):
    task_count: int
    task_todo: int
    task_doing: int
    task_done: int


class UserProfile(BaseModel):
    user: UserResponse
    result: ProfileResults
