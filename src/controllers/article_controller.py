from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.models import Article
from sqlalchemy import select

async def create_article(
    db: AsyncSession,
    user_id: int,
    title: str,
    description: str,
    body: str,
    tag_list: list | None = None
) -> Article:
    article = Article(
        author_id=user_id,
        title=title,
        description=description,
        body=body,
        slug=generate_slug(title),
        tags=tag_list or []
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
        raise HTTPException(status_code=403, detail="Нет доступа для изменения статьи")

    if title is not None:
        article.title = title
    if description is not None:
        article.description = description
    if body is not None:
        article.body = body
    if tag_list is not None:
        article.tags = tag_list

    await db.commit()
    await db.refresh(article)
    return article

async def list_articles(db: AsyncSession, page: int = 1, per_page: int = 15):
    offset = (page - 1) * per_page
    result = await db.execute(select(Article).offset(offset).limit(per_page))
    articles = result.scalars().all()
    return articles, None, None


async def delete_article(db: AsyncSession, slug: str, user_id: int):
    article = await get_article_by_slug(db, slug)
    if article.author_id != user_id:
        raise HTTPException(status_code=403, detail="Нет доступа для удаления статьи")

    await db.delete(article)
    await db.commit()
