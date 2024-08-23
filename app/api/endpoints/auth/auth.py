from datetime import timedelta

from fastapi import HTTPException
from fastapi import APIRouter
from starlette import status

from app.api.schemas.users import UserCreate, Token, UserLogin
from app.config.settings import settings
from app.core.services.auth import create_access_token
from app.core.services.users import UsersService
from app.extensions.helpers import verify_password

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register(user_data: UserCreate):
    users_service = UsersService()

    # Перевірка, чи існує користувач з таким ім'ям
    existing_user = await users_service.get_first(
        filter_data={"username": user_data.username}
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Якщо користувач не існує, створюємо нового
    await users_service.create_user(user_data=user_data.dict())

    return {"msg": "User registered"}


@router.post("/login", response_model=Token)
async def login_for_access_token(user_data: UserLogin):
    users_service = UsersService()

    user = await users_service.get_first(filter_data={"username": user_data.username})

    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
