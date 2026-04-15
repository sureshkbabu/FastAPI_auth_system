from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.middleware.rate_limit import login_rate_limiter

from app.core.security import (
    create_access_token,
    create_refresh_token,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(User).where(User.email == user_in.email)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Hash password
    hashed_password = hash_password(user_in.password)

    user = User(
        email = user_in.email,
        hashed_password = hashed_password
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

@router.post("/login")
async def login_user(
    request: Request,
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    login_rate_limiter(request)
    result = await db.execute(
        select(User).where(User.email == user_in.email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
        )

    access_token = create_access_token(subject = str(user.id),
                                       role = user.role)
    refresh_token = create_refresh_token(str(user.id))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
