from sqlalchemy.orm import Session
from ..db.publication_model import Publication
from ..schemas.publication_schemas import PublicationCreate, PublicationUpdate

class PublicationRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Publication).all()

    @staticmethod
    def get_by_id(db: Session, publication_id: int):
        return db.query(Publication).filter(Publication.id == publication_id).first()

    @staticmethod
    def create(db: Session, publication: PublicationCreate):
        db_publication = Publication(**publication.dict())
        db.add(db_publication)
        db.commit()
        db.refresh(db_publication)
        return db_publication

    @staticmethod
    def update(db: Session, publication_id: int, publication: PublicationUpdate):
        db_publication = db.query(Publication).filter(Publication.id == publication_id).first()
        if db_publication:
            for key, value in publication.dict(exclude_unset=True).items():
                setattr(db_publication, key, value)
            db.commit()
            db.refresh(db_publication)
        return db_publication

    @staticmethod
    def delete(db: Session, publication_id: int):
        db_publication = db.query(Publication).filter(Publication.id == publication_id).first()
        if db_publication:
            db.delete(db_publication)
            db.commit()
        return db_publication
