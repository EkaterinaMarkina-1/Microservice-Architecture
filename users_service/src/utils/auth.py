from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.utils.security import decode_access_token

security = HTTPBearer()


async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    """Возвращает ID текущего пользователя из Bearer токена"""

    token = credentials.credentials

    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Нет доступа")

    return int(payload["sub"])


def check_author(obj, user_id: int):
    """Проверка авторства: выбрасывает 403, если пользователь не является автором объекта"""
    if getattr(obj, "author_id", None) != user_id:
        raise HTTPException(status_code=403, detail="Нет доступа")
