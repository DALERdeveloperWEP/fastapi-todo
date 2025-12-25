from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..core.security import verify_token
from ..models.user import User
from ..core.dependencies import get_db


security = HTTPBearer()


def get_curent_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
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
    
    return user


def get_user(user: Annotated[User, Depends(get_curent_user)]) -> User:
    if not user.is_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission dendied.")
        
    return user

def get_admin(admin: Annotated[User, Depends(get_curent_user)]) -> User:
    if not admin.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission dendied.")
        
    return admin