from typing import Optional, List

from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: Optional[bool] = None
    db_connections: Optional[List[str]] = None

class UserInDB(User):
    hashed_password: bytes

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []
    