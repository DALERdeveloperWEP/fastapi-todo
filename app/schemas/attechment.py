from typing import Annotated
from pydantic import BaseModel, Field

class AttechmentResponse(BaseModel):
    attechment_id: int
    file_path: str
    task_id: int