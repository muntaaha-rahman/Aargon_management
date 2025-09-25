from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user, verify_token, credentials_exception, oauth2_scheme 
from app.models.auth import User
from app.schemas.clients import ClientCreate, ClientResponse, ClientStatusUpdate
from app.services.clients import ClientService

router = APIRouter(prefix="/clients", tags=["clients"])

def get_current_active_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Get full user object from token"""
    token_data = verify_token(token, credentials_exception)
    
    # Get user from database using email from token
    user = db.query(User).filter(User.email == token_data.username).first()
    if not user:
        raise credentials_exception
    
    return user

@router.post("/", response_model=ClientResponse)
def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)  # Use the new function
):
    return ClientService.create_client(db, client_data, current_user)

# Update other endpoints to use get_current_active_user too
@router.get("/", response_model=List[ClientResponse])
def get_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return ClientService.get_clients(db, current_user, skip, limit)

@router.patch("/{client_id}/status", response_model=ClientResponse)
def update_client_status(
    client_id: int,
    status_data: ClientStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return ClientService.update_client_status(db, client_id, status_data.active, current_user)