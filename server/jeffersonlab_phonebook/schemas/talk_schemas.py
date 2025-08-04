from datetime import date
from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict, Field



# --- Talk Schemas ---
class TalkBase(BaseModel):
    title: str
    dodb_id: Optional[str] = None
    talk_link: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    conference_id: Optional[int] = None

class TalkCreate(TalkBase):
    pass

class TalkUpdate(BaseModel):
    title: Optional[str] = None
    dodb_id: Optional[str] = None
    talk_link: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    conference_id: Optional[int] = None


# --- Conference Schemas ---
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



# --- TalkAssignment Schemas ---
class TalkAssignmentBase(BaseModel):
    talk_id: int
    member_id: int
    role_id: int
    assigned_by_id: Optional[int] = None
    assignment_date: date

class TalkAssignmentCreate(TalkAssignmentBase):
    pass

class TalkAssignmentUpdate(BaseModel):
    talk_id: Optional[int] = None
    member_id: Optional[int] = None
    role_id: Optional[int] = None
    assigned_by_id: Optional[int] = None
    assignment_date: Optional[date] = None

