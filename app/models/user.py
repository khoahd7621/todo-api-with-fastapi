from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from models.task import TaskViewModel


class UserModel(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str

class UserBaseModel(BaseModel):
    id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
    company_id: UUID
    tasks: list[TaskViewModel]
    
    class Config:
        from_attributes = True

class UserViewModel(UserBaseModel):
    is_admin: bool
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

class UserClaims(BaseModel):
    sub: str
    id: str
    first_name: Optional[str]
    last_name: Optional[str]
    is_admin: bool = False