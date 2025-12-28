from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.database import Base
from .association import article_tags

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    description = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    slug = Column(String(400), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    author_id = Column(Integer, nullable=False)

    comments = relationship(
        "Comment",
        back_populates="article",
        cascade="all, delete-orphan"
    )

    tags = relationship(
        "Tag",
        secondary=article_tags,
        back_populates="articles",
        passive_deletes=True
    )
