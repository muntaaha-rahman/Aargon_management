from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.auth import User
from app.schemas.services import ServiceCreate, ServiceResponse, ServiceUpdate, ServiceActiveUpdate
from app.services.services import ServiceService

router = APIRouter(prefix="/services", tags=["services"])

@router.post("/", response_model=ServiceResponse)
def create_service(
    service_data: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ServiceService.create_service(db, service_data, current_user)

@router.get("/", response_model=List[ServiceResponse])
def get_services(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ServiceService.get_services(db, skip, limit)

@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ServiceService.get_service_by_id(db, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.put("/{service_id}", response_model=ServiceResponse)
def update_service(
    service_id: int,
    service_data: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ServiceService.update_service(db, service_id, service_data, current_user)

@router.delete("/{service_id}")
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ServiceService.delete_service(db, service_id, current_user)

@router.patch("/{service_id}/active", response_model=ServiceResponse)
def update_service_active(
    service_id: int,
    active_data: ServiceActiveUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ServiceService.update_service_active(db, service_id, active_data.active, current_user)