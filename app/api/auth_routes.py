"""
Authentication API Routes

Handles user registration, login authentication, JWT token generation,
and current user profile verification.
"""

from __future__ import annotations

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.schemas import TokenResponse, UserLogin, UserRegister
from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    create_access_token,
    get_current_user_email,
    get_password_hash,
    verify_password,
)
from app.db.models import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
)
async def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    """
    Creates a new user account and returns a valid JWT access token.
    """
    # Check if email is already registered
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists.",
        )

    # Hash password and store new user
    hashed_pwd = get_password_hash(user_data.password)
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hashed_pwd,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.email},
        expires_delta=access_token_expires,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=new_user.id,
        email=new_user.email,
        user_name=new_user.full_name,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Log in with JSON payload",
)
async def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Authenticates a user via JSON body (used by frontend JavaScript) and returns a JWT token.
    """
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        user_name=user.full_name,
    )


@router.post(
    "/token",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Log in with OAuth2 Form Data (Swagger UI)",
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    OAuth2 compatible token login endpoint (used automatically by Swagger UI at /docs).
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        user_name=user.full_name,
    )


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get current logged-in user profile",
)
async def get_me(
    current_user_email: str = Depends(get_current_user_email),
    db: Session = Depends(get_db),
):
    """
    Returns current user details based on the provided Bearer JWT token.
    """
    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found.",
        )

    return {
        "user_id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "created_at": user.created_at,
    }