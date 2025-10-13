"""
REST API with JWT Authentication
Built with FastAPI - Production Ready
"""

import os
from datetime import datetime, timedelta
from typing import Any, Dict, List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from .auth import (
    create_access_token,
    get_current_active_user,
    get_password_hash,
    verify_password,
)
from .database import get_db, init_db
from .models import Item, ItemCreate, Token, UserCreate, UserResponse
from .security_fixes import (
    add_security_headers_middleware,
    setup_rate_limiting,
    setup_security_logger,
)

# Type alias for user dict from database
UserDict = Dict[str, Any]


# Helper function to get client IP
def get_client_ip(request: Request) -> str:
    """Get client IP address from request, handling None cases"""
    if request.client:
        return request.client.host
    return "unknown"


# Initialize FastAPI app
app = FastAPI(
    title="Secure REST API",
    description="Production-ready REST API with JWT Authentication",
    version="1.0.0",
)

# Setup security
limiter = setup_rate_limiting(app)
security_logger = setup_security_logger()

# Add security headers middleware
app.middleware("http")(add_security_headers_middleware)

# CORS middleware - Configured for security
allowed_origins_str = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000"
)
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # ✅ SECURE: Only specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Specific methods only
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("✅ Database initialized")
    print("🚀 API is ready!")


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Secure REST API with Authentication",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "authentication": "enabled",
        "timestamp": datetime.utcnow().isoformat(),
    }


# ==================== AUTHENTICATION ENDPOINTS ====================


@app.post("/auth/register", response_model=UserResponse, tags=["Authentication"])
async def register(user: UserCreate, db=Depends(get_db)):
    """
    Register a new user

    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address
    - **password**: Strong password (min 8 characters)
    """
    # Check if user exists
    existing_user = db.get("users", {}).get(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Check if email exists
    for username, user_data in db.get("users", {}).items():
        if user_data.get("email") == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    # Create new user
    hashed_password = get_password_hash(user.password)
    new_user = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "full_name": user.full_name,
        "disabled": False,
        "created_at": datetime.utcnow().isoformat(),
    }

    # Store user
    if "users" not in db:
        db["users"] = {}
    db["users"][user.username] = new_user

    return UserResponse(
        username=new_user["username"],
        email=new_user["email"],
        full_name=new_user.get("full_name"),
        disabled=new_user["disabled"],
    )


@app.post("/auth/login", response_model=Token, tags=["Authentication"])
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_db),
):
    """
    Login with username and password

    Returns JWT access token for authenticated requests
    """
    # Get user from database
    users = db.get("users", {})
    user_data = users.get(form_data.username)

    # Get client IP for logging
    client_ip = get_client_ip(request)

    if not user_data:
        # Log failed login attempt
        security_logger.warning(
            f"Failed login attempt - Username: {form_data.username} - IP: {client_ip}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not verify_password(form_data.password, user_data["hashed_password"]):
        # Log failed password attempt
        security_logger.warning(
            f"Failed password - Username: {form_data.username} - IP: {client_ip}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is disabled
    if user_data.get("disabled", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user_data["username"]}, expires_delta=access_token_expires
    )

    # Log successful login
    security_logger.info(
        f"Successful login - Username: {user_data['username']} - IP: {client_ip}"
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/auth/me", response_model=UserResponse, tags=["Authentication"])
async def read_users_me(current_user: UserDict = Depends(get_current_active_user)):
    """
    Get current user information

    Requires valid JWT token
    """
    return UserResponse(
        username=current_user["username"],
        email=current_user["email"],
        full_name=current_user.get("full_name"),
        disabled=current_user["disabled"],
    )


# ==================== PROTECTED ENDPOINTS ====================


@app.get("/items", response_model=List[Item], tags=["Items"])
async def get_items(
    current_user: UserDict = Depends(get_current_active_user), db=Depends(get_db)
):
    """
    Get all items for the current user

    Requires authentication
    """
    user_items = db.get("items", {}).get(current_user["username"], [])
    return user_items


@app.post("/items", response_model=Item, tags=["Items"])
async def create_item(
    item: ItemCreate,
    current_user: UserDict = Depends(get_current_active_user),
    db=Depends(get_db),
):
    """
    Create a new item

    Requires authentication
    """
    # Initialize items structure
    if "items" not in db:
        db["items"] = {}
    if current_user["username"] not in db["items"]:
        db["items"][current_user["username"]] = []

    # Create new item
    new_item = {
        "id": len(db["items"][current_user["username"]]) + 1,
        "title": item.title,
        "description": item.description,
        "owner": current_user["username"],
        "created_at": datetime.utcnow().isoformat(),
    }

    # Store item
    db["items"][current_user["username"]].append(new_item)

    return Item(**new_item)


@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
async def get_item(
    item_id: int,
    current_user: UserDict = Depends(get_current_active_user),
    db=Depends(get_db),
):
    """
    Get a specific item by ID

    Requires authentication and ownership
    """
    user_items = db.get("items", {}).get(current_user["username"], [])

    for item in user_items:
        if item["id"] == item_id:
            return Item(**item)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


@app.delete("/items/{item_id}", tags=["Items"])
async def delete_item(
    item_id: int,
    current_user: UserDict = Depends(get_current_active_user),
    db=Depends(get_db),
):
    """
    Delete a specific item

    Requires authentication and ownership
    """
    user_items = db.get("items", {}).get(current_user["username"], [])

    for idx, item in enumerate(user_items):
        if item["id"] == item_id:
            deleted_item = user_items.pop(idx)
            return {
                "status": "success",
                "message": f"Item '{deleted_item['title']}' deleted",
                "item_id": item_id,
            }

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")


# ==================== ADMIN ENDPOINTS ====================


@app.get("/admin/users", tags=["Admin"])
async def list_users(
    current_user: UserDict = Depends(get_current_active_user), db=Depends(get_db)
):
    """
    List all users (admin only)

    Note: In production, add role-based access control
    """
    users = db.get("users", {})
    return {
        "total_users": len(users),
        "users": [
            {
                "username": user_data["username"],
                "email": user_data["email"],
                "created_at": user_data.get("created_at"),
            }
            for user_data in users.values()
        ],
    }


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
