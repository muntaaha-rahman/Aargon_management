from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import os
from datetime import date

INVOICE_DIR = "app/invoices"

# Ensure folder exists
os.makedirs(INVOICE_DIR, exist_ok=True)

def generate_invoice_pdf(invoice_number: str, client_name: str, client_address: str, months: str):
    """Generate and save a simple PDF invoice."""
    file_path = os.path.join(INVOICE_DIR, f"{invoice_number}.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(30 * mm, height - 30 * mm, "Aargon Management")

    c.setFont("Helvetica", 12)
    c.drawString(30 * mm, height - 40 * mm, "Invoice")
    c.drawString(30 * mm, height - 50 * mm, f"Invoice Number: {invoice_number}")
    c.drawString(30 * mm, height - 60 * mm, f"Invoice Date: {date.today().strftime('%d %B %Y')}")

    # Client info
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30 * mm, height - 80 * mm, "Bill To:")
    c.setFont("Helvetica", 12)
    c.drawString(30 * mm, height - 90 * mm, client_name)
    c.drawString(30 * mm, height - 100 * mm, client_address)

    # Invoice content
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30 * mm, height - 120 * mm, "Billing Period:")
    c.setFont("Helvetica", 12)
    c.drawString(30 * mm, height - 130 * mm, months)

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(30 * mm, 20 * mm, "Thank you for your business.")

    c.showPage()
    c.save()

    return file_path
