from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None

class ClientStatusUpdate(BaseModel):
    active: bool

class ClientResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    active: bool
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True