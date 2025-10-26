from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Tag

async def create_tag(db: AsyncSession, name: str) -> Tag:
    tag_name_clean = name.strip().lower()
    q = await db.execute(select(Tag).where(Tag.name == tag_name_clean))
    tag = q.scalar_one_or_none()
    if tag:
        return tag
    tag = Tag(name=tag_name_clean)
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


async def get_all_tags(db: AsyncSession) -> List[Tag]:
    q = await db.execute(select(Tag))
    return q.scalars().all()