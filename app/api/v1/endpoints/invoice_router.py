from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from schemas.invoice import InvoiceCreate, InvoiceResponse
from services.invoice_service import create_invoice, get_invoices, get_invoice_by_id

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("/", response_model=InvoiceResponse)
def create_new_invoice(invoice_data: InvoiceCreate, db: Session = Depends(get_db)):
    invoice = create_invoice(db, invoice_data)
    return invoice


@router.get("/", response_model=list[InvoiceResponse])
def list_invoices(db: Session = Depends(get_db)):
    return get_invoices(db)


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = get_invoice_by_id(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice
