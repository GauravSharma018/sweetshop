from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models
from app.auth import hash_password
from app.database import SessionLocal
from app.schemas import UserCreate, UserResponse
from app.deps import get_db

router = APIRouter(
    tags=["auth"]
)

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(models.User)
        .filter(models.User.username == user.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = models.User(
        username=user.username,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

from app.auth import verify_password, create_access_token
from app.schemas import LoginRequest, TokenResponse


@router.post(
    "/login",
    response_model=TokenResponse
)
def login_user(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(models.User.username == credentials.username)
        .first()
    )

    if not user or not verify_password(
        credentials.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token(
    data={
        "sub": user.username,
        "is_admin": user.is_admin
    }
    )


    return {
        "access_token": token,
        "token_type": "bearer"
    }
