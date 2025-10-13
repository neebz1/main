"""
Authentication utilities
JWT token management and password hashing
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import settings
from .database import get_db

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ==================== PASSWORD FUNCTIONS ====================


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password

    Args:
        plain_password: The plain text password
        hashed_password: The hashed password from database

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt

    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


# ==================== JWT TOKEN FUNCTIONS ====================


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token

    Args:
        data: Dictionary containing token data (typically {"sub": username})
        expires_delta: Optional expiration time delta

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": "access"})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """
    Verify and decode a JWT token

    Args:
        token: JWT token string

    Returns:
        Username from token if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None


# ==================== DEPENDENCY FUNCTIONS ====================


async def get_current_user(
    token: str = Depends(oauth2_scheme), db=Depends(get_db)
) -> dict:
    """
    Get current user from JWT token

    Args:
        token: JWT token from Authorization header
        db: Database dependency

    Returns:
        User dictionary if valid

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify token
    username = verify_token(token)
    if username is None:
        raise credentials_exception

    # Get user from database
    users = db.get("users", {})
    user = users.get(username)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: dict = Depends(get_current_user),
) -> dict:
    """
    Get current active user (not disabled)

    Args:
        current_user: Current user from get_current_user

    Returns:
        User dictionary if active

    Raises:
        HTTPException: If user is disabled
    """
    if current_user.get("disabled", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


# ==================== UTILITY FUNCTIONS ====================


def authenticate_user(db: dict, username: str, password: str) -> Optional[dict]:
    """
    Authenticate a user with username and password

    Args:
        db: Database dictionary
        username: Username to authenticate
        password: Plain text password

    Returns:
        User dictionary if authenticated, None otherwise
    """
    users = db.get("users", {})
    user = users.get(username)

    if not user:
        return None

    if not verify_password(password, user["hashed_password"]):
        return None

    return user
