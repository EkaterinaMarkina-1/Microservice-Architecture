from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.database import get_async_session
from src.schemas.user_schemas import UserCreate, UserLogin, UserOut, TokenResponse, UserUpdate
from src.utils.security import create_access_token, decode_access_token
from src.controllers.user_controller import (
    create_user,
    authenticate_user,
    get_user_by_id,
    update_user,
    delete_user as delete_user_ctrl
)
from utils.auth import get_current_user_id, check_author

router = APIRouter(prefix="/api", tags=["users"])


async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_async_session),
) -> UserOut:
    return await get_user_by_id(db, user_id)


#  Регистрация
@router.post("/users", response_model=UserOut, status_code=201,
             summary="Регистрация нового пользователя",
             description="Создает нового пользователя в системе.")
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_async_session)):
    return await create_user(db, user_data)


#  Логин
@router.post("/users/login", response_model=TokenResponse,
             summary="Вход в систему",
             description="Аутентифицирует пользователя и возвращает токен доступа.")
async def login_user(login_data: UserLogin, db: AsyncSession = Depends(get_async_session)):
    user = await authenticate_user(db, login_data.email, login_data.password)
    token_data = {"sub": str(
        user.id), "username": user.username, "email": user.email}
    access_token = create_access_token(token_data)
    return TokenResponse(access_token=access_token)


#  Получение текущего пользователя
@router.get("/user", response_model=UserOut,
            summary="Текущий пользователь",
            description="Возвращает информацию о текущем аутентифицированном пользователе.")
async def get_user(current_user: UserOut = Depends(get_current_user)):
    return current_user

# Обновление текущего пользователя


@router.put("/user", response_model=UserOut,
            summary="Обновление текущего пользователя",
            description="Обновляет информацию о текущем аутентифицированном пользователе.")
async def update_current_user(user_update: UserUpdate, current_user: UserOut = Depends(get_current_user),
                              db: AsyncSession = Depends(get_async_session)):
    return await update_user(
        db,
        user_id=current_user.id,
        email=user_update.email,
        username=user_update.username,
        password=user_update.password,
        bio=user_update.bio,
        image_url=user_update.image_url
    )


# Удаление текущего пользователя
@router.delete("/user", response_model=dict,
               summary="Удаление текущего пользователя",
               description="Удаляет текущего аутентифицированного пользователя.")
async def delete_current_user(current_user: UserOut = Depends(get_current_user),
                              db: AsyncSession = Depends(get_async_session)):
    await delete_user_ctrl(db, current_user.id)
    return {"detail": "User deleted successfully"}
