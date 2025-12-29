from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .deps import get_curent_user, get_user
from ..core.dependencies import get_db
from ..models.task import SubTask, Task
from ..models.user import User
from ..schemas.subtask import SubTaskCreate, SubTaskResponse, SubTaskUpdate


router = APIRouter(prefix='/subtask', tags=['SubTask'])


@router.post('/', response_model=SubTaskResponse)
def create_subtask(
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
    data: SubTaskCreate
) -> SubTaskResponse:
    task = db.query(Task).filter(Task.task_id==data.task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found."
        )
        
    
    if task.user_id != user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not allowed.'
        )
    
    
    new_subtask = SubTask(
        name=data.name,
        description = data.description,
        task_id=data.task_id
    )
    
    db.add(new_subtask)
    db.commit()
    db.refresh(new_subtask)
    
    return new_subtask


@router.put('/{pk}', response_model=SubTaskResponse)
def update_subtask(
    pk: int,
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
    data: SubTaskUpdate
) -> SubTaskResponse:
    sub_task = db.query(SubTask).filter(SubTask.sub_task_id==pk).first()
    
    if not sub_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Sub Task not found.'
        )
    
    task = sub_task.task
    
    
    if task.user_id != user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not allowed.'
        )
    
    
    if data.name is not None:
        sub_task.name = data.name

    if data.description is not None:
        sub_task.description = data.description
    
    db.commit()
    db.refresh(sub_task)
    
    return sub_task
    

@router.get('/{pk}', response_model=SubTaskResponse)
def get_one_sub_task(
    pk: int,
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)]
):
    sub_task = db.query(SubTask).filter(SubTask.sub_task_id==pk).first()
    
    if not sub_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Sub Task not found.'
        )
    
    task = sub_task.task

    if task.user_id != user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not allowed.'
        )

        
        
    return sub_task

    
@router.delete('/{pk}', response_model=dict)
def delete_sup_task(
    pk: int,
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)]   
):
    subtask = db.query(SubTask).filter(SubTask.sub_task_id==pk).first()
    
    if not subtask:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Sub Task not found.'
        )
    
    task = subtask.task
    
    
    if task.user_id != user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not allowed.'
        )
    
    db.delete(subtask)
    db.commit()
    return {'detail': 'Sub Task deleted successfully.'}
    