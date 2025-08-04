from datetime import date
from typing import Any, Optional

from pydantic import BaseModel, Field

class MemberBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    orcid: Optional[str] = None
    preferred_author_name: Optional[str] = None
    institution_id: int
    date_joined: date
    date_left: Optional[date] = None
    is_active: bool = True
    experimental_data: Optional[dict[str, Any]] = None


class MemberCreate(MemberBase):
    pass


class MemberUpdate(MemberBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    orcid: Optional[str] = None
    preferred_author_name: Optional[str] = None
    institution_id: Optional[int] = None
    date_joined: Optional[date] = None
    date_left: Optional[date] = None
    is_active: Optional[bool] = None
    experimental_data: Optional[dict[str, Any]] = None
