from sqlalchemy import Column, Integer, String, Text
from ..db.session import Base

class Publication(Base):
    __tablename__ = "publications"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    year = Column(Integer, nullable=True)
    doi = Column(String, nullable=True)
