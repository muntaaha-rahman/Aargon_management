from sqlalchemy import Column, Integer, String, DateTime, func, Enum
import enum
from app.core.database import Base

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
