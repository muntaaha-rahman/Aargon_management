from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.security import (
    hash_password, 
    verify_password, 
    create_access_token, 
    create_refresh_token,
    revoke_token,
    verify_token,
    credentials_exception
)
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, UserOut

class AuthService:
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> UserOut:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = hash_password(user_data.password)
        user = User(
            name=user_data.full_name,
            email=user_data.email,
            password=hashed_password,
            role=user_data.role
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return UserOut.from_orm(user)
    
    @staticmethod
    def login_user(db: Session, login_data: UserLogin):
        # Find user by email
        user = db.query(User).filter(User.email == login_data.email).first()
        if not user or not verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Create tokens using your existing functions
        token_data = {"sub": user.email}
        access_token, access_jti, access_expires = create_access_token(token_data)
        refresh_token, refresh_jti, refresh_expires = create_refresh_token(token_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": UserOut.from_orm(user)
        }
    
    @staticmethod
    def logout_user(token_jti: str):
        # Use your existing revoke_token function
        revoke_token(token_jti, expires_in=60)
        return {"message": "Successfully logged out"}
    
    @staticmethod
    def get_current_user(db: Session, token: str):
        # Use your existing verify_token function
        token_data = verify_token(token, credentials_exception)
        user = db.query(User).filter(User.email == token_data.username).first()
        if not user:
            raise credentials_exception
        return UserOut.from_orm(user)