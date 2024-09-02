from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from models.task import TaskViewModel
from models.user import UserViewModel

class SearchCompanyModel():
    def __init__(self, name, page, size) -> None:
        self.name = name
        self.page = page
        self.size = size


class CompanyModel(BaseModel):
    name: str
    description: Optional[str]
    rating: int = Field(ge=0, le=5, default=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Company 1",
                "description": "Description for Company 1",
                "rating": 4
            }
        }


class CompanyViewModel(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    rating: int
    tasks: list[TaskViewModel]
    users: list[UserViewModel]
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    class Config:
        from_attributes = True