from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    superadmin = "superadmin"
    admin = "admin"
    manager = "manager"

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
