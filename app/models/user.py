from enum import Enum
from datetime import datetime

from sqlalchemy import String, DateTime, Column, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship

from ..core.database import Base


class Role(str, Enum):
    OWNER = "owner"
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    user_id = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column(String(length=64), unique=True, nullable=False)
    password = Column(String(length=128), nullable=False)
    role = Column(SQLEnum(Role), default=Role.USER, nullable=False)

    tasks = relationship("Task", back_populates="user", lazy="dynamic")

    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return self.username

    @property
    def is_user(self) -> bool:
        return self.role == Role.USER

    @property
    def is_admin(self) -> bool:
        return self.role == Role.ADMIN
