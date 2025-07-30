from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session  # For type hinting db session

from jeffersonlab_phonebook.repositories.member_repository import MemberRepository
from jeffersonlab_phonebook.schemas.members_schemas import (
    MemberCreate,
    MemberResponse,
    MemberUpdate,
)
from jeffersonlab_phonebook.db.session import get_db

# Your security dependency that provides an active Member ORM object
from ..deps import get_current_user

router = APIRouter(prefix="/members", tags=["members"])


@router.get(
    "/",
    response_model=List[MemberResponse],
    summary="List all members",
    description="Retrieves a list of all members in the collaboration.",
)
def list_members(
    db: Session = Depends(get_db),
    # Assign to '_' to signal that the value itself is not used, only its side-effect.
    # This ensures the user is authenticated and active to access this endpoint.
    _=Depends(get_current_user),
):
    """
    Retrieves a list of all members from the database.
    The user must be authenticated and their account must be active.
    """
    member_repo = MemberRepository(db)
    members = member_repo.get_all()
    # FastAPI automatically handles the serialization from SQLAlchemy ORM objects
    # into MemberResponse Pydantic models, including nested relationships.
    return members


@router.post(
    "/",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new member",
    description="Creates a new member with the provided details.",
)
def create_member(
    member_in: MemberCreate,
    db: Session = Depends(get_db),
    # Ensure only authenticated and active users can create members
    _=Depends(get_current_user),
):
    """
    Creates a new member in the database.
    The user must be authenticated and their account must be active.
    """
    member_repo = MemberRepository(db)
    # You might want to add additional validation here,
    # e.g., check if an email or ORCID already exists.
    db_member = member_repo.create(member_in)
    return db_member


@router.get(
    "/{member_id}",
    response_model=MemberResponse,
    summary="Get a member by ID",
    description="Retrieves a single member by their unique ID.",
)
def get_member(
    member_id: int,
    db: Session = Depends(get_db),
    # Ensure only authenticated and active users can view member details
    _=Depends(get_current_user),
):
    """
    Retrieves a single member from the database by their ID.
    Raises a 404 Not Found error if the member does not exist.
    The user must be authenticated and their account must be active.
    """
    member_repo = MemberRepository(db)
    member = member_repo.get(member_id)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    return member


@router.patch(
    "/{member_id}",
    response_model=MemberResponse,
    summary="Update an existing member",
    description="Updates an existing member's details. Only provided fields will be changed.",
)
def update_member(
    member_id: int,
    member_in: MemberUpdate,
    db: Session = Depends(get_db),
    # Ensure only authenticated and active users can update members
    _=Depends(get_current_user),
):
    """
    Updates an existing member in the database.
    Only the fields provided in the request body will be updated.
    Raises a 404 Not Found error if the member does not exist.
    The user must be authenticated and their account must be active.
    """
    member_repo = MemberRepository(db)
    member = member_repo.get(member_id)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

    # The update method should handle applying the partial updates from member_in
    # to the existing 'member' ORM object.
    updated_member = member_repo.update(member, member_in)
    return updated_member


@router.delete(
    "/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a member",
    description="Deletes a member by their unique ID.",
)
def delete_member(
    member_id: int,
    db: Session = Depends(get_db),
    # Ensure only authenticated and active users can delete members
    _=Depends(get_current_user),
):
    """
    Deletes a member from the database by their ID.
    Raises a 404 Not Found error if the member does not exist.
    The user must be authenticated and their account must be active.
    """
    member_repo = MemberRepository(db)
    member = member_repo.get(member_id)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

    member_repo.delete(member_id)
    # FastAPI automatically returns 204 No Content for functions that return None
    # when status_code=status.HTTP_204_NO_CONTENT is specified.
    return