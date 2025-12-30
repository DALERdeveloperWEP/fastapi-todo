from datetime import datetime
from pydantic import BaseModel

from ..models.user import Role

class UserResponse(BaseModel):
    user_id: int
    username: str
    role: str
    
    class Config:
        from_attributes = True
    

class UserResponseDetalies(BaseModel):
    user_id: int
    username: str
    role: str
    password: str 
    create_at: datetime 
    update_at: datetime
    

    class Config:
        from_attributes = True
        
    
class UserEditRole(BaseModel):
    role: Role
    
