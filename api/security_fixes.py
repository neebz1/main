"""
Security Enhancements for API
Apply these fixes to improve security posture
"""

import logging
import re
import subprocess
from datetime import datetime
from typing import Callable, Optional

from fastapi import FastAPI, HTTPException, Request, status

# ==================== RATE LIMITING ====================


def setup_rate_limiting(app: FastAPI) -> Optional[object]:
    """
    Setup rate limiting for API endpoints

    Installation:
        pip install slowapi

    Usage in main.py:
        from .security_fixes import setup_rate_limiting

        setup_rate_limiting(app)

        # Then in your endpoints, add manual rate limiting checks

    Note: slowapi is optional. Install it separately if needed.
    For production, use a Redis-based rate limiter or API gateway.
    """
    try:
        from slowapi import Limiter, _rate_limit_exceeded_handler  # type: ignore
        from slowapi.errors import RateLimitExceeded  # type: ignore
        from slowapi.util import get_remote_address  # type: ignore

        limiter = Limiter(key_func=get_remote_address)
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        return limiter
    except ImportError:
        print(
            "⚠️  slowapi not installed. Rate limiting disabled. Install with: pip install slowapi"
        )
        return None


# ==================== SECURITY HEADERS ====================


async def add_security_headers_middleware(request: Request, call_next: Callable):
    """
    Add security headers to all responses

    Usage in main.py:
        from .security_fixes import add_security_headers_middleware

        app.middleware("http")(add_security_headers_middleware)
    """
    response = await call_next(request)

    # Prevent MIME type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"

    # Prevent clickjacking
    response.headers["X-Frame-Options"] = "DENY"

    # XSS protection
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # HSTS - Force HTTPS (only in production)
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )

    # Content Security Policy
    response.headers["Content-Security-Policy"] = "default-src 'self'"

    # Referrer policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # Permissions policy
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    return response


# ==================== ROLE-BASED ACCESS CONTROL ====================


async def get_current_admin_user(current_user: dict) -> dict:
    """
    Verify user has admin role

    Usage in main.py:
        from .security_fixes import get_current_admin_user

        @app.get("/admin/users")
        async def list_users(
            current_user: dict = Depends(get_current_admin_user)
        ):

    Note: You need to add 'role' field to User model first
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return current_user


# ==================== INPUT SANITIZATION ====================


def sanitize_project_name(name: str, max_length: int = 50) -> str:
    """
    Sanitize project name to prevent command injection

    Args:
        name: Project name to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized project name

    Raises:
        ValueError: If name contains invalid characters
    """
    # Remove leading/trailing whitespace
    name = name.strip()

    # Check for valid characters (alphanumeric, hyphens, underscores)
    if not re.match(r"^[a-zA-Z0-9-_]+$", name):
        raise ValueError(
            "Project name can only contain letters, numbers, hyphens, and underscores"
        )

    # Check length
    if len(name) == 0:
        raise ValueError("Project name cannot be empty")

    if len(name) > max_length:
        raise ValueError(f"Project name must be {max_length} characters or less")

    return name


def sanitize_git_commit_message(message: str, max_length: int = 200) -> str:
    """
    Sanitize git commit message

    Args:
        message: Commit message to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized commit message
    """
    # Remove potentially dangerous characters
    message = re.sub(r"[`$();&|<>]", "", message)

    # Limit length
    if len(message) > max_length:
        message = message[:max_length]

    # Escape quotes
    message = message.replace('"', '\\"').replace("'", "\\'")

    return message.strip()


def validate_file_path(
    file_path: str, allowed_extensions: Optional[list] = None
) -> bool:
    """
    Validate file path to prevent directory traversal

    Args:
        file_path: File path to validate
        allowed_extensions: List of allowed file extensions

    Returns:
        True if valid, False otherwise
    """
    # Prevent directory traversal
    if ".." in file_path or file_path.startswith("/"):
        return False

    # Check extension if specified
    if allowed_extensions:
        ext = file_path.split(".")[-1].lower()
        if ext not in allowed_extensions:
            return False

    return True


# ==================== SECRET DETECTION ====================


def detect_secrets(text: str) -> bool:
    """
    Detect potential secrets in text

    Args:
        text: Text to scan for secrets

    Returns:
        True if potential secrets found, False otherwise
    """
    secret_patterns = [
        r"sk-[a-zA-Z0-9]{32,}",  # OpenAI/Anthropic keys
        r"AIza[a-zA-Z0-9_-]{35}",  # Google API keys
        r"hf_[a-zA-Z0-9]{32,}",  # Hugging Face tokens
        r"sk-ant-[a-zA-Z0-9-_]{95}",  # Anthropic keys
        r"sk-or-[a-zA-Z0-9]{48}",  # OpenRouter keys
        r'(password|secret|api_key)\s*[:=]\s*["\'][\w-]{8,}["\']',  # Generic secrets
        r"Bearer [a-zA-Z0-9_-]{20,}",  # Bearer tokens
        r"postgres://[^:]+:[^@]+@",  # Database URLs with passwords
    ]

    for pattern in secret_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


# ==================== SECURE COMMAND EXECUTION ====================

ALLOWED_COMMANDS = {
    "git_status": ["git", "status"],
    "git_log": ["git", "log", "--oneline", "-10"],
    "git_branch": ["git", "branch"],
    "pytest_version": ["pytest", "--version"],
    "python_version": ["python", "--version"],
}


def execute_safe_command(command_key: str) -> tuple:
    """
    Execute a pre-approved safe command

    Args:
        command_key: Key from ALLOWED_COMMANDS

    Returns:
        Tuple of (success: bool, output: str)

    Usage:
        success, output = execute_safe_command('git_status')
    """
    if command_key not in ALLOWED_COMMANDS:
        return False, f"Command '{command_key}' not allowed"

    try:
        result = subprocess.run(
            ALLOWED_COMMANDS[command_key],
            capture_output=True,
            text=True,
            timeout=30,
            shell=False,  # IMPORTANT: shell=False prevents injection
        )

        success = result.returncode == 0
        output = result.stdout if success else result.stderr

        return success, output

    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, f"Error executing command: {str(e)}"


# ==================== LOGGING ====================


def setup_security_logger() -> logging.Logger:
    """
    Setup security event logger

    Usage in main.py:
        from .security_fixes import setup_security_logger

        security_logger = setup_security_logger()

        # Log security events
        security_logger.warning(f"Failed login: {username} from {ip}")
        security_logger.critical(f"Admin access denied: {username}")
    """
    logger = logging.getLogger("security")
    logger.setLevel(logging.INFO)

    # Create logs directory if it doesn't exist
    import os

    os.makedirs("logs", exist_ok=True)

    # File handler
    fh = logging.FileHandler(f"logs/security_{datetime.now().strftime('%Y%m%d')}.log")
    fh.setLevel(logging.INFO)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


# ==================== USAGE EXAMPLE ====================

"""
Example implementation in api/main.py:

```python
from .security_fixes import (
    setup_rate_limiting,
    add_security_headers_middleware,
    get_current_admin_user,
    setup_security_logger,
)

# Setup
app = FastAPI(...)
limiter = setup_rate_limiting(app)
security_logger = setup_security_logger()

# Add security headers
app.middleware("http")(add_security_headers_middleware)

# Apply rate limiting to login
@app.post("/auth/login")
@limiter.limit("5/minute")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Log failed attempts
    if not verify_password(...):
        security_logger.warning(
            f"Failed login: {form_data.username} from {request.client.host}"
        )
        raise HTTPException(...)
    ...

# Protect admin endpoints
@app.get("/admin/users")
async def list_users(
    current_user: dict = Depends(get_current_admin_user),
    db=Depends(get_db)
):
    security_logger.info(f"Admin access: {current_user['username']}")
    ...
```
"""
