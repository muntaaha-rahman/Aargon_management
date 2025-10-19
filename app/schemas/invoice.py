# schemas/invoice.py
from pydantic import BaseModel
from datetime import date
from typing import Optional

class InvoiceBase(BaseModel):
    client_id: int
    months: str  # e.g., "January 2025, February 2025"
    file_path: Optional[str] = None  # e.g., "invoices/invoice_001.pdf"

class InvoiceCreate(InvoiceBase):
    pass  # All required fields for creation are already in InvoiceBase

class InvoiceOut(InvoiceBase):
    id: int
    invoice_number: str
    created_date: date

    class Config:
        orm_mode = True
