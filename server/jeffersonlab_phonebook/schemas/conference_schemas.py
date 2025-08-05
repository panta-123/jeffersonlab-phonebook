from typing import Optional, List
from datetime import date

from pydantic import BaseModel, ConfigDict



class TalkBase(BaseModel):
    title: str
    start_date: date
    end_date: Optional[date] = None
    docdb_id: Optional[str] = None
    talk_link: Optional[str] = None


class TalkCreate(TalkBase):
    conference_id: int


class TalkUpdate(TalkBase):
    conference_id: Optional[int] = None


class ConferenceBase(BaseModel):
    name: str
    location: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    url: Optional[str] = None


class ConferenceCreate(ConferenceBase):
    pass


class ConferenceUpdate(ConferenceBase):
    pass



class TalkAssignmentBase(BaseModel):
    talk_id: int
    member_id: int
    role_id: int
    assigned_by_id: Optional[int] = None

class TalkAssignmentCreate(TalkAssignmentBase):
    pass

class TalkAssignmentUpdate(BaseModel):
    talk_id: Optional[int] = None
    member_id: Optional[int] = None
    role_id: Optional[int] = None
    assigned_by_id: Optional[int] = None




