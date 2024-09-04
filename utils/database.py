from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.config import load_config

config = load_config()
DATABASE_URL = config['database_url']

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()