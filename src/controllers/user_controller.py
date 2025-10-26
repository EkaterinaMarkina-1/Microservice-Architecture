from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User

async def create_user(
    db: AsyncSession,
    email: str,
    username: str,
    password: str,
    bio: Optional[str] = None,
    image_url: Optional[str] = None
) -> User:
    user = User(
        email=email,
        username=username,
        password=password,
        bio=bio,
        image_url=image_url
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    q = await db.execute(select(User).where(User.id == user_id))
    user = q.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    q = await db.execute(select(User).where(User.email == email))
    return q.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    q = await db.execute(select(User).where(User.username == username))
    return q.scalar_one_or_none()

async def get_all_users(db: AsyncSession) -> List[User]:
    q = await db.execute(select(User))
    return q.scalars().all()

async def update_user(
    db: AsyncSession,
    user_id: int,
    email: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    bio: Optional[str] = None,
    image_url: Optional[str] = None
) -> User:
    user = await get_user_by_id(db, user_id)

    if email is not None:
        user.email = email
    if username is not None:
        user.username = username
    if password is not None:
        user.password = password
    if bio is not None:
        user.bio = bio
    if image_url is not None:
        user.image_url = image_url

    await db.commit()
    await db.refresh(user)
    return user

async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user_by_id(db, user_id)
    await db.delete(user)
    await db.commit()
    return {"detail": "Пользователь удалён"}
