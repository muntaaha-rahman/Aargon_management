from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

# Service Schemas
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

# Service Assignment Schemas
class ServiceAssignmentCreate(BaseModel):
    client_id: int
    service_id: int
    service_start_month: date
    billing_start_date: date
    description: str
    link_capacity: str
    rate: Optional[float] = None

class ServiceAssignmentUpdate(BaseModel):
    status: Optional[bool] = None
    description: Optional[str] = None
    link_capacity: Optional[str] = None
    rate: Optional[float] = None

class ServiceAssignmentResponse(BaseModel):
    id: int
    client_id: int  # Keep as ID
    service_id: int  # Keep as ID
    service_start_month: date
    billing_start_date: date
    status: bool
    description: str
    link_capacity: str
    rate: Optional[float]
    created_by: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True