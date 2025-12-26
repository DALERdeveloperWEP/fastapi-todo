from typing import Annotated, List, Dict
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter

from ..models.user import User
from ..models.task import TaskStatus
from ..core.dependencies import get_db
from ..schemas.user import UserResponse, UserProfile
from ..api.deps import get_user, get_admin


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
def get_users(db: Annotated[Session, Depends(get_db)]):
    return db.query(User).all()


@router.get("/profile", response_model=UserProfile)
def profile(
    db: Annotated[Session, Depends(get_db)], user: Annotated[User, Depends(get_user)]
):
    result = {
        "task_count": user.tasks.count(),
        "task_todo": user.tasks.filter_by(status=TaskStatus.TODO).count(),
        "task_doing": user.tasks.filter_by(status=TaskStatus.DOING).count(),
        "task_done": user.tasks.filter_by(status=TaskStatus.DONE).count(),
    }

    print({"user": user, "result": result})
    return {"user": user, "result": result}
