from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from src.models.user import User


class UserCreate(BaseModel):
    """Схема регистрации пользователя"""
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    username: str = Field(
        ..., min_length=3, max_length=150, pattern=r"^[a-zA-Z0-9_]+$", example="user",
        description="Имя пользователя (может содержать английские буквы, цифры и подчеркивания, уникальное)"
    )
    password: str = Field(..., min_length=6, example="password",
                          description="Пароль пользователя")
    bio: Optional[str] = Field(
        None, example="Привет! Я новый пользователь.", description="Краткая биография")
    image_url: Optional[str] = Field(
        None, example="https://example.com/avatar.jpg", description="URL аватара")


class UserLogin(BaseModel):
    """Схема входа пользователя"""
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=6,
                          example="password", description="Пароль")


class UserUpdate(BaseModel):
    """Схема обновления данных пользователя"""
    email: Optional[EmailStr] = Field(
        None, description="Новая электронная почта")
    username: Optional[str] = Field(
        None, min_length=3, max_length=150, pattern=r"^[a-zA-Z0-9_]+$", example="new_user",
        description="Новое имя пользователя"
    )
    password: Optional[str] = Field(
        None, min_length=6, example="newpassword", description="Новый пароль")
    bio: Optional[str] = Field(
        None, example="Обновленная биография", description="Обновленная биография")
    image_url: Optional[str] = Field(
        None, example="https://example.com/new_avatar.jpg", description="Новый URL аватара")
    model_config = ConfigDict(extra="forbid")

class UserOut(BaseModel):
    """Схема вывода данных авторизованного пользователя"""
    id: int
    updated_at: datetime = Field(...,
                                 description="Дата и время последнего обновления")
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    username: str = Field(..., description="Имя пользователя")
    bio: Optional[str] = Field(None, description="Краткая биография")
    image_url: Optional[str] = Field(
        None, description="URL аватара пользователя")
    subscription_key: Optional[str] = Field(
        None,
        description="Ключ для получения push-уведомлений",
        example="bb779f9b-44b3-48e7-9576-bbdf7884cbb1"
    )
    class Config:
        from_attributes = True


class ProfileOut(BaseModel):
    """Схема вывода данных публичного профиля пользователя"""
    username: str
    bio: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_user(cls, user: Optional[User]) -> "ProfileOut":
        if user is None or getattr(user, "is_deleted", False):
            return cls(username="deleted_user")
        return cls.from_orm(user)


class TokenResponse(BaseModel):
    """Схема ответа с JWT токеном"""
    access_token: str = Field(..., description="JWT токен доступа")
    token_type: str = Field("bearer", description="Тип токена")
