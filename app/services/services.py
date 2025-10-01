from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from app.models.services import Service, ServiceAssignment
from app.models.auth import User

class ServiceService:
    @staticmethod
    def create_service(db: Session, service_data, current_user: User):
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

class ServiceAssignmentService:
    @staticmethod
    def create_service_assignment(db: Session, assignment_data, current_user: User):
        assignment = ServiceAssignment(
            client_id=assignment_data.client_id,
            service_id=assignment_data.service_id,
            service_start_month=assignment_data.service_start_month,
            billing_start_date=assignment_data.billing_start_date,
            description=assignment_data.description,
            link_capacity=assignment_data.link_capacity,
            rate=assignment_data.rate,
            status=True,
            created_by=current_user.username
        )
        
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        return assignment

    @staticmethod
    def get_service_assignments(db: Session, skip: int = 0, limit: int = 100):
        return db.query(ServiceAssignment).offset(skip).limit(limit).all()

    @staticmethod
    def get_service_assignment_by_id(db: Session, assignment_id: int):
        return db.query(ServiceAssignment).filter(ServiceAssignment.id == assignment_id).first()

    @staticmethod
    def update_service_assignment_status(db: Session, assignment_id: int, status: bool, current_user: User):
        assignment = db.query(ServiceAssignment).filter(ServiceAssignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(status_code=404, detail="Service assignment not found")
        
        assignment.status = status
        
        # Set service_stop_date when stopping the service
        if status == False and assignment.service_stop_date is None:
            assignment.service_stop_date = datetime.now().date()
        
        db.commit()
        db.refresh(assignment)
        return assignment