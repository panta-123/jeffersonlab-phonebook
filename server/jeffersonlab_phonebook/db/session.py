from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from jeffersonlab_phonebook.config.settings import settings
from jeffersonlab_phonebook.db.models import Base 


SQLALCHEMY_DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI)

# Replace with your actual database URL
# For PostgreSQL: "postgresql://user:password@host:port/dbname"
# For SQLite: "sqlite:///./jeffersonlab_phonebook.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./jeffersonlab_phonebook.db" # Using SQLite for simplicity

engine = create_engine(
    SQLALCHEMY_DATABASE_URL  # , connect_args={"check_same_thread": False} # Needed for SQLite
)

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
