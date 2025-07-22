from sqlalchemy import select
from sqlalchemy.orm import Session

from jeffersonlab_phonebook.db.models import Institution


class InstitutionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, full_name: str) -> Institution | None:
        return self.db.scalar(
            select(Institution).where(Institution.full_name == full_name)
        )

    def create(self, name: str, userinfo: dict) -> Institution:
        institution = Institution(
            full_name=name,
            short_name=name,
            country=userinfo.get("country", "Unknown"),
            region=userinfo.get("region", "Unknown"),
            latitude=userinfo.get("latitude", None),
            longitude=userinfo.get("longitude", None),
            city=userinfo.get("city", None),
            address=userinfo.get("address", None),
        )
        self.db.add(institution)
        self.db.commit()
        self.db.refresh(institution)
        return institution
