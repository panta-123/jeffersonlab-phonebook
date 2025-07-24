from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from jeffersonlab_phonebook.repositories.institution_repository import (
    InstitutionRepository,
)
from jeffersonlab_phonebook.schemas.institutions_schemas import (
    InstitutionCreate,
    InstitutionResponse,
    InstitutionUpdate,
)
from jeffersonlab_phonebook.db.session import get_db

from ..deps import get_current_user

router = APIRouter(prefix="/institutions", tags=["institutions"])


@router.get(
    "/",
    response_model=List[InstitutionResponse],
    summary="List all institutions",
    description="Retrieves a list of all institutions in the collaboration.",
)
def list_institutions(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    # Assign to '_' to signal that the value itself is not used, only its side-effect.
    _=Depends(get_current_user),
):
    """
    Retrieves a list of all institutions from the database.
    The user must be authenticated and their account must be active.
    """
    institution_repo = InstitutionRepository(db)
    institutions = institution_repo.get_all(skip=skip, limit=limit)
    return institutions


@router.post(
    "/",
    response_model=InstitutionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new institution",
    description="Creates a new institution with the provided details.",
)
def create_institution(
    institution_in: InstitutionCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Creates a new institution in the database.
    The user must be authenticated and their account must be active.
    """
    institution_repo = InstitutionRepository(db)
    # You might want to add logic here to check for existing institutions by name
    # or other unique identifiers before creating.
    db_institution = institution_repo.create(institution_in)
    return db_institution


@router.get(
    "/{institution_id}",
    response_model=InstitutionResponse,
    summary="Get institution by ID",
    description="Retrieves a single institution by its unique ID.",
)
def get_institution(
    institution_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Retrieves a single institution from the database by its ID.
    The user must be authenticated and their account must be active.
    Raises a 404 error if the institution is not found.
    """
    institution_repo = InstitutionRepository(db)
    institution = institution_repo.get(institution_id)
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found"
        )
    return institution


@router.put(
    "/{institution_id}",
    response_model=InstitutionResponse,
    summary="Update an institution",
    description="Updates an existing institution's details by its ID.",
)
def update_institution(
    institution_id: int,
    institution_in: InstitutionUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Updates an existing institution in the database.
    The user must be authenticated and their account must be active.
    Raises a 404 error if the institution is not found.
    """
    institution_repo = InstitutionRepository(db)
    db_institution = institution_repo.get(institution_id)
    if not db_institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found"
        )
    updated_institution = institution_repo.update(db_institution, institution_in)
    return updated_institution


@router.delete(
    "/{institution_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an institution",
    description="Deletes an institution by its ID.",
)
def delete_institution(
    institution_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Deletes an institution from the database.
    The user must be authenticated and their account must be active.
    Raises a 404 error if the institution is not found.
    """
    institution_repo = InstitutionRepository(db)
    deleted = institution_repo.delete(institution_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found"
        )
    return {"message": "Institution deleted successfully"}
