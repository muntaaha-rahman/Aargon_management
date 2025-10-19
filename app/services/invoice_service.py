from app.models.invoice import Invoice
from app.utils.invoice_pdf import generate_invoice_pdf
from app.db.session import SessionLocal
from datetime import date
import uuid

def create_invoice(db, client_id: int, client_name: str, client_address: str, months: str):
    # Generate unique invoice number
    invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"  # e.g., INV-1A2B3C4D

    # Generate PDF
    file_path = generate_invoice_pdf(invoice_number, client_name, client_address, months)

    # Save to DB
    new_invoice = Invoice(
        invoice_number=invoice_number,
        client_id=client_id,
        months=months,
        created_date=date.today(),
        file_path=file_path
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    return new_invoice
