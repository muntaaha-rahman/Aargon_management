import uuid
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from .settings import settings
from .redis_client import store_revoked_token, is_token_revoked

# Environment variables
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class TokenData(BaseModel):
    username: Optional[str] = None

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_token(data: dict, expires_delta: timedelta) -> tuple[str, str, datetime]:
    to_encode = data.copy()
    jti = str(uuid.uuid4())
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"jti": jti, "exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, jti, expire

def create_access_token(data: dict) -> tuple[str, str, datetime]:
    return create_token(data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(data: dict) -> tuple[str, str, datetime]:
    return create_token(data, timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))

def revoke_token(jti: str, expires_in: int):
    store_revoked_token(jti, timedelta(minutes=expires_in))

def verify_token(token: str, credentials_exception) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        jti = payload.get("jti")

        if not username or not jti or is_token_revoked(jti):
            raise credentials_exception

        return TokenData(username=username)
    except JWTError:
        raise credentials_exception

# Exception
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    return verify_token(token, credentials_exception)