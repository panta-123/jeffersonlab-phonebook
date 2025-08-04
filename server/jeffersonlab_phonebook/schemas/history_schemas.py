from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

# Base Schema for the history table
class MemberInstitutionHistoryBase(BaseModel):
    member_id: int
    institution_id: int
    start_date: date
    end_date: Optional[date] = None

# Create Schema
class MemberInstitutionHistoryCreate(MemberInstitutionHistoryBase):
    pass

# Update Schema
class MemberInstitutionHistoryUpdate(MemberInstitutionHistoryBase):
    member_id: Optional[int] = None
    institution_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
