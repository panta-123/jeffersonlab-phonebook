from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # For type hinting db session

from jeffersonlab_phonebook.repositories.member_repository import MemberRepository
from jeffersonlab_phonebook.schemas.members_schemas import MemberResponse
from jeffersonlab_phonebook.db.session import get_db

# Your security dependency that provides an active Member ORM object
from ..deps import get_current_user

router = APIRouter(prefix="/members", tags=["members"])


@router.get(
    "/",
    response_model=List[
        MemberResponse
    ],  # Declares the response will be a list of MemberResponse objects
    summary="List all members",
    description="Retrieves a list of all members in the collaboration.",
)
def list_members(
    db: Session = Depends(get_db),
    # FIX: Use get_current_active_member to ensure active status check
    # Assign to '_' to signal that the value itself is not used, only its side-effect.
    _=Depends(get_current_user),
):
    """
    Retrieves a list of all members from the database.
    The user must be authenticated and their account must be active.
    """
    member_repo = MemberRepository(db)

    # Calls the get_all method from your repository, which now eagerly loads institution.
    members = member_repo.get_all()

    # FastAPI automatically handles the serialization from SQLAlchemy Member ORM objects
    # (including the eagerly loaded institution) into MemberResponse Pydantic models.
    return members
