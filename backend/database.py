from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from ai_platform.config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_size=10, max_overflow=20)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models  # Import models to ensure they are known to SQLAlchemy
    Base.metadata.create_all(bind=engine)