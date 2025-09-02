from pydantic import BaseModel
from typing import Optional

class PublicationBase(BaseModel):
    title: str
    description: Optional[str] = None
    year: Optional[int] = None
    doi: Optional[str] = None

class PublicationCreate(PublicationBase):
    pass

class PublicationUpdate(PublicationBase):
    pass

class Publication(PublicationBase):
    id: int
    class Config:
        orm_mode = True
