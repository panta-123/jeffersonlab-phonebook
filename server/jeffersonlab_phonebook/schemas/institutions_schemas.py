from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# Base Schema
class InstitutionBase(BaseModel):
    """Base schema for Institution, includes all common fields."""

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
    entityid: str  # Added from SQLAlchemy model
    rorid: Optional[str] = None # Added from SQLAlchemy model, now Optional

# Create Schema
class InstitutionCreate(InstitutionBase):
    """Schema for creating a new Institution."""
    # When creating, 'entityid' and 'rorid' might be auto-generated or optional depending on your logic.
    # For now, keeping them as required based on InstitutionBase.
    pass

# Update Schema
class InstitutionUpdate(BaseModel):
    """Schema for updating an existing Institution, all fields are optional."""

    full_name: Optional[str] = Field(None, max_length=50)
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
    rorid: Optional[str] = None # Made optional for updates

# Response Schema
class InstitutionResponse(InstitutionBase):
    """Schema for returning Institution data, includes the ID."""

    id: int

    model_config = ConfigDict(from_attributes=True)