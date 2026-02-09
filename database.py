from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Auth.models import Base

CONNECTION_DB = "postgresql://ilias:ilias@localhost:5433/authdb"

Engine = create_engine(CONNECTION_DB)

SessionLocal = sessionmaker(bind=Engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()



def create_tables():
    Base.metadata.create_all(Engine)
