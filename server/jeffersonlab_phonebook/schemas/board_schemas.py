from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

# We need to import the BoardType enum
from jeffersonlab_phonebook.db.constants import BoardType

# Base Schema for the associative table
class InstitutionalBoardMemberBase(BaseModel):
    member_id: int
    institution_id: int
    board_type: BoardType
    role: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    is_chair: bool = False

# Create Schema
class InstitutionalBoardMemberCreate(InstitutionalBoardMemberBase):
    pass

# Update Schema
class InstitutionalBoardMemberUpdate(InstitutionalBoardMemberBase):
    member_id: Optional[int] = None
    institution_id: Optional[int] = None
    board_type: Optional[BoardType] = None
    role: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_chair: Optional[bool] = None

# Response Schema
class InstitutionalBoardMemberResponse(InstitutionalBoardMemberBase):
    id: int

    model_config = ConfigDict(from_attributes=True)