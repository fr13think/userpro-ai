from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128))
    preferences = Column(JSON)
    prompts = relationship("Prompt", back_populates="user")
    conversations = relationship("Conversation", back_populates="user")

    def __repr__(self):
        return f'<User {self.username}>'