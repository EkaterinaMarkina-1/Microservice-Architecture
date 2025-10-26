from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    bio = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

    articles = relationship(
        "Article",
        back_populates="author",
        cascade="all, delete-orphan"  
    )

    comments = relationship(
        "Comment",
        back_populates="author",
        cascade="all, delete-orphan" 
    )
