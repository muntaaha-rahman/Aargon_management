from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.services import Service
from app.models.auth import User

class ServiceService:
    @staticmethod
    def create_service(db: Session, service_data, current_user: User):
        # Check if service name already exists
        existing_service = db.query(Service).filter(Service.name == service_data.name).first()
        if existing_service:
            raise HTTPException(status_code=400, detail="Service name already exists")
        
        service = Service(
            name=service_data.name,
            created_by=current_user.username,
            active=True
        )
        db.add(service)
        db.commit()
        db.refresh(service)
        return service

    @staticmethod
    def get_services(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Service).offset(skip).limit(limit).all()

    @staticmethod
    def get_service_by_id(db: Session, service_id: int):
        return db.query(Service).filter(Service.id == service_id).first()

    @staticmethod
    def update_service(db: Session, service_id: int, service_data, current_user: User):
        service = db.query(Service).filter(Service.id == service_id).first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        if service_data.name is not None:
            # Check if new name already exists (excluding current service)
            existing_service = db.query(Service).filter(
                Service.name == service_data.name, 
                Service.id != service_id
            ).first()
            if existing_service:
                raise HTTPException(status_code=400, detail="Service name already exists")
            service.name = service_data.name
        
        if service_data.active is not None:
            service.active = service_data.active
        
        db.commit()
        db.refresh(service)
        return service

    @staticmethod
    def delete_service(db: Session, service_id: int, current_user: User):
        service = db.query(Service).filter(Service.id == service_id).first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        db.delete(service)
        db.commit()
        return {"message": "Service deleted successfully"}
    
    @staticmethod
    def update_service_active(db: Session, service_id: int, active: bool, current_user: User):
        service = db.query(Service).filter(Service.id == service_id).first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        service.active = active
        db.commit()
        db.refresh(service)
        return service
