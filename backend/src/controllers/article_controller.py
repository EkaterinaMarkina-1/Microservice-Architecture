from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Article, Tag
from src.utils.slug import slugify
from src.utils.tasks import notify_followers

# ------------------ INTERNAL: PROCESS TAGS ------------------


async def _process_tags(db: AsyncSession, tag_list: Optional[List[str]] = None) -> List[Tag]:
    """Возвращает список Tag объектов, создавая недостающие."""
    if not tag_list:
        return []

    tags: List[Tag] = []
    for tag_name in tag_list:
        q = await db.execute(select(Tag).where(Tag.name == tag_name))
        tag = q.scalar_one_or_none()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            await db.flush()
        tags.append(tag)

    return tags


# ------------------ CREATE ARTICLE ------------------
async def create_article(
    db: AsyncSession,
    user_id: int,
    title: str,
    description: str,
    body: str,
    tag_list: Optional[List[str]] = None
) -> Article:
    slug = slugify(title)

    existing = await get_article_by_slug(db, slug, raise_if_missing=False)
    if existing:
        raise HTTPException(
            status_code=400, detail="Статья с таким названием уже существует")

    tags = await _process_tags(db, tag_list)

    article = Article(
        author_id=user_id,
        title=title,
        description=description,
        body=body,
        slug=slug,
        tags=tags
    )

    db.add(article)
    await db.commit()
    await db.refresh(article)

    notify_followers.delay(
            author_id=user_id,
            post_id=article.id,
            post_title= article.title
    )
    return article

# ------------------ GET ARTICLE BY SLUG ------------------
async def get_article_by_slug(db: AsyncSession, slug: str, raise_if_missing: bool = True) -> Optional[Article]:
    q = await db.execute(select(Article).where(Article.slug == slug).options(selectinload(Article.tags)))
    article = q.scalar_one_or_none()
    if raise_if_missing and not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    return article


# ------------------ GET ARTICLE BY ID ------------------
async def get_article_by_id(db: AsyncSession, article_id: int, raise_if_missing: bool = True) -> Optional[Article]:
    q = await db.execute(select(Article).where(Article.id == article_id).options(selectinload(Article.tags)))
    article = q.scalar_one_or_none()
    if raise_if_missing and not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    return article


# ------------------ UPDATE ARTICLE ------------------
async def update_article(
    db: AsyncSession,
    slug: str,
    user_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    body: Optional[str] = None,
    tag_list: Optional[List[str]] = None
) -> Article:
    article = await get_article_by_slug(db, slug)

    if article.author_id != user_id:
        raise HTTPException(status_code=403, detail="Нет доступа")

    if title:
        article.title = title
        article.slug = slugify(title)
    if description is not None:
        article.description = description
    if body is not None:
        article.body = body
    if tag_list is not None:
        tags = await _process_tags(db, tag_list)
        article.tags.clear()
        article.tags.extend(tags)

    await db.commit()
    await db.refresh(article)
    return article


# ------------------ DELETE ARTICLE ------------------
async def delete_article(db: AsyncSession, slug: str, user_id: int):
    article = await get_article_by_slug(db, slug)

    if article.author_id != user_id:
        raise HTTPException(status_code=403, detail="Нет доступа")

    await db.delete(article)
    await db.commit()


# ------------------ LIST ARTICLES ------------------
async def list_articles(db: AsyncSession, page: int = 1, per_page: int = 15):
    offset = (page - 1) * per_page

    q = await db.execute(select(Article))
    total = len(q.scalars().all())

    q = await db.execute(select(Article).offset(offset).limit(per_page))
    articles = q.scalars().all()

    return articles, total, page
