from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, Float, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_by = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    assignments = relationship("ServiceAssignment", back_populates="service")

class ServiceAssignment(Base):
    __tablename__ = "service_assignments"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    service_start_month = Column(Date, nullable=False)
    billing_start_date = Column(Date, nullable=False)
    service_stop_date = Column(Date, nullable=True)  # NEW FIELD - can be null
    status = Column(Boolean, default=True, nullable=False)
    
    # Individual flexible fields
    description = Column(String(255), nullable=False)
    link_capacity = Column(String(100), nullable=False)
    rate = Column(Float, nullable=True)
    
    created_by = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    client = relationship("User", foreign_keys=[client_id], back_populates="service_assignments")
    service = relationship("Service", foreign_keys=[service_id], back_populates="assignments")