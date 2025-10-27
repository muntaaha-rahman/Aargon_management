from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class PaymentMethod(str, Enum):
    cash = "Cash"
    bank_transfer = "Bank Transfer"
    bkash = "Bkash"

# Payment Schemas
class PaymentCreate(BaseModel):
    date: date
    received_amount: float
    discount: Optional[float] = None
    method: PaymentMethod
    description: Optional[str] = None
    client_id: int

class PaymentUpdate(BaseModel):
    date: Optional[date] = None
    received_amount: Optional[float] = None
    discount: Optional[float] = None
    method: Optional[PaymentMethod] = None
    description: Optional[str] = None

class PaymentResponse(BaseModel):
    id: int
    date: date
    received_amount: float
    discount: Optional[float]
    method: PaymentMethod
    description: Optional[str]
    client_id: int
    client_name: str
    received_by_id: int
    received_by_name: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Payment Summary Schemas
class PaymentSummary(BaseModel):
    total_received: float
    total_discount: float
    payment_count: int

class ClientPaymentSummary(PaymentSummary):
    client_id: int
    client_name: str

class PaymentStatsResponse(BaseModel):
    overall: PaymentSummary
    by_client: List[ClientPaymentSummary]
    by_method: dict