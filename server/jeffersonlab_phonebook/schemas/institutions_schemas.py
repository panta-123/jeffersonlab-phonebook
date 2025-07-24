from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# Base Schema
class InstitutionBase(BaseModel):
    full_name: str = Field(..., max_length=50)
    short_name: str
    country: str
    region: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    address: Optional[str] = None
    date_added: date
    date_removed: Optional[date] = None
    is_active: bool = True

# Create Schema
class InstitutionCreate(InstitutionBase):
    pass

# Update Schema
class InstitutionUpdate(InstitutionBase):
    full_name: Optional[str] = None
    short_name: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = None
    address: Optional[str] = None
    date_added: Optional[date] = None
    date_removed: Optional[date] = None
    is_active: Optional[bool] = None

# Response Schema
class InstitutionResponse(InstitutionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)