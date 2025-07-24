from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from jeffersonlab_phonebook.config.settings import settings
from jeffersonlab_phonebook.db.models import Base 


# For PostgreSQL: "postgresql://user:password@host:port/dbname"
# For SQLite: "sqlite:///./jeffersonlab_phonebook.db"
# mysql://user:password@host:port/dbname

SQLALCHEMY_DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create table if not exits
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
