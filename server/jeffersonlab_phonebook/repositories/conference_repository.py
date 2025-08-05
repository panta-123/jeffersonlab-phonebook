# File: jeffersonlab_phonebook/repositories/talk_conference_repository.py

from typing import List, Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload, defer

from jeffersonlab_phonebook.db.models import Talk, Conference, TalkAssignment
from jeffersonlab_phonebook.schemas.conference_schemas import ConferenceCreate, ConferenceUpdate, TalkCreate, TalkUpdate


class TalkRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, talk_id: int) -> Optional[Talk]:
        query = select(Talk).where(Talk.id == talk_id).options(
            joinedload(Talk.assignments).joinedload(TalkAssignment.member),
            joinedload(Talk.assignments).joinedload(TalkAssignment.role),
            joinedload(Talk.assignments).joinedload(TalkAssignment.assigned_by_member),
        )
        return self.db.scalar(query)

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Talk]:
        query = select(Talk).offset(skip).limit(limit)
        talks = self.db.scalars(query).all()
        return talks

    def create(self, talk_in: TalkCreate) -> Talk:
        talk = Talk(**talk_in.model_dump(exclude_unset=True))
        self.db.add(talk)
        self.db.commit()
        self.db.refresh(talk)
        return talk

    def update(self, db_talk: Talk, talk_in: TalkUpdate) -> Talk:
        update_data = talk_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_talk, key, value)
        self.db.add(db_talk)
        self.db.commit()
        self.db.refresh(db_talk)
        return db_talk

    def delete(self, talk_id: int) -> bool:
        talk = self.db.get(Talk, talk_id)
        if talk:
            self.db.delete(talk)
            self.db.commit()
            return True
        return False


class ConferenceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, conference_id: int, include_talks: bool = False):
        query = select(Conference).where(Conference.id == conference_id)
        if include_talks:
            query = query.options(
                joinedload(Conference.talks).options(
                    selectinload(Talk.assignments).options(
                        selectinload(TalkAssignment.member),
                        selectinload(TalkAssignment.role),
                        selectinload(TalkAssignment.assigned_by_member),
                        defer(TalkAssignment.talk_id),
                    ),
                    defer(Talk.conference_id),
                )
            )
        return self.db.scalar(query)

    def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Conference]:
        query = select(Conference).offset(skip).limit(limit)
        conferences = self.db.scalars(query).all()
        return conferences

    def create(self, conference_in: ConferenceCreate) -> Conference:
        conference = Conference(**conference_in.model_dump())
        self.db.add(conference)
        self.db.commit()
        self.db.refresh(conference)
        return conference

    def update(self, db_conference: Conference, conference_in: ConferenceUpdate) -> Conference:
        update_data = conference_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_conference, key, value)
        self.db.add(db_conference)
        self.db.commit()
        self.db.refresh(db_conference)
        return db_conference

    def delete(self, conference_id: int) -> bool:
        conference = self.db.get(Conference, conference_id)
        if conference:
            self.db.delete(conference)
            self.db.commit()
            return True
        return False
