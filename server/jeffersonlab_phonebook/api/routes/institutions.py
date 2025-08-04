from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from jeffersonlab_phonebook.repositories.institution_repository import (
    InstitutionRepository,
)
from jeffersonlab_phonebook.repositories.member_repository import (
    MemberRepository,
)
from jeffersonlab_phonebook.schemas.institutions_schemas import (
    InstitutionCreate,
    InstitutionUpdate,
)
from jeffersonlab_phonebook.schemas.response_schemas import InstitutionLiteResponse, MemberLiteResponse
from jeffersonlab_phonebook.services.ror_api_client import (
    call_ror_api,
    RorApiClientError,
    RorApiNetworkError,
    RorApiDataError
)
from jeffersonlab_phonebook.db.session import get_db

from ..deps import get_current_user

router = APIRouter(prefix="/institutions", tags=["institutions"])


@router.get(
    "/",
    response_model=List[InstitutionLiteResponse],
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
    response_model=InstitutionLiteResponse,
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
    response_model=InstitutionLiteResponse,
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
    response_model=InstitutionLiteResponse,
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
    # --- ROR API Integration Logic ---
    # Check if rorid is provided in the update payload and is not None (meaning it's being set/updated)
    update_data = institution_in.model_dump(exclude_unset=True)
    if "rorid" in update_data and update_data["rorid"] is not None:
        new_rorid = update_data["rorid"]
        try:
            ror_data_from_api = call_ror_api(new_rorid)
            filtered_ror_data = {k: v for k, v in ror_data_from_api.items() if v is not None}

            update_data.update(filtered_ror_data)
        except RorApiNetworkError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to connect to ROR API: {e}"
            ) from e
        except RorApiDataError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"ROR API returned invalid data: {e}"
            ) from e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred during ROR API processing: {e}"
            ) from e
    if "full_name" not in update_data:
        # If so, get the full_name from the existing database record and add it to update_data.
        # We check `db_institution.full_name` to ensure it's not None.
        if db_institution.full_name:
            update_data["full_name"] = db_institution.full_name
    print(update_data)
    final_institution_in = InstitutionUpdate(**update_data)

    updated_institution = institution_repo.update(db_institution, final_institution_in)
    return updated_institution
        
    #updated_institution = institution_repo.update(db_institution, institution_in)
    #update_data = institution_in.model_dump(exclude_unset=True)

    
    #return updated_institution


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


@router.get(
    "/{institution_id}/members",
    response_model=List[MemberLiteResponse],
    summary="List all members of an institution",
    description="Retrieves all members associated with a specific institution.",
)
def get_institution_members(
    institution_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    """
    Retrieves all members belonging to a given institution, with optional pagination.
    Raises a 404 error if the institution does not exist.
    """
    institution_repo = InstitutionRepository(db)
    if not institution_repo.get(institution_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Institution not found"
        )

    member_repo = MemberRepository(db)
    return member_repo.get_member_by_institution(institution_id, skip, limit)
