from datetime import datetime, timedelta
import jwt
from jwt import PyJWTError
from pydantic import ValidationError
from typing import Optional

from fastapi import HTTPException, status, Depends
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)

from app.api import db_manager
from app.api.models import TokenData, Token, User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)


# to generate a random SECRET_KEY run:
# openssl rand -hex 32
SECRET_KEY = "7a7bdc5e25667a6aedf03f906ccbad2ea388630f052ad47aea37a76e2247d352"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code = 401, detail = "Could not validate credentials")
    token_scopes = payload.get("scopes")
    token_data = TokenData(scopes=token_scopes, username=username)

    User = await db_manager.get_user_by_name(username)

    return User
    
