from sqlalchemy import Column, ForeignKey, String, Boolean, Uuid
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

from database import Base
from .base_entity import BaseEntity

bcrypt_context = CryptContext(schemes=["bcrypt"])

class User(Base, BaseEntity):
    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    company_id = Column(Uuid, ForeignKey("companies.id"), nullable=False)

    tasks = relationship("Task", back_populates="user")
    company = relationship("Company")


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hased_password):
    return bcrypt_context.verify(plain_password, hased_password)
