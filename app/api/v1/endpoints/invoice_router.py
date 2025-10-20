# app/api/v1/endpoints/invoice_router.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
from datetime import date
import json

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.auth import User
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceCreate, InvoiceOut
from app.utils.invoice_pdf import generate_invoice_pdf

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

# --- Create Invoice (UPDATED for File Upload) ---
@router.post("/", response_model=InvoiceOut)
async def create_new_invoice(
    file: UploadFile = File(...),
    client_id: int = Form(...),
    invoice_number: str = Form(...),
    months: str = Form(...),  # JSON string of months array
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new invoice with file upload
    - Receives PDF file from frontend
    - Saves file to server storage
    - Creates invoice record in database
    """
    try:
        # Parse months from JSON string to list
        try:
            months_list = json.loads(months)
            # Convert to string format for database (as per your model)
            months_str = ", ".join([date.fromisoformat(month).strftime("%B %Y") for month in months_list])
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(status_code=400, detail=f"Invalid months format: {str(e)}")

        # Create uploads directory if it doesn't exist
        upload_dir = "uploads/invoices"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate filename and path
        file_extension = ".pdf"  # Force PDF extension
        filename = f"{invoice_number}{file_extension}"
        file_path = os.path.join(upload_dir, filename)
        
        # Save the uploaded PDF file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Save to DB (matching your existing Invoice model)
        new_invoice = Invoice(
            invoice_number=invoice_number,
            client_id=client_id,
            months=months_str,  # Store as string like "January 2025, February 2025"
            created_date=date.today(),
            file_path=file_path
        )
        db.add(new_invoice)
        db.commit()
        db.refresh(new_invoice)

        return new_invoice

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating invoice: {str(e)}")

# --- Keep existing endpoints unchanged ---
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