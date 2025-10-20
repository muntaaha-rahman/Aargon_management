# app/api/v1/endpoints/invoice_router.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
from datetime import date

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.auth import User
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate, InvoiceOut
from app.utils.invoice_pdf import generate_invoice_pdf  # Your PDF generator function

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

# --- Create Invoice ---
@router.post("/", response_model=InvoiceOut)
def create_new_invoice(
    invoice_data: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new invoice:
    - Generates invoice number
    - Generates PDF and stores file path
    - Saves record in DB
    """
    # Generate unique invoice number
    invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"  # e.g., INV-1A2B3C4D

    # Generate PDF
    file_path = generate_invoice_pdf(
        invoice_number=invoice_number,
        client_name=current_user.name,   # or fetch client by ID if needed
        client_address=current_user.address if hasattr(current_user, "address") else "",
        months=invoice_data.months
    )

    # Save to DB
    new_invoice = Invoice(
        invoice_number=invoice_number,
        client_id=invoice_data.client_id,
        months=invoice_data.months,
        created_date=date.today(),
        file_path=file_path
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    return new_invoice

# --- List all invoices ---
@router.get("/", response_model=List[InvoiceOut])
def list_all_invoices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Invoice).order_by(Invoice.created_date.desc()).all()

# --- Get single invoice ---
@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

# --- Download PDF ---
@router.get("/{invoice_id}/download")
def download_invoice_pdf(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if not invoice.file_path or not os.path.exists(invoice.file_path):
        raise HTTPException(status_code=404, detail="Invoice PDF not found")

    return FileResponse(
        path=invoice.file_path,
        filename=os.path.basename(invoice.file_path),
        media_type='application/pdf'
    )
