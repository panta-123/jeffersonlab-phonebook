# File: jeffersonlab_phonebook/repositories/group_repository.py

from typing import List, Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from jeffersonlab_phonebook.db.models import Group, GroupMember, Role
from jeffersonlab_phonebook.schemas.group_schemas import GroupCreate, GroupUpdate, GroupMemberCreate, GroupMemberUpdate

class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, group_id: int) -> Optional[Group]:
        query = select(Group).where(Group.id == group_id).options(
            joinedload(Group.subgroups),
            joinedload(Group.group_memberships)
        )
        db_group = self.db.scalar(query)
        return db_group

    def get_by_name(self, name: str) -> Optional[Group]:
        """
        Retrieves a single group by its name and returns the ORM object.
        """
        db_group = self.db.scalar(select(Group).where(Group.name == name))
        return db_group

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Group]:
        query = select(Group)
        db_groups = self.db.scalars(query.offset(skip).limit(limit)).all()
        return db_groups

    def create(self, group_in: GroupCreate) -> Group:
        """
        Creates a new group and returns the ORM object.
        """
        db_group = Group(**group_in.model_dump())
        self.db.add(db_group)
        self.db.commit()
        self.db.refresh(db_group)
        return db_group

    def update(self, db_group: Group, group_in: GroupUpdate) -> Group:
        """
        Updates an existing group and returns the ORM object.
        """
        update_data = group_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_group, key, value)
        self.db.add(db_group)
        self.db.commit()
        self.db.refresh(db_group)
        return db_group

    def delete(self, group_id: int) -> bool:
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

    def get(self, gm_id: int) -> Optional[GroupMember]:
        """
        Retrieves a single group member entry by its ID and returns the ORM object.
        """
        db_gm = self.db.get(GroupMember, gm_id)
        return db_gm

    def get_by_member_and_group(self, member_id: int, group_id: int) -> Optional[GroupMember]:
        """
        Retrieves a group member entry by member_id and group_id and returns the ORM object.
        """
        db_gm = self.db.scalar(
            select(GroupMember)
            .where(GroupMember.member_id == member_id)
            .where(GroupMember.group_id == group_id)
        )
        return db_gm

    def get_all(
        self,
        group_id: int,
        skip: int = 0,
        limit: int = 100,
        role_name: Optional[str] = None
    ) -> Sequence[GroupMember]:
        query = select(GroupMember).where(GroupMember.group_id == group_id)
        if role_name:
            query = query.join(GroupMember.role).where(Role.name == role_name)
        query = query.offset(skip).limit(limit)
        return self.db.execute(query).scalars().all()

    def create(self, gm_in: GroupMemberCreate) -> GroupMember:
        """
        Creates a new group member entry and returns the ORM object.
        """
        db_gm = GroupMember(**gm_in.model_dump())
        self.db.add(db_gm)
        self.db.commit()
        self.db.refresh(db_gm)
        return db_gm

    def update(self, db_gm: GroupMember, gm_in: GroupMemberUpdate) -> GroupMember:
        update_data = gm_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_gm, key, value)
        self.db.add(db_gm)
        self.db.commit()
        self.db.refresh(db_gm)
        return db_gm

    def delete(self, gm_id: int) -> bool:
        gm = self.db.get(GroupMember, gm_id)
        if gm:
            self.db.delete(gm)
            self.db.commit()
            return True
        return False