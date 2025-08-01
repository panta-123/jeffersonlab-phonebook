from typing import Optional

from pydantic import BaseModel, EmailStr

class AuthStatus(BaseModel):
    authenticated: bool
    isAdmin: bool
    email: EmailStr
    name: str

class ErrorDetail(BaseModel):
    detail: str
    code: Optional[str] = None
