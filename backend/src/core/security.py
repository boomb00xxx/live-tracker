import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext

from src.core.config import settings
from src.db.crud import get_user_by_id


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class Hasher:

    @staticmethod
    def verify_password(plain_password, hashed_password):
        prepared = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
        return pwd_context.verify(prepared, hashed_password)

    @staticmethod
    def get_hash(password) -> str:
        prepared = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return pwd_context.hash(prepared)


def create_access_token(subject: str | int, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = {"sub": str(subject), "iat": int(datetime.now(timezone.utc).timestamp())}
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


http_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Требуется аутентификация")
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401, detail="Недействительный токен")
        user_id = int(sub)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Срок действия токена истёк")
    except (InvalidTokenError, ValueError):
        raise HTTPException(status_code=401, detail="Недействительный токен")

    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user

