from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Import the repositories for Group and GroupMember
from jeffersonlab_phonebook.repositories.group_repository import GroupRepository
from jeffersonlab_phonebook.repositories.group_repository import GroupMemberRepository
from jeffersonlab_phonebook.repositories.institution_repository import InstitutionRepository

# Import the schemas for Group and GroupMember
from jeffersonlab_phonebook.schemas.group_schemas import (
    GroupCreate,
    GroupUpdate,
    GroupResponse,
    GroupMemberCreate,
    GroupMemberUpdate,
    GroupMemberResponse,
)
# Import the GroupRole enum
from jeffersonlab_phonebook.db.constants import GroupRole

# Import common dependencies
from jeffersonlab_phonebook.db.session import get_db
from ..deps import get_current_user


router = APIRouter(prefix="/groups", tags=["Working Groups"])


# --- Group Routes ---

@router.get(
    "/",
    response_model=List[GroupResponse],
    summary="List all working groups",
    description="Retrieves a list of all working groups in the collaboration.",
)
def list_groups(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    _=Depends(get_current_user),
):
    """
    Retrieves a list of all working groups from the database.
    The user must be authenticated and their account must be active.
    """
    group_repo = GroupRepository(db)
    groups = group_repo.get_all(skip=skip, limit=limit)
    return groups


@router.post(
    "/",
    response_model=GroupResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new working group",
    description="Creates a new working group with the provided name.",
)
def create_group(
    group_in: GroupCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Creates a new working group in the database.
    The user must be authenticated and their account must be active.
    Checks if a group with the same name already exists.
    """
    group_repo = GroupRepository(db)
    existing_group = group_repo.get_by_name(group_in.name)
    if existing_group:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Group with name '{group_in.name}' already exists",
        )
    db_group = group_repo.create(group_in)
    return db_group


@router.get(
    "/{group_id}",
    response_model=GroupResponse,
    summary="Get working group by ID",
    description="Retrieves a single working group by its unique ID.",
)
def get_group(
    group_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Retrieves a single working group from the database by its ID.
    The user must be authenticated and their account must be active.
    Raises a 404 error if the group is not found.
    """
    group_repo = GroupRepository(db)
    group = group_repo.get(group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Working group not found"
        )
    return group


@router.put(
    "/{group_id}",
    response_model=GroupResponse,
    summary="Update a working group",
    description="Updates an existing working group's details by its ID.",
)
def update_group(
    group_id: int,
    group_in: GroupUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Updates an existing working group in the database.
    The user must be authenticated and their account must be active.
    Raises a 404 error if the group is not found.
    """
    group_repo = GroupRepository(db)
    # Get the SQLAlchemy model instance first for update
    from jeffersonlab_phonebook.db.models import Group # Temporary import here for clarity, usually at top
    db_group = db.get(Group, group_id)
    if not db_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Working group not found"
        )
    updated_group = group_repo.update(db_group, group_in)
    return updated_group


@router.delete(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a working group",
    description="Deletes a working group by its ID.",
)
def delete_group(
    group_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Deletes a working group from the database.
    The user must be authenticated and their account must be active.
    Raises a 404 error if the group is not found.
    """
    group_repo = GroupRepository(db)
    deleted = group_repo.delete(group_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Working group not found"
        )
    # Consider handling deletion of associated GroupMembers or relying on DB cascade
    return {"message": "Working group deleted successfully"}


# --- Group Member Routes (nested under Group router or as separate sub-router) ---
# It's common to nest group member routes under the group, e.g., /groups/{group_id}/members
# For simplicity, I'll keep them as top-level /group-members for now, but prefix them conceptually.
# If you want them strictly nested, the prefix would be like "{group_id}/members" and group_id
# would be a path parameter in each function.

@router.get(
    "/{group_id}/members", # Nested route for members of a specific group
    response_model=List[GroupMemberResponse],
    summary="List members of a specific working group",
    description="Retrieves a list of members belonging to a specific working group.",
)
def list_group_members_of_group(
    group_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    role: Optional[GroupRole] = None,
    _=Depends(get_current_user),
):
    """
    Retrieves members of a specific working group.
    The user must be authenticated and their account must be active.
    Raises a 404 error if the group does not exist.
    """
    group_repo = GroupRepository(db)
    group = group_repo.get(group_id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Working group not found"
        )

    gm_repo = GroupMemberRepository(db)
    group_members = gm_repo.get_all(group_id=group_id, skip=skip, limit=limit, role=role)
    return group_members


@router.post(
    "/{group_id}/members",
    response_model=GroupMemberResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a member to a working group",
    description="Adds an existing member to a specific working group with a given role.",
)
def add_member_to_group(
    group_id: int,
    member_id: int, # As a path parameter, or include in GroupMemberCreate
    gm_in: GroupMemberCreate, # This should ideally only contain 'role' if member_id/group_id are path params
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Adds a member to a working group.
    The user must be authenticated and their account must be active.
    Raises 404 if group or member not found. Raises 409 if member is already in group.
    """
    # Verify group and member exist (optional but good practice)
    group_repo = GroupRepository(db)
    member_repo = InstitutionRepository(db) # You would need a MemberRepository here, not InstitutionRepository
    # Assuming you have a MemberRepository for validation:
    # from jeffersonlab_phonebook.repositories.member_repository import MemberRepository
    # member_repo = MemberRepository(db)

    group_exists = group_repo.get(group_id)
    if not group_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    # For a real app, validate member_id:
    # member_exists = member_repo.get(member_id)
    # if not member_exists:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")


    # Ensure the member_id and group_id from path match the body if provided
    if gm_in.group_id != group_id or gm_in.member_id != member_id:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mismatch between path parameters and request body IDs")


    gm_repo = GroupMemberRepository(db)
    existing_gm = gm_repo.get_by_member_and_group(member_id=member_id, group_id=group_id)
    if existing_gm:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Member is already part of this group",
        )

    db_gm = gm_repo.create(
        GroupMemberCreate(
            member_id=member_id,
            group_id=group_id,
            role=gm_in.role 
            )
    )
    return db_gm


@router.put(
    "/group-members/{gm_id}", # Or /{group_id}/members/{gm_id} if fully nested
    response_model=GroupMemberResponse,
    summary="Update a group member's role",
    description="Updates the role of a member within a specific working group.",
)
def update_group_member_role(
    gm_id: int,
    gm_in: GroupMemberUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Updates the role of a group member.
    The user must be authenticated and their account must be active.
    Raises a 404 error if the group member entry is not found.
    """
    gm_repo = GroupMemberRepository(db)
    # Get the SQLAlchemy model instance first for update
    from jeffersonlab_phonebook.db.models import GroupMember # Temporary import here for clarity, usually at top
    db_gm = db.get(GroupMember, gm_id)
    if not db_gm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group member entry not found"
        )
    updated_gm = gm_repo.update(db_gm, gm_in)
    return updated_gm


@router.delete(
    "/group-members/{gm_id}", # Or /{group_id}/members/{gm_id} if fully nested
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a member from a working group",
    description="Removes a member from a working group by deleting their group membership entry.",
)
def delete_group_member(
    gm_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Deletes a group member entry from the database.
    The user must be authenticated and their account must be active.
    Raises a 404 error if the group member entry is not found.
    """
    gm_repo = GroupMemberRepository(db)
    deleted = gm_repo.delete(gm_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group member entry not found"
        )
    return {"message": "Group member entry deleted successfully"}