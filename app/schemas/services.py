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
    service_stop_date: Optional[date] = None

class ServiceAssignmentResponse(BaseModel):
    id: int
    client_id: int
    service_id: int
    service_start_month: date
    billing_start_date: date
    service_stop_date: Optional[date] = None
    status: bool
    description: str
    link_capacity: str
    rate: Optional[float]
    created_by: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True



class InvoicePreviewRequest(BaseModel):
    client_id: int
    months: List[date]


class InvoicePreviewServiceItem(BaseModel):
    assignment_id: int
    service_id: int
    service_name: str
    description: str
    link_capacity: str
    rate: Optional[float]
    billing_start_date: date
    service_start_month: date
    service_stop_date: Optional[date]
    status: bool
    prorated_days: int
    prorated_amount: float


class InvoicePreviewMonth(BaseModel):
    month: date
    label: str
    days_in_month: int
    services: List[InvoicePreviewServiceItem]


class InvoicePreviewResponse(BaseModel):
    client_id: int
    months: List[InvoicePreviewMonth]