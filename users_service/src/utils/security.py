from passlib.utils import to_bytes
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException
from src.config import Settings

ACCESS_TOKEN_EXPIRE_MINUTES = Settings.ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = Settings.JWT_SECRET
ALGORITHM = Settings.JWT_ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # Конвертируем в байты и усекаем до 72 байт
    truncated_bytes = to_bytes(password)[:72]
    return pwd_context.hash(truncated_bytes)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Также конвертируем при проверке в байты
    truncated_bytes = to_bytes(plain_password)[:72]
    return pwd_context.verify(truncated_bytes, hashed_password)


def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    """
    Декодирует JWT токен и возвращает полезные данные.
    В случае ошибки выбрасывает HTTPException.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )