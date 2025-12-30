from typing import Annotated, List

from sqlalchemy.orm import Session
from sqlalchemy import func, case
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status
from .deps import get_admin
from ..core.dependencies import get_db
from ..models.user import User, Role
from ..models.task import Task, TaskStatus
from ..schemas.adminPanel import UserResponse, UserResponseDetalies, UserEditRole


router = APIRouter(prefix='/admin', tags=['Admin Panel Check Users'])

@router.get('/users', response_model=List[UserResponse])
def all_users(
    admin: Annotated[User, Depends(get_admin)],
    db: Annotated[Session, Depends(get_db)]
) -> List[UserResponse]:
    return db.query(User).all()


@router.get('/users_detalies', response_model=List[UserResponseDetalies])
def all_users_detalies(
    admin: Annotated[User, Depends(get_admin)],
    db: Annotated[Session, Depends(get_db)]
) -> List[UserResponseDetalies]:
    return db.query(User).all()


@router.put('/{pk}')
def edit_role(
    pk: int,
    admin: Annotated[User, Depends(get_admin)],
    db: Annotated[Session, Depends(get_db)],
    role: UserEditRole
) -> UserResponse:
    user = db.query(User).filter(User.user_id==pk).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    
    if role:
        user.role = role.role.value
    
    db.commit()
    db.refresh(user)
    
    return user


@router.get('/filter_by_task')
def filter_by_task(
    admin: Annotated[User, Depends(get_admin)],
    db: Annotated[Session, Depends(get_db)]
):
    users_with_task_stats = (
        db.query(
            User.username,
            func.count(Task.task_id).label("all_tasks"),
            func.count(case((Task.status == TaskStatus.DONE, 1)))
            .label("done"),
            func.count(case((Task.status == TaskStatus.TODO, 1)))
            .label("todo"),
            func.count(case((Task.status == TaskStatus.DOING, 1)))
            .label("doing"),
        )
        .outerjoin(Task, User.user_id == Task.user_id)
        .filter(User.role != Role.ADMIN)
        .group_by(User.user_id)
        .order_by(func.count(Task.task_id).desc())  # ko'pdan kamga
        .all()
    )

    response = []

    for index, (
        name, task_caunt, 
        status_done, status_todo, 
        status_doing
    ) in enumerate(users_with_task_stats, start=1):
        response.append({
            "name": name,
            "task_caunt": task_caunt,
            "status_done": status_done,
            "status_todo": status_todo,
            "status_doing": status_doing
        })

    return response
