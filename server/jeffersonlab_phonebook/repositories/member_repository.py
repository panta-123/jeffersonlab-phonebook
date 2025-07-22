from sqlalchemy import select
from sqlalchemy.orm import Session

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
                "email": userinfo.get("email"),
                "idp_name": userinfo.get("idp_name"),
            },
        )
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        return member
