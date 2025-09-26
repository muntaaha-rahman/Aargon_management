from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.auth import User, UserRole

class ClientService:
    @staticmethod
    def create_client(db: Session, client_data, current_user):
        if current_user.role not in [UserRole.superadmin, UserRole.admin]:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        existing_user = db.query(User).filter(User.email == client_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email exists")
        
        client = User(
            name=client_data.name,
            email=client_data.email,
            password=client_data.password,  # Make sure to hash this password
            role=UserRole.client,
            active=True,
            contact_person=client_data.contact_person,
            phone=client_data.phone
        )
        db.add(client)
        db.commit()
        db.refresh(client)
        return client

    @staticmethod
    def get_clients(db: Session, current_user, skip: int = 0, limit: int = 100):
        if current_user.role not in [UserRole.superadmin, UserRole.admin]:
            raise HTTPException(status_code=403, detail="Not authorized")
        return db.query(User).filter(User.role == UserRole.client).offset(skip).limit(limit).all()

    @staticmethod
    def update_client_status(db: Session, client_id: int, active: bool, current_user):
        if current_user.role not in [UserRole.superadmin, UserRole.admin]:
            raise HTTPException(status_code=403, detail="Not authorized")
        
        client = db.query(User).filter(User.id == client_id, User.role == UserRole.client).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        client.active = active
        db.commit()
        db.refresh(client)
        return client