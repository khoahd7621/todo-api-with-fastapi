from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from base_entity import BaseEntity

class CompanyUser(Base, BaseEntity):
    __tablename__ = "company_users"

    user_id = Column(Integer, ForeignKey('users.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

