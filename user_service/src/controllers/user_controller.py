from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import User
from src.schemas.user_schemas import UserCreate
from src.utils.security import hash_password, verify_password


# ------------------ CREATE USER ------------------
async def create_user(db: AsyncSession, data: UserCreate) -> User:
    existing = await get_user_by_email(db, data.email)
    if existing:
        raise HTTPException(
            status_code=400, detail="Email уже зарегистрирован")

    new_user = User(
        email=data.email,
        username=data.username,
        password=hash_password(data.password),
        bio=data.bio,
        image_url=data.image_url
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# ------------------ LOGIN / AUTH ------------------
async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=401, detail="Неверный email или пароль")
    return user


# ------------------ GET USER BY ID ------------------
async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    q = await db.execute(select(User).where(User.id == user_id))
    user = q.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


# ------------------ GET USER BY EMAIL ------------------
async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    q = await db.execute(select(User).where(User.email == email))
    return q.scalar_one_or_none()


# ------------------ GET ALL USERS ------------------
async def get_all_users(db: AsyncSession) -> List[User]:
    q = await db.execute(select(User))
    return q.scalars().all()


# ------------------ UPDATE USER ------------------
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
        user.password = hash_password(password)
    if bio is not None:
        user.bio = bio
    if image_url is not None:
        user.image_url = image_url

    await db.commit()
    await db.refresh(user)
    return user


# ------------------ DELETE USER ------------------
async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user_by_id(db, user_id)
    await db.delete(user)
    await db.commit()
