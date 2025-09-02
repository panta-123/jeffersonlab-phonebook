from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...schemas.publication_schemas import Publication, PublicationCreate, PublicationUpdate
from ...repositories.publication_repository import PublicationRepository

router = APIRouter(prefix="/publications", tags=["publications"])

@router.get("/", response_model=list[Publication])
def get_publications(db: Session = Depends(get_db)):
    return PublicationRepository.get_all(db)

@router.get("/{publication_id}", response_model=Publication)
def get_publication(publication_id: int, db: Session = Depends(get_db)):
    publication = PublicationRepository.get_by_id(db, publication_id)
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    return publication

@router.post("/", response_model=Publication)
def create_publication(publication: PublicationCreate, db: Session = Depends(get_db)):
    return PublicationRepository.create(db, publication)

@router.put("/{publication_id}", response_model=Publication)
def update_publication(publication_id: int, publication: PublicationUpdate, db: Session = Depends(get_db)):
    updated = PublicationRepository.update(db, publication_id, publication)
    if not updated:
        raise HTTPException(status_code=404, detail="Publication not found")
    return updated

@router.delete("/{publication_id}", response_model=Publication)
def delete_publication(publication_id: int, db: Session = Depends(get_db)):
    deleted = PublicationRepository.delete(db, publication_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Publication not found")
    return deleted
