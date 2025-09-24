from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import jwt

from app.core.security import (
    hash_password, 
    verify_password, 
    create_access_token, 
    create_refresh_token,
    revoke_token
)
from app.core.settings import settings
from app.models.auth import User  # Fixed import - should be user, not auth
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
        
        # Create tokens
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
        revoke_token(token_jti, expires_in=60)
        return {"message": "Successfully logged out"}
    
    @staticmethod  # Fixed indentation - this was outside the class!
    def get_current_user(db: Session, token: str):
        try:
            # Decode token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email = payload.get("sub")
            
            if not email:
                raise HTTPException(status_code=401, detail="Invalid token")
            
            # Find user in database
            user = db.query(User).filter(User.email == email).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
                
            return UserOut.from_orm(user)
            
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")