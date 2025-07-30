from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Import the repository for Institutional Board Members
from jeffersonlab_phonebook.repositories.institutionboard_repository import (
    InstitutionalBoardMemberRepository,
)
# Import the schemas for Institutional Board Members
from jeffersonlab_phonebook.schemas.board_schemas import (
    InstitutionalBoardMemberCreate,
    InstitutionalBoardMemberUpdate,
    InstitutionalBoardMemberResponse,
)
# Import the BoardType enum
from jeffersonlab_phonebook.db.constants import BoardType

# Import common dependencies
from jeffersonlab_phonebook.db.session import get_db
from ..deps import get_current_user # Assuming 'deps.py' is in the parent directory of 'routes'

router = APIRouter(prefix="/board-members", tags=["Board Members"])


@router.get(
    "/",
    response_model=List[InstitutionalBoardMemberResponse],
    summary="List all institutional/executive board memberships",
    description="Retrieves a list of all board memberships, with optional filtering by board type, member, or institution.",
)
def list_board_memberships(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    board_type: Optional[BoardType] = None, # Allow filtering by BoardType
    member_id: Optional[int] = None,
    institution_id: Optional[int] = None,
    _=Depends(get_current_user),
):
    """
    Retrieves a list of all institutional/executive board memberships from the database.
    The user must be authenticated and their account must be active.
    Can be filtered by board type (e.g., 'institutional', 'executive'), member ID, or institution ID.
    """
    ibm_repo = InstitutionalBoardMemberRepository(db)
    board_memberships = ibm_repo.get_all(
        skip=skip,
        limit=limit,
        board_type=board_type,
        member_id=member_id,
        institution_id=institution_id,
    )
    return board_memberships


@router.post(
    "/",
    response_model=InstitutionalBoardMemberResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new institutional/executive board membership",
    description="Creates a new board membership for a member at an institution.",
)
def create_board_membership(
    ibm_in: InstitutionalBoardMemberCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Creates a new institutional/executive board membership in the database.
    The user must be authenticated and their account must be active.
    """
    ibm_repo = InstitutionalBoardMemberRepository(db)
    # You might want to add checks here, e.g., if member_id or institution_id exist
    # For simplicity, assuming they exist for now.
    db_ibm = ibm_repo.create(
        member_id=ibm_in.member_id,
        institution_id=ibm_in.institution_id,
        board_type=ibm_in.board_type,
        start_date=ibm_in.start_date,
        role=ibm_in.role,
        end_date=ibm_in.end_date,
        is_chair=ibm_in.is_chair,
    )
    return db_ibm


@router.get(
    "/{ibm_id}",
    response_model=InstitutionalBoardMemberResponse,
    summary="Get board membership by ID",
    description="Retrieves a single institutional/executive board membership by its unique ID.",
)
def get_board_membership(
    ibm_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Retrieves a single institutional/executive board membership from the database by its ID.
    The user must be authenticated and their account must be active.
    Raises a 404 error if the membership is not found.
    """
    ibm_repo = InstitutionalBoardMemberRepository(db)
    ibm = ibm_repo.get(ibm_id)
    if not ibm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board membership not found"
        )
    return ibm


@router.put(
    "/{ibm_id}",
    response_model=InstitutionalBoardMemberResponse,
    summary="Update a board membership",
    description="Updates an existing institutional/executive board membership's details by its ID.",
)
def update_board_membership(
    ibm_id: int,
    ibm_in: InstitutionalBoardMemberUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Updates an existing institutional/executive board membership in the database.
    The user must be authenticated and their account must be active.
    Raises a 404 error if the membership is not found.
    """
    ibm_repo = InstitutionalBoardMemberRepository(db)
    # First, get the SQLAlchemy model instance to pass to the repository's update method
    # This requires importing the SQLAlchemy model directly.
    from jeffersonlab_phonebook.db.models import InstitutionalBoardMember # Temporary import here for clarity, usually at top
    db_ibm = db.get(InstitutionalBoardMember, ibm_id) # Get the DB model, not the Pydantic response
    if not db_ibm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board membership not found"
        )
    updated_ibm = ibm_repo.update(db_ibm, ibm_in) # Pass the DB model and the Pydantic update schema
    return updated_ibm


@router.delete(
    "/{ibm_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a board membership",
    description="Deletes an institutional/executive board membership by its ID.",
)
def delete_board_membership(
    ibm_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Deletes an institutional/executive board membership from the database.
    The user must be authenticated and their account must be active.
    Raises a 404 error if the membership is not found.
    """
    ibm_repo = InstitutionalBoardMemberRepository(db)
    deleted = ibm_repo.delete(ibm_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board membership not found"
        )
    return {"message": "Board membership deleted successfully"}