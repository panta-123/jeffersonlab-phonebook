from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from jeffersonlab_phonebook.db.session import get_db
from jeffersonlab_phonebook.repositories.role_repository import RoleRepository
from jeffersonlab_phonebook.schemas.role_schemas import RoleCreate, RoleUpdate, RoleResponse
from ..deps import get_current_user

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get(
    "/",
    response_model=List[RoleResponse],
    summary="List all roles",
    description="Retrieves a list of all dynamic roles.",
)
def list_roles(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    _=Depends(get_current_user),
):
    """
    Retrieves a list of all roles from the database.
    """
    role_repo = RoleRepository(db)
    roles = role_repo.get_all(skip=skip, limit=limit)
    # Convert ORM objects to Pydantic models for the response
    return [RoleResponse.model_validate(role) for role in roles]


@router.post(
    "/",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new role (Admin only)",
    description="Creates a new dynamic role with a unique name.",
)
def create_role(
    role_in: RoleCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Creates a new role in the database.
    """
    role_repo = RoleRepository(db)
    existing_role = role_repo.get_by_name(role_in.name)
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Role with name '{role_in.name}' already exists",
        )
    db_role = role_repo.create(role_in)
    # Convert ORM object to Pydantic model for the response
    return RoleResponse.model_validate(db_role)


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Get role by ID",
    description="Retrieves a single role by its unique ID.",
)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Retrieves a single role from the database by its ID.
    """
    role_repo = RoleRepository(db)
    role = role_repo.get(role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    # Convert ORM object to Pydantic model for the response
    return RoleResponse.model_validate(role)


@router.put(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Update a role (Admin only)",
    description="Updates an existing role's details by its ID.",
)
def update_role(
    role_id: int,
    role_in: RoleUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Updates an existing role in the database.
    """
    role_repo = RoleRepository(db)
    db_role = role_repo.get(role_id)
    if not db_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    updated_role = role_repo.update(db_role, role_in)
    # Convert ORM object to Pydantic model for the response
    return RoleResponse.model_validate(updated_role)


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a role (Admin only)",
    description="Deletes a role by its ID.",
)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Deletes a role from the database.
    """
    role_repo = RoleRepository(db)
    deleted = role_repo.delete(role_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role not found"
        )
    return