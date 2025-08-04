# File: jeffersonlab_phonebook/repositories/institutionboard_repository.py

from datetime import date
from typing import List, Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

# Import the SQLAlchemy model
from jeffersonlab_phonebook.db.models import InstitutionalBoardMember

# Import the BoardType enum
from jeffersonlab_phonebook.db.constants import BoardType

# Import Pydantic schemas (for method arguments, not return types)
from jeffersonlab_phonebook.schemas.board_schemas import (
    InstitutionalBoardMemberCreate,
    InstitutionalBoardMemberUpdate,
)

class InstitutionalBoardMemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ibm_id: int) -> Optional[InstitutionalBoardMember]:
        query = select(InstitutionalBoardMember).where(
            InstitutionalBoardMember.id == ibm_id
        ).options(
            joinedload(InstitutionalBoardMember.member),
            joinedload(InstitutionalBoardMember.institution),
            joinedload(InstitutionalBoardMember.role)
        )
        db_ibm = self.db.scalar(query)
        return db_ibm

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        board_type: Optional[BoardType] = None,
        member_id: Optional[int] = None,
        institution_id: Optional[int] = None,
    ) -> Sequence[InstitutionalBoardMember]:
        query = select(InstitutionalBoardMember).options(
            joinedload(InstitutionalBoardMember.member),
            joinedload(InstitutionalBoardMember.institution),
            joinedload(InstitutionalBoardMember.role),
        )

        if board_type:
            query = query.where(InstitutionalBoardMember.board_type == board_type)
        if member_id:
            query = query.where(InstitutionalBoardMember.member_id == member_id)
        if institution_id:
            query = query.where(
                InstitutionalBoardMember.institution_id == institution_id
            )

        db_ibms = self.db.scalars(query.offset(skip).limit(limit)).all()
        return db_ibms

    def create(self, ibm_in: InstitutionalBoardMemberCreate) -> InstitutionalBoardMember:
        db_ibm = InstitutionalBoardMember(**ibm_in.model_dump())
        self.db.add(db_ibm)
        self.db.commit()
        self.db.refresh(db_ibm)
        return db_ibm

    def update(
        self, db_ibm: InstitutionalBoardMember, ibm_in: InstitutionalBoardMemberUpdate
    ) -> InstitutionalBoardMember:
        update_data = ibm_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_ibm, key, value)
        self.db.add(db_ibm)
        self.db.commit()
        self.db.refresh(db_ibm)
        return db_ibm

    def delete(self, ibm_id: int) -> bool:
        ibm = self.db.get(InstitutionalBoardMember, ibm_id)
        if ibm:
            self.db.delete(ibm)
            self.db.commit()
            return True
        return False