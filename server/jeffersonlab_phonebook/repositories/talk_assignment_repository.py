from sqlalchemy.orm import Session
from sqlalchemy import select

from jeffersonlab_phonebook.db.models import TalkAssignment
from jeffersonlab_phonebook.schemas.conference_schemas import (
    TalkAssignmentCreate,
    TalkAssignmentUpdate
)
from typing import List, Optional, Sequence
from datetime import date



class TalkAssignmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, assignment_id: int) -> Optional[TalkAssignment]:
        return self.db.get(TalkAssignment, assignment_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[TalkAssignment]:
        query = select(TalkAssignment).offset(skip).limit(limit)
        return self.db.scalars(query).all()

    def create(self, assignment_in: TalkAssignmentCreate) -> TalkAssignment:
        data = assignment_in.model_dump()
        data["assignment_date"] = date.today()
        assignment = TalkAssignment(**data)
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment

    def update(self, db_assignment: TalkAssignment, assignment_in: TalkAssignmentUpdate) -> TalkAssignment:
        update_data = assignment_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_assignment, key, value)
        self.db.add(db_assignment)
        self.db.commit()
        self.db.refresh(db_assignment)
        return db_assignment

    def delete(self, assignment_id: int) -> bool:
        assignment = self.db.get(TalkAssignment, assignment_id)
        if assignment:
            self.db.delete(assignment)
            self.db.commit()
            return True
        return False
