from __future__ import annotations # Add this line at the very top
from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field



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
    entityid: str
    rorid: Optional[str] = None


class InstitutionCreate(InstitutionBase):
    pass


class InstitutionUpdate(BaseModel):
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
    rorid: Optional[str] = None
