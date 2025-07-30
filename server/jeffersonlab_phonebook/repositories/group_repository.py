from datetime import date
from typing import List, Optional

from sqlalchemy import select, or_
from sqlalchemy.orm import Session, joinedload

# Import SQLAlchemy models
from jeffersonlab_phonebook.db.models import Group, GroupMember, Member # Added Member

# Import the GroupRole enum
from jeffersonlab_phonebook.db.constants import GroupRole

# Import Pydantic schemas
from jeffersonlab_phonebook.schemas.group_schemas import ( # Assuming a group_schemas.py file
    GroupCreate,
    GroupUpdate,
    GroupResponse,
    GroupMemberCreate,
    GroupMemberUpdate, # New: Added this schema
    GroupMemberResponse,
)

# --- Group Repository ---
class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, group_id: int) -> Optional[GroupResponse]:
        """
        Retrieves a single group by its ID and converts it to a response schema.
        """
        db_group = self.db.get(Group, group_id)
        if db_group:
            return GroupResponse.model_validate(db_group)
        return None

    def get_by_name(self, name: str) -> Optional[GroupResponse]:
        """
        Retrieves a single group by its name and converts it to a response schema.
        """
        db_group = self.db.scalar(select(Group).where(Group.name == name))
        if db_group:
            return GroupResponse.model_validate(db_group)
        return None

    def get_all(self, skip: int = 0, limit: int = 100) -> List[GroupResponse]:
        """
        Retrieves all groups from the database with pagination,
        eagerly loading their members, and converting them to response schemas.
        """
        query = select(Group).options(
            joinedload(Group.group_memberships).joinedload(GroupMember.member)
        )
        db_groups = self.db.scalars(query.offset(skip).limit(limit)).all()
        return [GroupResponse.model_validate(group) for group in db_groups]

    def create(self, group_in: GroupCreate) -> GroupResponse:
        """
        Creates a new group in the database from the provided schema.
        """
        db_group = Group(**group_in.model_dump())
        self.db.add(db_group)
        self.db.commit()
        self.db.refresh(db_group)
        return GroupResponse.model_validate(db_group)

    def update(self, db_group: Group, group_in: GroupUpdate) -> GroupResponse:
        """
        Updates an existing group in the database using data from the update schema.
        """
        update_data = group_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_group, key, value)
        self.db.add(db_group)
        self.db.commit()
        self.db.refresh(db_group)
        return GroupResponse.model_validate(db_group)

    def delete(self, group_id: int) -> bool:
        """
        Deletes a group from the database by ID.
        """
        group = self.db.get(Group, group_id)
        if group:
            self.db.delete(group)
            self.db.commit()
            return True
        return False

# --- GroupMember Repository ---
class GroupMemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, gm_id: int) -> Optional[GroupMemberResponse]:
        """
        Retrieves a single group member entry by its ID and converts it to a response schema.
        """
        db_gm = self.db.get(GroupMember, gm_id)
        if db_gm:
            return GroupMemberResponse.model_validate(db_gm)
        return None

    def get_by_member_and_group(self, member_id: int, group_id: int) -> Optional[GroupMemberResponse]:
        """
        Retrieves a group member entry by member_id and group_id and converts it to a response schema.
        """
        db_gm = self.db.scalar(
            select(GroupMember)
            .where(GroupMember.member_id == member_id)
            .where(GroupMember.group_id == group_id)
        )
        if db_gm:
            return GroupMemberResponse.model_validate(db_gm)
        return None

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        group_id: Optional[int] = None,
        member_id: Optional[int] = None,
        role: Optional[GroupRole] = None,
    ) -> List[GroupMemberResponse]:
        """
        Retrieves all group member entries from the database with pagination
        and optional filtering, then converts them to response schemas.
        Includes eager loading of 'group' and 'member' relationships.
        """
        query = select(GroupMember).options(
            joinedload(GroupMember.group), joinedload(GroupMember.member)
        )

        if group_id:
            query = query.where(GroupMember.group_id == group_id)
        if member_id:
            query = query.where(GroupMember.member_id == member_id)
        if role:
            query = query.where(GroupMember.role == role)

        db_gms = self.db.scalars(query.offset(skip).limit(limit)).all()
        return [GroupMemberResponse.model_validate(gm) for gm in db_gms]

    def create(
        self, gm_in: GroupMemberCreate # Accepts the Pydantic Create schema
    ) -> GroupMemberResponse: # Returns the Pydantic Response schema
        """
        Creates a new group member entry from the provided schema.
        """
        db_gm = GroupMember(**gm_in.model_dump())
        self.db.add(db_gm)
        self.db.commit()
        self.db.refresh(db_gm)
        return GroupMemberResponse.model_validate(db_gm)

    def update(
        self, db_gm: GroupMember, gm_in: GroupMemberUpdate # Accepts the Pydantic Update schema
    ) -> GroupMemberResponse: # Returns the Pydantic Response schema
        """
        Updates an existing group member entry using data from the update schema.
        """
        update_data = gm_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_gm, key, value)
        self.db.add(db_gm)
        self.db.commit()
        self.db.refresh(db_gm)
        return GroupMemberResponse.model_validate(db_gm)

    def delete(self, gm_id: int) -> bool:
        """
        Deletes a group member entry from the database by ID.
        """
        gm = self.db.get(GroupMember, gm_id)
        if gm:
            self.db.delete(gm)
            self.db.commit()
            return True
        return False