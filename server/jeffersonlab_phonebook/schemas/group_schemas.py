from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import date

class GroupBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    is_active: bool = True

class GroupCreate(GroupBase):
    date_created: date = date.today()
    # This is the corrected line.
    # A top-level group has no parent, so the value should be None (NULL).
    parent_group_id: Optional[int] = None

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    parent_group_id: Optional[int] = None


# --- GroupMember Schemas ---
class GroupMemberBase(BaseModel):
    group_id: int
    member_id: int
    role_id: int
    start_date: date
    end_date: Optional[date] = None

class GroupMemberCreate(GroupMemberBase):
    pass

class GroupMemberUpdate(BaseModel):
    role_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

