from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from jeffersonlab_phonebook.repositories.conference_repository import TalkRepository, ConferenceRepository
from jeffersonlab_phonebook.schemas.conference_schemas import ConferenceCreate, ConferenceUpdate, TalkCreate, TalkUpdate
from jeffersonlab_phonebook.schemas.response_schemas import TalkResponse, TalkLiteResponse, ConferenceResponse, ConferenceLiteResponse
from jeffersonlab_phonebook.db.session import get_db
from ..deps import get_current_user

router = APIRouter(prefix="/talks", tags=["Talks"])

# --- Talk Routes ---

@router.get(
    "/",
    response_model=List[TalkLiteResponse],
    summary="List all talks",
    description="Retrieve a list of all talks without nested relationships.",
)
def list_talks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    _=Depends(get_current_user),
):
    talk_repo = TalkRepository(db)
    talks = talk_repo.get_all(skip=skip, limit=limit)
    return [TalkLiteResponse.model_validate(talk) for talk in talks]


@router.post(
    "/",
    response_model=TalkResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new talk (Admin only)",
    description="Create a new talk assigned to a conference and optionally a member.",
)
def create_talk(
    talk_in: TalkCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    talk_repo = TalkRepository(db)
    db_talk = talk_repo.create(talk_in)
    return TalkResponse.model_validate(db_talk)


@router.get(
    "/{talk_id}",
    response_model=TalkResponse,
    summary="Get talk by ID",
    description="Retrieve a single talk with nested assignments and conference info.",
)
def get_talk(
    talk_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    talk_repo = TalkRepository(db)
    talk = talk_repo.get(talk_id)
    if not talk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Talk not found")
    return TalkResponse.model_validate(talk)


@router.put(
    "/{talk_id}",
    response_model=TalkResponse,
    summary="Update a talk (Admin only)",
    description="Update an existing talk's details.",
)
def update_talk(
    talk_id: int,
    talk_in: TalkUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    talk_repo = TalkRepository(db)
    db_talk = talk_repo.get(talk_id)
    if not db_talk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Talk not found")
    updated_talk = talk_repo.update(db_talk, talk_in)
    return TalkResponse.model_validate(updated_talk)


@router.delete(
    "/{talk_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a talk (Admin only)",
    description="Delete a talk by its ID.",
)
def delete_talk(
    talk_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    talk_repo = TalkRepository(db)
    deleted = talk_repo.delete(talk_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Talk not found")
    return


# --- Conference Routes ---

conference_router = APIRouter(prefix="/conferences", tags=["Conferences"])

@conference_router.get(
    "/",
    response_model=List[ConferenceLiteResponse],
    summary="List all conferences",
    description="Retrieve a list of all conferences without nested talks.",
)
def list_conferences(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    _=Depends(get_current_user),
):
    conference_repo = ConferenceRepository(db)
    conferences = conference_repo.get_all(skip=skip, limit=limit)
    return [ConferenceLiteResponse.model_validate(c) for c in conferences]


@conference_router.post(
    "/",
    response_model=ConferenceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new conference (Admin only)",
    description="Create a new conference with given details.",
)
def create_conference(
    conference_in: ConferenceCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    conference_repo = ConferenceRepository(db)
    db_conference = conference_repo.create(conference_in)
    return ConferenceResponse.model_validate(db_conference)


@conference_router.get(
    "/{conference_id}",
    response_model=ConferenceResponse,
    summary="Get conference by ID",
    description="Retrieve a single conference with optional nested talks.",
)
def get_conference(
    conference_id: int,
    include_talks: bool = Query(False),
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    conference_repo = ConferenceRepository(db)
    conference = conference_repo.get(conference_id, include_talks=include_talks)
    if not conference:
        raise HTTPException(status_code=404, detail="Conference not found")
    return ConferenceResponse.model_validate(conference)


@conference_router.put(
    "/{conference_id}",
    response_model=ConferenceResponse,
    summary="Update a conference (Admin only)",
    description="Update details of an existing conference.",
)
def update_conference(
    conference_id: int,
    conference_in: ConferenceUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    conference_repo = ConferenceRepository(db)
    db_conference = conference_repo.get(conference_id)
    if not db_conference:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conference not found")
    updated_conference = conference_repo.update(db_conference, conference_in)
    return ConferenceResponse.model_validate(updated_conference)


@conference_router.delete(
    "/{conference_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a conference (Admin only)",
    description="Delete a conference by its ID.",
)
def delete_conference(
    conference_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    conference_repo = ConferenceRepository(db)
    deleted = conference_repo.delete(conference_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conference not found")
    return
