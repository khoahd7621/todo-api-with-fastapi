from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

from schemas.task import ETaskStatus, EPriority

class TaskModel(BaseModel):
    summary: str = Field(min_length=2)
    description: Optional[str]
    status: ETaskStatus = Field(default=ETaskStatus.TODO)
    priority: EPriority = Field(default=EPriority.LOW)
    company_id: UUID
    user_id: Optional[UUID]


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