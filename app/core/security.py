# """
# Security utilities for TripMate AI.
# """

# from __future__ import annotations

# from datetime import datetime, timedelta, timezone
# from typing import Any

# import jwt

# from app.core.config import settings


# def create_access_token(
#     data: dict[str, Any],
#     expires_delta: timedelta | None = None,
# ) -> str:
#     """
#     Create a JWT access token.
#     """
#     payload = data.copy()

#     expire = datetime.now(timezone.utc) + (
#         expires_delta
#         or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     )

#     payload.update({"exp": expire})

#     return jwt.encode(
#         payload,
#         settings.SECRET_KEY,
#         algorithm=settings.JWT_ALGORITHM,
#     )


# def verify_access_token(
#     token: str,
# ) -> dict[str, Any]:
#     """
#     Verify and decode JWT token.
#     """
#     return jwt.decode(
#         token,
#         settings.SECRET_KEY,
#         algorithms=[settings.JWT_ALGORITHM],
#     )



# """
# Security and JWT Authentication Helpers
# """

# from __future__ import annotations

# from datetime import datetime, timedelta, timezone
# from typing import Optional

# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from passlib.context import CryptContext

# from app.core.config import settings

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)


# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + (
#         expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     )
#     to_encode.update({"exp": expire})
#     return jwt.encode(
#         to_encode,
#         settings.SECRET_KEY,
#         algorithm=settings.ALGORITHM,
#     )


# def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(
#             token,
#             settings.SECRET_KEY,
#             algorithms=[settings.ALGORITHM],
#         )
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         return email
#     except JWTError:
#         raise credentials_exception






# """
# Security and JWT Authentication Helpers
# """

# from __future__ import annotations

# from datetime import datetime, timedelta, timezone
# from typing import Optional

# import bcrypt
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt

# from app.core.config import settings

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """Verifies a plain text password against a stored bcrypt hash."""
#     pwd_bytes = plain_password.encode("utf-8")[:72]
#     hash_bytes = hashed_password.encode("utf-8")
#     return bcrypt.checkpw(pwd_bytes, hash_bytes)


# def get_password_hash(password: str) -> str:
#     """Hashes a password using bcrypt (truncates to 72 bytes safely)."""
#     pwd_bytes = password.encode("utf-8")[:72]
#     salt = bcrypt.gensalt()
#     return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
#     to_encode = data.copy()
#     expire = datetime.now(timezone.utc) + (
#         expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     )
#     to_encode.update({"exp": expire})
#     return jwt.encode(
#         to_encode,
#         settings.SECRET_KEY,
#         algorithm=settings.ALGORITHM,
#     )


# def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(
#             token,
#             settings.SECRET_KEY,
#             algorithms=[settings.ALGORITHM],
#         )
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         return email
#     except JWTError:
#         raise credentials_exception






"""
Security and JWT Authentication Helpers
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain text password against a stored bcrypt hash."""
    pwd_bytes = plain_password.encode("utf-8")[:72]
    hash_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(pwd_bytes, hash_bytes)


def get_password_hash(password: str) -> str:
    """Hashes a password using bcrypt (truncates to 72 bytes safely)."""
    pwd_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,  # Fixed: changed from settings.ALGORITHM
    )


def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],  # Fixed: changed from settings.ALGORITHM
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception