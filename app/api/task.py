from datetime import datetime
from typing import Annotated, List, Optional
from fastapi import Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from .deps import get_curent_user, get_user
from ..core.dependencies import get_db
from ..models.task import Category, Priority, Task, TaskStatus
from ..models.user import User
from ..schemas.task import TaskCreate, TaskResponse, TaskUpdate


from fastapi.routing import APIRouter

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/")
def create_task(
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
    task_data: TaskCreate,
) -> TaskResponse:
    exists_task = (
        db.query(Task)
        .filter(Task.name == task_data.name, Task.user_id == user.user_id)
        .first()
    )

    if exists_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task with this name already exists.",
        )

    category = (
        db.query(Category).filter(Category.category_id == task_data.category_id).first()
    )
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found."
        )

    new_task = Task(
        name=task_data.name,
        description=task_data.description,
        due_date=task_data.due_date,
        priority=task_data.priority or Priority.PRIORITY05,
        category_id=task_data.category_id,
        user_id=user.user_id,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get("/")
def get_task_list(
    user: Annotated[User, Depends(get_user)], db: Annotated[Session, Depends(get_db)]
):
    tasks = db.query(Task).filter(Task.user_id == user.user_id).all()
    return tasks


@router.get("/filter", response_model=List[TaskResponse])
def filter_tasks(
    user: Annotated[User, Depends(get_curent_user)],
    db: Annotated[Session, Depends(get_db)],
    status: Annotated[Optional[TaskStatus], Query()] = None,
    priority: Annotated[Optional[Priority], Query()] = None,
    due_date: Annotated[Optional[datetime], Query()] = None,
):
    query = db.query(Task).filter(Task.user_id == user.user_id)

    # print()

    if status is not None:
        query = query.filter(Task.status == status)
    if priority is not None:
        query = query.filter(Task.priority == priority)
    if due_date is not None:
        query = query.filter(Task.due_date <= due_date)

    # print(status, priority.value, due_date)

    tasks = query.all()
    return tasks


@router.get("/{pk}")
def get_one_task(
    pk: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_user)],
):
    exists_task = (
        db.query(Task).filter(Task.task_id == pk, Task.user_id == user.user_id).first()
    )

    if not exists_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found."
        )

    return exists_task


@router.put("/{pk}")
def update_task(
    pk: int,
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
    task_data: TaskUpdate,
) -> TaskResponse:
    task = (
        db.query(Task).filter(Task.task_id == pk, Task.user_id == user.user_id).first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found."
        )

    if task_data.name:
        if db.query(Task).filter(Task.name == task_data.name, Task.user_id == user.user_id).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task with this name already exists.",
            )
        task.name = task_data.name
    task.description = (
        task_data.description if task_data.description else task.description
    )
    task.due_date = task_data.due_date if task_data.due_date else task.due_date
    task.priority = task_data.priority if task_data.priority else task.priority
    task.status = task_data.status if task_data.status else task.status
    if task_data.category_id:
        if not db.query(Category).filter(Category.category_id == task_data.category_id).first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found."
            )
        task.category_id = task_data.category_id

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{pk}")
def delete_task(
    pk: int,
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
):
    task = (
        db.query(Task).filter(Task.task_id == pk, Task.user_id == user.user_id).first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found."
        )

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
