from sqlalchemy import (
    Column, String, Integer, Enum, ForeignKey, Date, Text, DateTime, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    superadmin = "superadmin"
    admin = "admin"
    manager = "manager"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)  # hashed
    role = Column(Enum(UserRole), nullable=False, default=UserRole.manager)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
