from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.auth import User
from app.schemas.payments import (
    PaymentCreate, PaymentResponse, PaymentUpdate, 
    PaymentStatsResponse
)
from app.services.payments import PaymentService

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=PaymentResponse)
def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PaymentService.create_payment(db, payment_data, current_user)

@router.get("/", response_model=List[PaymentResponse])
def get_payments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PaymentService.get_payments(db, skip, limit)

@router.get("/stats", response_model=PaymentStatsResponse)
def get_payment_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PaymentService.get_payment_stats(db)

@router.get("/client/{client_id}", response_model=List[PaymentResponse])
def get_payments_by_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PaymentService.get_payments_by_client(db, client_id)

@router.get("/date-range", response_model=List[PaymentResponse])
def get_payments_by_date_range(
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PaymentService.get_payments_by_date_range(db, start_date, end_date)

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payment = PaymentService.get_payment_by_id(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(
    payment_id: int,
    payment_data: PaymentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PaymentService.update_payment(db, payment_id, payment_data, current_user)

@router.delete("/{payment_id}")
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return PaymentService.delete_payment(db, payment_id, current_user)