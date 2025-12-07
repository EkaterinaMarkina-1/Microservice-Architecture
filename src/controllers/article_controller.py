from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException

from src.models import Article, Tag
from src.utils.slug import slugify


async def _process_tags(db: AsyncSession, tag_list: list | None):
    """Возвращает список Tag объектов, создавая недостающие."""
    if not tag_list:
        return []

    tags = []
    for tag_name in tag_list:
        q = await db.execute(select(Tag).where(Tag.name == tag_name))
        tag = q.scalar_one_or_none()

        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            await db.flush()

        tags.append(tag)

    return tags


async def create_article(
    db: AsyncSession,
    user_id: int,
    title: str,
    description: str,
    body: str,
    tag_list: list | None = None
) -> Article:

    slug = slugify(title)

    # Проверяем уникальность slug
    q = await db.execute(select(Article).where(Article.slug == slug))
    if q.scalar_one_or_none():
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
    return article


async def get_article_by_slug(db: AsyncSession, slug: str) -> Article:
    q = await db.execute(select(Article).where(Article.slug == slug))
    article = q.scalar_one_or_none()
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    return article


async def update_article(
    db: AsyncSession,
    slug: str,
    user_id: int,
    title: str | None = None,
    description: str | None = None,
    body: str | None = None,
    tag_list: list | None = None
) -> Article:
    article = await get_article_by_slug(db, slug)

    if article.author_id != user_id:
        raise HTTPException(status_code=403, detail="Нет доступа")

    if title:
        article.title = title
        article.slug = slugify(title)

    if description:
        article.description = description

    if body:
        article.body = body

    if tag_list is not None:
        article.tags = await _process_tags(db, tag_list)

    await db.commit()
    await db.refresh(article)
    return article


async def delete_article(db: AsyncSession, slug: str, user_id: int):
    article = await get_article_by_slug(db, slug)

    if article.author_id != user_id:
        raise HTTPException(status_code=403, detail="Нет доступа")

    await db.delete(article)
    await db.commit()


async def list_articles(db: AsyncSession, page: int = 1, per_page: int = 15):
    offset = (page - 1) * per_page

    q = await db.execute(select(Article))
    total = len(q.scalars().all())

    q = await db.execute(
        select(Article).offset(offset).limit(per_page)
    )
    articles = q.scalars().all()

    return articles, total, page
