from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.schemas.user_schemas import (
    UserCreate,
    UserLogin,
    UserUpdate,
    UserOut,
    TokenResponse,
)
from src.schemas.common import DeleteResponse
from src.controllers import user_controller
from src.utils.auth import get_current_user_id
from src.utils.security import create_access_token


router = APIRouter(prefix="/api/users", tags=["users"])


# ---------- REGISTER ----------
async def register_user_dependency(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> UserOut:
    new_user = await user_controller.create_user(db, user_data)
    return UserOut.model_validate(new_user, from_attributes=True)


@router.post("", response_model=UserOut, status_code=201,
             summary="Зарегистрировать нового пользователя")
async def register(payload: UserOut = Depends(register_user_dependency)):
    return payload


# ---------- LOGIN ----------
async def login_user_dependency(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
) -> TokenResponse:
    user = await user_controller.authenticate_user(db, login_data.email, login_data.password)
    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse,
             summary="Войти в систему")
async def login(payload: TokenResponse = Depends(login_user_dependency)):
    return payload


# ---------- GET CURRENT USER ----------
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=403, detail="Invalid token")
        return int(user_id)

    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")


# ---------- UPDATE CURRENT USER ----------
async def update_current_user_dependency(
    update_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
) -> UserOut:
    updated = await user_controller.update_user(
        db,
        user_id,
        **update_data.dict(exclude_unset=True)
    )
    return UserOut.model_validate(updated, from_attributes=True)


@router.put("/me", response_model=UserOut,
            summary="Обновить текущего пользователя")
async def update_user(payload: UserOut = Depends(update_current_user_dependency)):
    return payload


# ---------- DELETE CURRENT USER ----------
async def delete_current_user_dependency(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
) -> DeleteResponse:
    await user_controller.delete_user(db, user_id)
    return DeleteResponse(detail="Пользователь удалён")


@router.delete("/me", response_model=DeleteResponse,
               summary="Удалить текущего пользователя")
async def delete_user(payload: DeleteResponse = Depends(delete_current_user_dependency)):
    return payload
