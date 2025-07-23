from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from jeffersonlab_phonebook.db.models import Member


class MemberRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_sub(self, sub: str) -> Member | None:
        return self.db.scalar(
            select(Member).where(Member.experimental_data["sub"].astext == sub)
        )

    def create(self, userinfo: dict, institution_id: int) -> Member:
        member = Member(
            first_name=userinfo.get("given_name"),
            last_name=userinfo.get("family_name"),
            orcid=userinfo.get("orcid"),
            institution_id=institution_id,
            experimental_data={
                "sub": userinfo.get("sub"),
                "idp_name": userinfo.get("idp_name"),
            },
        )
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member

    def get_all(self) -> list[Member]:
        """
        Retrieves all members from the database.
        Includes eager loading of the 'institution' relationship for nested serialization.
        """
        # If your MemberResponse schema includes 'institution', you should eager load it
        # to prevent N+1 query problems.
        # # Import this at the top of the file
        return list(
            self.db.scalars(
                select(Member).options(joinedload(Member.institution))
            ).all()
        )

        # If you don't need institution details in the list, a simple select is fine:
        # return self.db.scalars(select(Member)).all()
