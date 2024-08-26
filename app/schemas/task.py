from sqlalchemy import Column, ForeignKey, String, Enum, Uuid
from sqlalchemy.orm import relationship
import enum

from database import Base
from .base_entity import BaseEntity

class ETaskStatus(enum.Enum):
    TODO = "T"
    IN_PROGRESS = "I"
    DONE = "D"

class EPriority(enum.Enum):
    LOW = "L"
    MEDIUM = "M"
    HIGH = "H"

class Task(Base, BaseEntity):
    __tablename__ = "tasks"

    summary = Column(String(255), nullable=False)
    description = Column(String)
    status = Column(Enum(ETaskStatus), nullable=False, default=ETaskStatus.TODO)
    priority = Column(Enum(EPriority), nullable=False, default=EPriority.LOW)
    company_id = Column(Uuid, ForeignKey("users.id"), nullable=False)
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=True)

    company = relationship("Company")
    user = relationship("User")
