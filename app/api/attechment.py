import os
import shutil
from uuid import uuid1
from typing import Annotated

from sqlalchemy.orm import Session
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException, status, File, UploadFile, Form
from supabase import create_client

from ..core.config import settings
from ..models.user import User
from ..models.task import Task, Attechment
from ..core.dependencies import get_db
from .deps import get_user
from ..schemas.attechment import AttechmentResponse

router = APIRouter(prefix='/attechment', tags=['Attechment'])
supabase = create_client(settings.supabase_url, settings.supabase_key)


@router.post('/')
def create_attechment(
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
    att_file: Annotated[UploadFile, File()],
    task_id: Annotated[int, Form()]
) -> AttechmentResponse: 
    
    task = db.query(Task).filter(Task.task_id==task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found.'
        )
        
    get_file_type = att_file.filename[::-1].split('.')[0][::-1]
    
    create_file_path = f'media/attechment/{uuid1()}.{get_file_type}'
    
    if len(create_file_path) >= 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='File name is too long.'
        )
    
    # Save file locally
    # with open(create_file_path, 'wb') as f:
    #     shutil.copyfileobj(att_file.file, f)
    
    # Upload to Supabase Storage
    supabase.storage.from_('attechment').upload(create_file_path, att_file.file)
    
    public_url = supabase.storage.from_('attechment').get_public_url(create_file_path)
    
    new_attechment = Attechment(
        file_path=public_url.public_url,
        task_id=task_id
    )
    
    db.add(new_attechment)
    db.commit()
    db.refresh(new_attechment)
    
    return new_attechment
    

@router.get('/{pk}')
def get_one_attechment(
    pk: int,
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)]
) -> AttechmentResponse:
    attechment = db.query(Attechment).filter(Attechment.attechment_id==pk).first()
    
    if not attechment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Attechment not found'
        )
    
    return attechment
    

@router.delete('/{pk}')
def delete_attechment(
    pk: int,
    user: Annotated[User, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
) -> dict:
    get_att_file = db.query(Attechment).filter(Attechment.attechment_id==pk).first()
    
    if not get_att_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Attechment not found'
        )
    
    os.remove(get_att_file.file_path)
    
    db.delete(get_att_file)
    db.commit()
    
    return {'detail': 'Attechment deleted successfully.'}
    
