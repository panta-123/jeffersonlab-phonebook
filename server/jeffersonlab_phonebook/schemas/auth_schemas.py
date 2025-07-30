from typing import Optional

from pydantic import BaseModel, EmailStr

class AuthStatus(BaseModel):
    authenticated: bool
    isAdmin: bool
    email: Optional[EmailStr] = None
    name: Optional[str]= None

class ErrorDetail(BaseModel):
    detail: str
    code: Optional[str] = None
