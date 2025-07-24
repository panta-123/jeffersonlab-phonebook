from datetime import date
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from jeffersonlab_phonebook.schemas.institutions_schemas import InstitutionResponse

# Base Schema
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

# Create Schema
class MemberCreate(MemberBase):
    pass

# Update Schema
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

# Response Schema
class MemberResponse(MemberBase):
    id: int
    # Include a nested schema for the institution relationship
    institution: Optional[InstitutionResponse] = None

    model_config = ConfigDict(from_attributes=True)