from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, oauth2_scheme
from app.schemas.auth import UserCreate, UserLogin
from app.services.auth import AuthService

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return AuthService.register_user(db, user_data)

@router.post("/login")
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    return AuthService.login_user(db, login_data)

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    from jose import jwt
    from app.core.settings import settings
    
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    jti = payload.get("jti")
    
    if jti:
        AuthService.logout_user(jti)
    
    return {"message": "Successfully logged out"}

@router.get("/me")
async def get_current_user_info(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_info = AuthService.get_current_user(db, token)
    return {"user": user_info}