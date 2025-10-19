# routes/invoice.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os

from database import get_db  # Your DB session dependency
from models.invoice import Invoice
from schemas.invoice import InvoiceCreate, InvoiceOut
from services.invoice_service import create_invoice, get_invoices, get_invoice_by_id

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

@router.post("/", response_model=InvoiceOut)
def create_new_invoice(invoice_data: InvoiceCreate, db: Session = Depends(get_db)):
    """
    Create a new invoice. Auto-generates invoice number, PDF, and created_date.
    """
    invoice = create_invoice(db, invoice_data)
    if not invoice:
        raise HTTPException(status_code=400, detail="Invoice creation failed")
    return invoice

@router.get("/", response_model=List[InvoiceOut])
def list_all_invoices(db: Session = Depends(get_db)):
    """
    Get all invoices, newest first
    """
    return get_invoices(db)

@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """
    Get a single invoice by ID
    """
    invoice = get_invoice_by_id(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.get("/{invoice_id}/download")
def download_invoice_pdf(invoice_id: int, db: Session = Depends(get_db)):
    """
    Download the PDF file for a given invoice ID
    """
    invoice = get_invoice_by_id(db, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if not invoice.file_path or not os.path.exists(invoice.file_path):
        raise HTTPException(status_code=404, detail="Invoice PDF not found")
    
    return FileResponse(
        path=invoice.file_path,
        filename=os.path.basename(invoice.file_path),
        media_type='application/pdf'
    )
