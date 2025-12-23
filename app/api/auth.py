from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import Depends, Body, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from ..core.dependencies import get_db
from ..core.security import hash_password, create_token, verify_password
from ..schemas.user import UserRegister, UserResponse
from ..models.user import User

router = APIRouter(prefix="/auth")
security = HTTPBasic()


def get_user_by_username(user: str, database: Session) -> User:
    return database.query(User).filter(User.username == user.username).first()


@router.post("/register", response_model=UserResponse)
def register(
    user_data: Annotated[UserRegister, Body()], db: Annotated[Session, Depends(get_db)]
):
    if get_user_by_username(user_data, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User exists."
        )

    new_user = User(
        username=user_data.username, password=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db: Annotated[Session, Depends(get_db)],
):
    user = get_user_by_username(credentials, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    if not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
        )

    return {"token": create_token(user.user_id)}
