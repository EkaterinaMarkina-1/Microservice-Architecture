from fastapi import Header, HTTPException
from src.utils.security import decode_access_token

async def get_current_user_id(authorization: str = Header(...)) -> int:
    """Возвращает ID текущего пользователя из Bearer токена"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Требуется токен")
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    return payload["sub"]

def check_author(obj, user_id: int):
    """Проверка авторства: выбрасывает 403, если пользователь не является автором объекта"""
    if getattr(obj, "author_id", None) != user_id:
        raise HTTPException(status_code=403, detail="Нет доступа")
