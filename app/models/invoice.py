from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from app.models.base import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True, nullable=False)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    months = Column(String, nullable=False)  # e.g. "January 2025, February 2025"
    created_date = Column(Date, default=date.today)
    file_path = Column(String, nullable=True)  # e.g. "invoices/invoice_001.pdf"

    client = relationship("User", back_populates="invoices")
