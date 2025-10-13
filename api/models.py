"""
Data models for the REST API
Pydantic models for request/response validation
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator

# ==================== USER MODELS ====================


class UserBase(BaseModel):
    """Base user model"""

    username: str = Field(
        ..., min_length=3, max_length=50, description="Unique username"
    )
    email: EmailStr = Field(..., description="Valid email address")
    full_name: Optional[str] = Field(
        None, max_length=100, description="User's full name"
    )


class UserCreate(UserBase):
    """Model for user registration"""

    password: str = Field(
        ..., min_length=8, description="Strong password (min 8 characters)"
    )

    @validator("password")
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v

    @validator("username")
    def validate_username(cls, v):
        """Validate username format"""
        if not v.isalnum() and "_" not in v:
            raise ValueError(
                "Username can only contain letters, numbers, and underscores"
            )
        return v


class UserResponse(UserBase):
    """Model for user response (no password)"""

    disabled: bool = False

    class Config:
        from_attributes = True


class User(UserBase):
    """Internal user model with hashed password"""

    hashed_password: str
    disabled: bool = False


# ==================== TOKEN MODELS ====================


class Token(BaseModel):
    """JWT token response"""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class TokenData(BaseModel):
    """Token payload data"""

    username: Optional[str] = None


# ==================== ITEM MODELS ====================


class ItemBase(BaseModel):
    """Base item model"""

    title: str = Field(..., min_length=1, max_length=100, description="Item title")
    description: Optional[str] = Field(
        None, max_length=500, description="Item description"
    )


class ItemCreate(ItemBase):
    """Model for creating an item"""

    pass


class Item(ItemBase):
    """Complete item model with metadata"""

    id: int = Field(..., description="Unique item ID")
    owner: str = Field(..., description="Username of the owner")
    created_at: str = Field(..., description="Creation timestamp")

    class Config:
        from_attributes = True


# ==================== RESPONSE MODELS ====================


class MessageResponse(BaseModel):
    """Generic message response"""

    status: str = Field(..., description="Response status")
    message: str = Field(..., description="Response message")
    timestamp: Optional[str] = Field(None, description="Response timestamp")


class ErrorResponse(BaseModel):
    """Error response model"""

    detail: str = Field(..., description="Error detail")
    status_code: int = Field(..., description="HTTP status code")
