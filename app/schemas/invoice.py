from pydantic import BaseModel
from datetime import date


class InvoiceBase(BaseModel):
    client_id: int
    months: str  # e.g. "January 2025, February 2025"
    file_path: str | None = None


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceResponse(InvoiceBase):
    id: int
    invoice_number: str
    created_date: date

    class Config:
        orm_mode = True
