from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserLogin(BaseModel):
    username: str
    password: str

