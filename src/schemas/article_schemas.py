from typing import List, Optional
from pydantic import BaseModel, Field


# ---------- Input Schemas ----------

class ArticleBase(BaseModel):
    title: str = Field(..., max_length=300)
    description: str = Field(..., max_length=500)
    body: str


class ArticleCreate(ArticleBase):
    tagList: Optional[List[str]] = None


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=300)
    description: Optional[str] = Field(None, max_length=500)
    body: Optional[str] = None
    tagList: Optional[List[str]] = None


# ---------- Output Schemas ----------

class ArticleOut(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    author_id: int
    tagList: List[str] = []

    class Config:
        from_attributes = True


class ArticleListItem(BaseModel):
    slug: str
    title: str
    author_id: int

    class Config:
        from_attributes = True
