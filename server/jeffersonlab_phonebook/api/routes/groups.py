from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from jeffersonlab_phonebook.repositories.group_repository import GroupRepository, GroupMemberRepository
from jeffersonlab_phonebook.repositories.member_repository import MemberRepository
from jeffersonlab_phonebook.schemas.group_schemas import (
    GroupCreate,
    GroupUpdate,
    GroupMemberCreate,
)
from jeffersonlab_phonebook.schemas.response_schemas import GroupResponse, GroupMemberResponse, GroupLiteResponse
from jeffersonlab_phonebook.db.constants import GroupRole
from jeffersonlab_phonebook.db.session import get_db
from ..deps import get_current_user


router = APIRouter(prefix="/groups", tags=["Working Groups"])


# --- Group Routes ---

@router.get(
    "/",
    response_model=List[GroupLiteResponse],
    summary="List all working groups",
    description="Retrieves a list of all working groups in the collaboration without nested relationships.",
)
def list_groups(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    _=Depends(get_current_user),
):
    """
    Retrieves a list of all working groups from the database.
    """
    group_repo = GroupRepository(db)
    groups = group_repo.get_all(skip=skip, limit=limit)
    return [GroupLiteResponse.model_validate(group) for group in groups]


@router.post(
    "/",
    response_model=GroupResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new working group (Admin only)",
    description="Creates a new working group with the provided name.",
)
def create_group(
    group_in: GroupCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Creates a new working group in the database.
    """
    group_repo = GroupRepository(db)
    existing_group = group_repo.get_by_name(group_in.name)
    if existing_group:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Group with name '{group_in.name}' already exists",
        )
    # The repository now returns an ORM object
    db_group = group_repo.create(group_in)
    # The router is responsible for converting it to a Pydantic schema
    return GroupResponse.model_validate(db_group)


@router.get(
    "/{group_id}",
    response_model=GroupResponse,
    summary="Get working group by ID",
    description="Retrieves a single working group by its unique ID, including all nested relationships.",
)
def get_group(
    group_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Retrieves a single working group from the database by its ID.
    """
    group_repo = GroupRepository(db)
    group = group_repo.get(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Working group not found")
    return GroupResponse.model_validate(group)


@router.put(
    "/{group_id}",
    response_model=GroupResponse,
    summary="Update a working group (Admin only)",
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
    """
    group_repo = GroupRepository(db)
    db_group = group_repo.get(group_id)
    if not db_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Working group not found"
        )
    # The repository now returns the updated ORM object
    updated_group = group_repo.update(db_group, group_in)
    # The router is responsible for converting it
    return GroupResponse.model_validate(updated_group)


@router.delete(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a working group (Admin only)",
    description="Deletes a working group by its ID.",
)
def delete_group(
    group_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Deletes a working group from the database.
    """
    group_repo = GroupRepository(db)
    deleted = group_repo.delete(group_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Working group not found"
        )
    return


# --- Group Member Routes ---

@router.get(
    "/{group_id}/members",
    response_model=List[GroupMemberResponse],
    summary="List members of a specific working group",
    description="Retrieves a list of members belonging to a specific working group.",
)
def list_group_members_of_group(
    group_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    role_name: Optional[GroupRole] = None,
    _=Depends(get_current_user),
):
    """
    Retrieves members of a specific working group.
    """
    gm_repo = GroupMemberRepository(db)
    role_str = role_name.value if role_name else None
    group_members = gm_repo.get_all(group_id=group_id, skip=skip, limit=limit, role_name=role_str)
    # The router is responsible for the conversion
    return [GroupMemberResponse.model_validate(gm) for gm in group_members]


@router.post(
    "/{group_id}/members",
    response_model=GroupMemberResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a member to a working group (Admin only)",
    description="Adds an existing member to a specific working group with a given role.",
)
def add_member_to_group(
    group_id: int,
    gm_in: GroupMemberCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Adds a member to a working group.
    """
    if gm_in.group_id != group_id:
         raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST, 
             detail="Group ID in path does not match ID in request body"
         )

    member_repo = MemberRepository(db)
    member_exists = member_repo.get(gm_in.member_id)
    if not member_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
        
    gm_repo = GroupMemberRepository(db)
    existing_gm = gm_repo.get_by_member_and_group(member_id=gm_in.member_id, group_id=group_id)
    if existing_gm:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Member is already part of this group",
        )

    # The repository now returns an ORM object
    db_gm = gm_repo.create(gm_in)
    # The router is responsible for converting it
    return GroupMemberResponse.model_validate(db_gm)


@router.delete(
"/group-members/{gm_id}",
status_code=status.HTTP_204_NO_CONTENT,
summary="Remove a member from a working group (Admin only)",
description="Removes a member from a working group by deleting their group membership entry.",
)
def delete_group_member(
    gm_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Deletes a group member entry from the database.
    """
    gm_repo = GroupMemberRepository(db)
    deleted = gm_repo.delete(gm_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group member entry not found"
        )
    return