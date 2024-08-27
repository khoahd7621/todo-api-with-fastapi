from sqlalchemy import Table, Column, Uuid, ForeignKey

from database import Base
from .base_entity import BaseEntity

class CompanyUser(Base, BaseEntity):
    __tablename__ = "company_users"

    user_id = Column(Uuid, ForeignKey('users.id'))
    company_id = Column(Uuid, ForeignKey('companies.id'))
