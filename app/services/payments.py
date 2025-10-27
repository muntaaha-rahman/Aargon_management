from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date, datetime
from typing import List, Optional
from sqlalchemy import func

from app.models.payments import Payment, PaymentMethod
from app.models.auth import User, UserRole

class PaymentService:
    @staticmethod
    def create_payment(db: Session, payment_data, current_user: User):
        # Validate client exists and has client role
        client = db.query(User).filter(
            User.id == payment_data.client_id,
            User.role == UserRole.client
        ).first()
        if not client:
            raise HTTPException(
                status_code=404, 
                detail="Client not found or user is not a client"
            )
        
        # Validate received_by user exists and has appropriate role
        if current_user.role not in [UserRole.superadmin, UserRole.admin, UserRole.manager]:
            raise HTTPException(
                status_code=403,
                detail="Only admin, superadmin or manager can receive payments"
            )

        payment = Payment(
            date=payment_data.date,
            received_amount=payment_data.received_amount,
            discount=payment_data.discount,
            method=payment_data.method,
            description=payment_data.description,
            client_id=payment_data.client_id,
            received_by_id=current_user.id
        )
        
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def get_payments(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Payment).offset(skip).limit(limit).all()

    @staticmethod
    def get_payment_by_id(db: Session, payment_id: int):
        return db.query(Payment).filter(Payment.id == payment_id).first()

    @staticmethod
    def update_payment(db: Session, payment_id: int, payment_data, current_user: User):
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        # Validate user has permission to update
        if current_user.role not in [UserRole.superadmin, UserRole.admin]:
            raise HTTPException(
                status_code=403,
                detail="Only admin or superadmin can update payments"
            )

        update_data = payment_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(payment, field, value)
        
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def delete_payment(db: Session, payment_id: int, current_user: User):
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        # Validate user has permission to delete
        if current_user.role not in [UserRole.superadmin, UserRole.admin]:
            raise HTTPException(
                status_code=403,
                detail="Only admin or superadmin can delete payments"
            )
        
        db.delete(payment)
        db.commit()
        return {"message": "Payment deleted successfully"}

    @staticmethod
    def get_payments_by_client(db: Session, client_id: int):
        # Validate client exists
        client = db.query(User).filter(
            User.id == client_id,
            User.role == UserRole.client
        ).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        return db.query(Payment).filter(Payment.client_id == client_id).all()

    @staticmethod
    def get_payments_by_date_range(db: Session, start_date: date, end_date: date):
        return db.query(Payment).filter(
            Payment.date >= start_date,
            Payment.date <= end_date
        ).all()

    @staticmethod
    def get_payment_stats(db: Session):
        # Overall stats
        overall_stats = db.query(
            func.sum(Payment.received_amount).label('total_received'),
            func.sum(Payment.discount).label('total_discount'),
            func.count(Payment.id).label('payment_count')
        ).first()

        # Stats by client
        client_stats = db.query(
            Payment.client_id,
            User.name.label('client_name'),
            func.sum(Payment.received_amount).label('total_received'),
            func.sum(Payment.discount).label('total_discount'),
            func.count(Payment.id).label('payment_count')
        ).join(User, Payment.client_id == User.id)\
         .group_by(Payment.client_id, User.name)\
         .all()

        # Stats by payment method
        method_stats = db.query(
            Payment.method,
            func.sum(Payment.received_amount).label('total_received'),
            func.count(Payment.id).label('payment_count')
        ).group_by(Payment.method).all()

        # Format response
        overall_summary = {
            "total_received": float(overall_stats.total_received or 0),
            "total_discount": float(overall_stats.total_discount or 0),
            "payment_count": overall_stats.payment_count or 0
        }

        client_summaries = []
        for stat in client_stats:
            client_summaries.append({
                "client_id": stat.client_id,
                "client_name": stat.client_name,
                "total_received": float(stat.total_received or 0),
                "total_discount": float(stat.total_discount or 0),
                "payment_count": stat.payment_count or 0
            })

        method_summary = {}
        for stat in method_stats:
            method_summary[stat.method.value] = {
                "total_received": float(stat.total_received or 0),
                "payment_count": stat.payment_count or 0
            }

        return {
            "overall": overall_summary,
            "by_client": client_summaries,
            "by_method": method_summary
        }