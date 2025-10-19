from sqlalchemy.orm import Session
from datetime import date
from models.invoice import Invoice
from schemas.invoice import InvoiceCreate

def generate_invoice_number(db: Session) -> str:
    """Generates a unique invoice number like INV-20251019-001"""
    today_str = date.today().strftime("%Y%m%d")
    count_today = db.query(Invoice).filter(Invoice.created_date == date.today()).count() + 1
    return f"INV-{today_str}-{count_today:03d}"


def create_invoice(db: Session, invoice_data: InvoiceCreate):
    """Create a new invoice and auto-generate invoice number"""
    invoice_number = generate_invoice_number(db)

    new_invoice = Invoice(
        client_id=invoice_data.client_id,
        months=invoice_data.months,
        file_path=invoice_data.file_path,
        invoice_number=invoice_number,
        created_date=date.today()
    )

    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice


def get_invoices(db: Session):
    """Fetch all invoices"""
    return db.query(Invoice).order_by(Invoice.created_date.desc()).all()


def get_invoice_by_id(db: Session, invoice_id: int):
    """Fetch single invoice by ID"""
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()
