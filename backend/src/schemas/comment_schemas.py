from pydantic import BaseModel, Field
from datetime import datetime


class CommentCreate(BaseModel):
    body: str = Field(..., min_length=1)


class CommentOut(BaseModel):
    id: int
    body: str
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True
