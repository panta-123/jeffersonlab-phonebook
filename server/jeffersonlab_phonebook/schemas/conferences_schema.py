from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ConferenceBase(BaseModel):
    name: str
    location: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    url: Optional[str] = None

class ConferenceCreate(ConferenceBase):
    pass

class ConferenceUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    url: Optional[str] = None
