from typing import Annotated, List, Dict
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Request
from fastapi.routing import APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..core.security import verify_token
from ..models.user import User
from ..models.task import TaskStatus, Task
from ..core.dependencies import get_db
from ..schemas.user import UserResponse, UserProfile


security = HTTPBearer()


router = APIRouter(prefix="/users")


@router.get('/', response_model=List[UserResponse])
def get_users(db: Annotated[Session, Depends(get_db)]):
    return db.query(User).all()


@router.get("/profile", response_model=UserProfile)
def profile(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[Session, Depends(get_db)],
):
    decode_token = verify_token(credentials.credentials)

    if not decode_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
        )

    user: User = db.query(User).get(decode_token["user_id"])
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
        )
    
    if not user.is_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Permission dendied."
        )
        
   
    result = {
        'task_count': user.tasks.count(),
        'task_todo': user.tasks.filter_by(status=TaskStatus.TODO).count(),
        'task_doing': user.tasks.filter_by(status=TaskStatus.DOING).count(),
        'task_done': user.tasks.filter_by(status=TaskStatus.DONE).count()
    }

    print({
        'user': user,
        'result': result
    })
    return {
        'user': user,
        'result':result 
    }
