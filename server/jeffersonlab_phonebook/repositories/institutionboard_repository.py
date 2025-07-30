from datetime import date
from typing import List, Optional

from sqlalchemy import select, or_
from sqlalchemy.orm import Session, joinedload # Added joinedload

# Import the SQLAlchemy model
from jeffersonlab_phonebook.db.models import InstitutionalBoardMember # Corrected import

# Import the BoardType enum
from jeffersonlab_phonebook.db.constants import BoardType

# Import Pydantic schemas
from jeffersonlab_phonebook.schemas.board_schemas import (
    InstitutionalBoardMemberCreate,
    InstitutionalBoardMemberUpdate, # Added for update method
    InstitutionalBoardMemberResponse,
)

class InstitutionalBoardMemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, ibm_id: int) -> Optional[InstitutionalBoardMemberResponse]:
        """
        Retrieves a single institutional board member entry by its ID and converts it to a response schema.
        """
        db_ibm = self.db.get(InstitutionalBoardMember, ibm_id) # Corrected to use SQLAlchemy model
        if db_ibm:
            return InstitutionalBoardMemberResponse.model_validate(db_ibm)
        return None

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        board_type: Optional[BoardType] = None,
        member_id: Optional[int] = None,
        institution_id: Optional[int] = None,
    ) -> List[InstitutionalBoardMemberResponse]:
        """
        Retrieves all institutional board member entries from the database with pagination
        and optional filtering, then converts them to response schemas.
        Includes eager loading of 'member' and 'institution' relationships for full response data.
        """
        query = select(InstitutionalBoardMember).options(
            joinedload(InstitutionalBoardMember.member),
            joinedload(InstitutionalBoardMember.institution),
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
        return [InstitutionalBoardMemberResponse.model_validate(ibm) for ibm in db_ibms]


    def create(
        self,
        ibm_in: InstitutionalBoardMemberCreate # Accepts the Pydantic Create schema
    ) -> InstitutionalBoardMemberResponse: # Returns the Pydantic Response schema
        """
        Creates a new institutional board member entry from the provided schema.
        Can be used for both Institutional and Executive Board members.
        """
        db_ibm = InstitutionalBoardMember(**ibm_in.model_dump())
        self.db.add(db_ibm)
        self.db.commit()
        self.db.refresh(db_ibm)
        return InstitutionalBoardMemberResponse.model_validate(db_ibm)

    def update(
        self,
        db_ibm: InstitutionalBoardMember, # Still takes the SQLAlchemy model for direct manipulation
        ibm_in: InstitutionalBoardMemberUpdate # Accepts the Pydantic Update schema
    ) -> InstitutionalBoardMemberResponse: # Returns the Pydantic Response schema
        """
        Updates an existing institutional board member entry using data from the update schema.
        """
        update_data = ibm_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_ibm, key, value)

        self.db.add(db_ibm)
        self.db.commit()
        self.db.refresh(db_ibm)
        return InstitutionalBoardMemberResponse.model_validate(db_ibm)

    def delete(self, ibm_id: int) -> bool:
        """
        Deletes an institutional board member entry from the database by ID.
        """
        ibm = self.db.get(InstitutionalBoardMember, ibm_id) # Corrected to use SQLAlchemy model
        if ibm:
            self.db.delete(ibm)
            self.db.commit()
            return True
        return False