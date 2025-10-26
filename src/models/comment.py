from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)

    author = relationship("User", back_populates="comments")
    article = relationship("Article", back_populates="comments")
