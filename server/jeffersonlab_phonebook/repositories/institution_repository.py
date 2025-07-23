from typing import List, Optional

from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from jeffersonlab_phonebook.db.models import Institution
from jeffersonlab_phonebook.schemas.members import (
    InstitutionCreate,
    InstitutionUpdate,
)


class InstitutionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, institution_id: int) -> Optional[Institution]:
        """
        Retrieves a single institution by its ID.
        """
        return self.db.get(Institution, institution_id)

    def get_by_name(self, name: str) -> Optional[Institution]:
        """
        Retrieves a single institution by its full_name or short_name.
        """
        return self.db.scalar(
            select(Institution).where(
                or_(
                    Institution.full_name == name,
                    Institution.short_name == name,
                )
            )
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Institution]:
        """
        Retrieves all institutions from the database with pagination.
        """
        return list(
            self.db.scalars(select(Institution).offset(skip).limit(limit)).all()
        )

    def create(self, institution_in: InstitutionCreate) -> Institution:
        """
        Creates a new institution in the database.
        """
        db_institution = Institution(**institution_in.model_dump())
        self.db.add(db_institution)
        self.db.commit()
        self.db.refresh(db_institution)
        return db_institution

    def update(
        self, db_institution: Institution, institution_in: InstitutionUpdate
    ) -> Institution:
        """
        Updates an existing institution in the database.
        """
        update_data = institution_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_institution, key, value)
        self.db.add(db_institution)
        self.db.commit()
        self.db.refresh(db_institution)
        return db_institution

    def delete(self, institution_id: int):
        """
        Deletes an institution from the database by ID.
        """
        institution = self.db.get(Institution, institution_id)
        if institution:
            self.db.delete(institution)
            self.db.commit()
            return True
        return False
