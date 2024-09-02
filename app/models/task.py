from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

from schemas.task import ETaskStatus, EPriority

class SearchTaskModel():
    def __init__(self, company_id, user_id, page, size) -> None:
        self.company_id = company_id
        self.user_id = user_id
        self.page = page
        self.size = size


class TaskCreateModel(BaseModel):
    summary: str = Field(min_length=2)
    description: Optional[str]
    priority: EPriority = Field(default=EPriority.LOW)
    company_id: UUID
    user_id: Optional[UUID]


class TaskUpdateModel(BaseModel):
    summary: Optional[UUID] = Field(min_length=2)
    description: Optional[str]
    priority: EPriority = Field(default=EPriority.LOW)
    company_id: Optional[UUID]
    user_id: Optional[UUID]


class TaskUpdateStatusModel(BaseModel):
    status: ETaskStatus

class TaskViewModel(BaseModel):
    id: UUID
    summary: str
    description: Optional[str]
    status: ETaskStatus
    priority: EPriority
    company_id: UUID
    user_id: Optional[UUID]
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        from_attributes = True