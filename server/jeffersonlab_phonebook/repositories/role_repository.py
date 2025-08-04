from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from jeffersonlab_phonebook.db.models import Role
from jeffersonlab_phonebook.schemas.role_schemas import RoleCreate, RoleUpdate

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, role_id: int) -> Optional[Role]:
        """
        Retrieves a single role by its ID.
        Returns the SQLAlchemy ORM object.
        """
        return self.db.get(Role, role_id)

    def get_by_name(self, name: str) -> Optional[Role]:
        """
        Retrieves a single role by its name.
        Returns the SQLAlchemy ORM object.
        """
        return self.db.scalar(select(Role).where(Role.name == name))

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Role]:
        """
        Retrieves all roles from the database with pagination.
        Returns a list of SQLAlchemy ORM objects.
        """
        return list(self.db.scalars(select(Role).offset(skip).limit(limit)).all())

    def create(self, role_in: RoleCreate) -> Role:
        """
        Creates a new role in the database.
        """
        db_role = Role(**role_in.model_dump())
        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role

    def update(self, db_role: Role, role_in: RoleUpdate) -> Role:
        """
        Updates an existing role in the database.
        """
        update_data = role_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_role, key, value)
        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role

    def delete(self, role_id: int) -> bool:
        """
        Deletes a role from the database by ID.
        """
        role = self.db.get(Role, role_id)
        if role:
            self.db.delete(role)
            self.db.commit()
            return True
        return False