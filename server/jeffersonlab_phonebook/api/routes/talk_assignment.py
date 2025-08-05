from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from jeffersonlab_phonebook.schemas.conference_schemas import (
    TalkAssignmentCreate,
    TalkAssignmentUpdate,
)
from jeffersonlab_phonebook.schemas.response_schemas import TalkAssignmentResponse
from jeffersonlab_phonebook.db.session import get_db
from jeffersonlab_phonebook.repositories.talk_assignment_repository import TalkAssignmentRepository

router = APIRouter(prefix="/talk-assignments", tags=["Talk Assignments"])


@router.post("/", response_model=TalkAssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_talk_assignment(
    talk_assignment: TalkAssignmentCreate,
    db: Session = Depends(get_db)
):
    repository = TalkAssignmentRepository(db)
    return repository.create(talk_assignment)


@router.get("/", response_model=List[TalkAssignmentResponse])
def list_talk_assignments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    repository = TalkAssignmentRepository(db)
    return repository.get_all(skip=skip, limit=limit)


@router.get("/{assignment_id}", response_model=TalkAssignmentResponse)
def get_talk_assignment(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    repository = TalkAssignmentRepository(db)
    talk_assignment = repository.get(assignment_id)
    if not talk_assignment:
        raise HTTPException(status_code=404, detail="Talk assignment not found")
    return talk_assignment


@router.put("/{assignment_id}", response_model=TalkAssignmentResponse)
def update_talk_assignment(
    assignment_id: int,
    talk_assignment_update: TalkAssignmentUpdate,
    db: Session = Depends(get_db)
):
    repository = TalkAssignmentRepository(db)
    talk_assignment = repository.get(assignment_id)
    if not talk_assignment:
        raise HTTPException(status_code=404, detail="Talk assignment not found")
    return repository.update(talk_assignment, talk_assignment_update)


@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_talk_assignment(assignment_id: int, db: Session = Depends(get_db)):
    repo = TalkAssignmentRepository(db)
    success = repo.delete(assignment_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Talk assignment not found")
    return
