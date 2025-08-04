from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from jeffersonlab_phonebook.repositories.institutionboard_repository import (
    InstitutionalBoardMemberRepository,
)
from jeffersonlab_phonebook.schemas.board_schemas import (
    InstitutionalBoardMemberCreate,
    InstitutionalBoardMemberUpdate,
)
from jeffersonlab_phonebook.schemas.response_schemas import InstitutionalBoardMemberResponse
from jeffersonlab_phonebook.db.constants import BoardType

from jeffersonlab_phonebook.db.session import get_db
from ..deps import get_current_user

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
    board_type: Optional[BoardType] = None,
    member_id: Optional[int] = None,
    institution_id: Optional[int] = None,
    _=Depends(get_current_user),
):
    ibm_repo = InstitutionalBoardMemberRepository(db)
    board_memberships_orms = ibm_repo.get_all(
        skip=skip,
        limit=limit,
        board_type=board_type,
        member_id=member_id,
        institution_id=institution_id,
    )
    return board_memberships_orms


@router.post(
    "/",
    response_model=InstitutionalBoardMemberResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new institutional/executive board membership (Admin only)",
    description="Creates a new board membership for a member at an institution.",
)
def create_board_membership(
    ibm_in: InstitutionalBoardMemberCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    ibm_repo = InstitutionalBoardMemberRepository(db)
    db_ibm = ibm_repo.create(ibm_in=ibm_in)
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
    summary="Update a board membership (Admin only)",
    description="Updates an existing institutional/executive board membership's details by its ID.",
)
def update_board_membership(
    ibm_id: int,
    ibm_in: InstitutionalBoardMemberUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    ibm_repo = InstitutionalBoardMemberRepository(db)
    db_ibm = ibm_repo.get(ibm_id)
    if not db_ibm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board membership not found"
        )
    updated_ibm = ibm_repo.update(db_ibm, ibm_in)
    return updated_ibm


@router.delete(
    "/{ibm_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a board membership (Admin only)",
    description="Deletes an institutional/executive board membership by its ID.",
)
def delete_board_membership(
    ibm_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    ibm_repo = InstitutionalBoardMemberRepository(db)
    deleted = ibm_repo.delete(ibm_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Board membership not found"
        )
    return