from fastapi import APIRouter, HTTPException

from src.api.schemas.user import UserCreate, UserLogin, UserRead
from src.core.security import Hasher, create_access_token
from src.db.crud import add_user, get_user_by_username
from src.db.models import UserDB

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
async def register_user(data: UserCreate) -> UserRead:
    existing = await get_user_by_username(data.username)
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    user = UserDB(
        username=data.username,
        password_hash=Hasher.get_hash(data.password),
        email=data.email
    )
    user = await add_user(user)
    return UserRead(id=user.id, username=user.username, email=user.email)


@router.post("/login")
async def login_user(data: UserLogin):
    user = await get_user_by_username(data.username)
    if not user or not Hasher.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")
    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}


