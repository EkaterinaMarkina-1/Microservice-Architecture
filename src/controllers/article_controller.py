from typing import List, Optional, Tuple
from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.models import Article, Tag, User

async def create_article(
    db: AsyncSession,
    author_id: int,
    title: str,
    description: str,
    body: str,
    slug: str,
    tag_list: Optional[List[str]] = None
) -> Article:
    article = Article(
        author_id=author_id,
        title=title,
        description=description,
        body=body,
        slug=slug,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    if tag_list:
        tags_objs = []
        for tag_name in tag_list:
            tag_name_clean = tag_name.strip().lower()
            q = await db.execute(select(Tag).where(Tag.name == tag_name_clean))
            tag = q.scalar_one_or_none()
            if not tag:
                tag = Tag(name=tag_name_clean)
                db.add(tag)
                await db.flush()
            tags_objs.append(tag)
        article.tags = tags_objs

    db.add(article)
    await db.commit()
    await db.refresh(article)
    return article


async def get_article_by_id(db: AsyncSession, article_id: int) -> Article:
    q = await db.execute(select(Article).where(Article.id == article_id))
    article = q.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    return article


async def get_article_by_slug(db: AsyncSession, slug: str) -> Article:
    q = await db.execute(select(Article).where(Article.slug == slug))
    article = q.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    return article


async def list_articles(
    db: AsyncSession,
    page: int = 1,
    per_page: int = 15
) -> Tuple[List[Article], int, int]:
    offset = (page - 1) * per_page
    q = await db.execute(select(Article).offset(offset).limit(per_page))
    articles = q.scalars().all()

    total_items = await db.scalar(select(func.count(Article.id)))
    total_pages = (total_items + per_page - 1) // per_page if total_items > 0 else 1
    return articles, total_items, total_pages


async def update_article(
    db: AsyncSession,
    article_id: int,
    author_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    body: Optional[str] = None,
    tag_list: Optional[List[str]] = None
) -> Article:
    article = await get_article_by_id(db, article_id)

    if article.author_id != author_id:
        raise HTTPException(status_code=403, detail="Нет доступа для редактирования этой статьи")

    if title:
        article.title = title
    if description:
        article.description = description
    if body:
        article.body = body
    if tag_list is not None:
        article.tags.clear()
        for tag_name in tag_list:
            tn = tag_name.strip().lower()
            q = await db.execute(select(Tag).where(Tag.name == tn))
            tag = q.scalar_one_or_none()
            if not tag:
                tag = Tag(name=tn)
                db.add(tag)
                await db.flush()
            article.tags.append(tag)

    article.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(article)
    return article


async def delete_article(db: AsyncSession, article_id: int, author_id: int):
    article = await get_article_by_id(db, article_id)
    if article.author_id != author_id:
        raise HTTPException(status_code=403, detail="Нет доступа для удаления статьи")
    await db.delete(article)
    await db.commit()
    return {"detail": "Статья удалена"}
