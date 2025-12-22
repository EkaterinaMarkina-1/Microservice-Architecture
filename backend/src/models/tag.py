from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base
from .association import article_tags


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)

    articles = relationship(
        "Article",
        secondary=article_tags,
        back_populates="tags",
        passive_deletes=True
    )
