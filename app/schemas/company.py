from sqlalchemy import Column, String, SmallInteger
from sqlalchemy.orm import relationship

from database import Base
from .base_entity import BaseEntity

class Company(Base, BaseEntity):
    __tablename__ = "companies"

    name = Column(String(255), nullable=False)
    description = Column(String)
    rating = Column(SmallInteger, default=0)

    tasks = relationship("Task", back_populates='company')
    users = relationship("User", back_populates='company')
