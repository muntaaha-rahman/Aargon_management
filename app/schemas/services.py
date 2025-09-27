from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ServiceCreate(BaseModel):
    name: str

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    active: Optional[bool] = None

class ServiceResponse(BaseModel):
    id: int
    name: str
    active: bool
    created_by: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ServiceActiveUpdate(BaseModel):
    active: bool
