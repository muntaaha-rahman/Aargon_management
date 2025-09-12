from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    revoke_token,
    get_current_user,
)
from app.core.database import get_db
from app.auth.models import User


# Authenticate user
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        return None
    return user


# Login service
def login_service(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # access token
    access_token, access_jti, access_exp = create_access_token({"sub": user.username})
    # refresh token
    refresh_token, refresh_jti, refresh_exp = create_refresh_token({"sub": user.username})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# Refresh token service
def refresh_token_service(refresh_token: str):
    from jose import jwt
    from app.core.security import SECRET_KEY, ALGORITHM, credentials_exception

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        jti = payload.get("jti")
        exp = payload.get("exp")

        if not username or not jti:
            raise credentials_exception

        # revoke old refresh token
        expires_in = int(exp - (datetime.utcnow().timestamp()))
        revoke_token(jti, expires_in)

        # issue new access + refresh
        new_access_token, _, _ = create_access_token({"sub": username})
        new_refresh_token, _, _ = create_refresh_token({"sub": username})

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }
    except Exception:
        raise credentials_exception


# Logout service (revoke both tokens)
def logout_service(token: str = Depends(get_current_user)):
    from jose import jwt
    from app.core.security import SECRET_KEY, ALGORITHM

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    jti = payload.get("jti")
    exp = payload.get("exp")

    expires_in = int(exp - (datetime.utcnow().timestamp()))
    revoke_token(jti, expires_in)

    return {"msg": "Successfully logged out"}
