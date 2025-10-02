from sqlalchemy import create_engine # @UnresolvedImport
from sqlalchemy.orm import declarative_base, sessionmaker # @UnresolvedImport

DatabaseURL = "sqlite:///./test.db"

engine = create_engine(DatabaseURL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()