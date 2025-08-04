from datetime import date
from typing import Optional

from pydantic import BaseModel

# We need to import the BoardType enum
from jeffersonlab_phonebook.db.constants import BoardType

class InstitutionalBoardMemberBase(BaseModel):
    member_id: int
    institution_id: int
    board_type: BoardType
    role_id: int
    start_date: date
    end_date: Optional[date] = None

class InstitutionalBoardMemberCreate(InstitutionalBoardMemberBase):
    pass

class InstitutionalBoardMemberUpdate(BaseModel):
    member_id: Optional[int] = None
    institution_id: Optional[int] = None
    board_type: Optional[BoardType] = None
    role_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


