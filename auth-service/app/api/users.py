from typing import List
from datetime import timedelta
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
import bcrypt

from app.api.models import User, UserInDB, Token
from app.api import db_manager
from app.api import db
from app.api import utils

users = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)

# Register new user account
@users.post("/register", status_code = 201)
async def register_user_account(payload: UserInDB):
    passwd = payload.hashed_password.decode('utf-8')
    hashed_password = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
    db_user = payload.dict()
    db_user["hashed_password"]= str(hashed_password)
    
    user_id = await db_manager.add_user(db_user)
    response = {
        'id': user_id,
        **db_user
    }

    return response

# Login with username and password
@users.post("/login", response_model = Token)
async def authenticate_user_with_credentials(username: str, password: str):
    db_user_info = await db_manager.get_user_by_name(username)
    if not db_user_info:
        raise HTTPException(status_code = 404, detail=f"User with provided username: {username} does not exist")

    db_user = UserInDB(**db_user_info)
    hashed = db_user.hashed_password[2:-1]
    if bcrypt.checkpw(password.encode('utf-8'), hashed):
        access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = utils.create_access_token(
            data={"sub": db_user.username, "scopes": ["me", "items"]},
            expires_delta=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code = 404, detail = "We have no user mathing these credentials")

# Get currently logged in user's profile and it's items (for now placeholder list)
@users.get("/users/me/items")
async def get_items(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    curr_user = await utils.get_current_user(security_scopes, token)
    if not curr_user:
        raise HTTPException(detail = "Invalid token")
    
    response = {
        'user': UserInDB(**curr_user),
        'items': [{"item_id": "Foo", "owner": UserInDB(**curr_user).username}]
    }
    return response

# Check system status
@users.get("/status")
async def read_system_status(current_user: User = Depends(utils.get_current_user)):
    return {"status": "ok"}

    