from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class InstitutionBase(BaseModel):
    id: int
    full_name: str
    short_name: str
    country: str
    region: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    city: str | None = None
    address: str | None = None
    date_added: date
    date_removed: date | None = None
    is_active: bool

    class Config:
        from_attributes = True


class MemberBaseSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    orcid: str | None = None
    preferred_author_name: str | None = None
    date_joined: date
    date_left: date | None = None
    is_active: bool

    class Config:
        from_attributes = True


class MemberResponse(MemberBaseSchema):
    id: int
    institution_id: int
    institution: Optional[InstitutionBase] = None


# Properties to receive via API on creation
class InstitutionCreate(InstitutionBase):
    pass


# Properties to receive via API on update
class InstitutionUpdate(InstitutionBase):
    full_name: Optional[str] = None
    short_name: Optional[str] = None
    country: Optional[str] = None
    is_active: Optional[bool] = None
    date_removed: Optional[date] = None


# Properties to return via API
class InstitutionResponse(InstitutionBase):
    id: int
    date_added: date
    date_removed: Optional[date] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
