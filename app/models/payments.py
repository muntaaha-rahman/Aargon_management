from sqlalchemy import (
    Column, String, Integer, Enum, ForeignKey, Date, Text, DateTime, Boolean, Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.models.base import Base
from app.models.auth import UserRole

class PaymentMethod(str, enum.Enum):
    cash = "Cash"
    bank_transfer = "Bank Transfer"
    bkash = "Bkash"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, default=func.current_date())
    received_amount = Column(Float, nullable=False)
    discount = Column(Float, nullable=True)  # percentage
    method = Column(Enum(PaymentMethod), nullable=False)
    description = Column(String(500), nullable=True)
    
    # Foreign key to client (users with client role)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Foreign key to received_by (users with admin/moderator role)
    received_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    client = relationship("User", foreign_keys=[client_id], back_populates="payments")
    received_by = relationship("User", foreign_keys=[received_by_id])