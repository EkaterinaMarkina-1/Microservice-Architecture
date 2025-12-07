from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.controllers import tag_controller as tags_ctrl

router = APIRouter(prefix="/api/tags", tags=["tags"])


@router.post("/", response_model=dict)
async def create_tag(name: str, db: AsyncSession = Depends(get_async_session)):
    tag = await tags_ctrl.create_tag(db, name)
    return {"id": tag.id, "name": tag.name}


@router.get("/", response_model=List[dict])
async def list_tags(db: AsyncSession = Depends(get_async_session)):
    tags = await tags_ctrl.get_all_tags(db)
    return [{"id": t.id, "name": t.name} for t in tags]
