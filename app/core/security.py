from typing import Dict
from time import time
import jwt
from passlib.hash import bcrypt

from .config import settings


def hash_password(plain_password: str) -> str:
    return bcrypt.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)


def create_token(user_id: str) -> Dict[str, str]:
    payload = {"user_id": user_id, "expires": time() + 900}
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    return token


def verify_token(token: str) -> dict:
    try:
        decode_token = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return decode_token if decode_token['expires'] > time() else None
    except:
        return None