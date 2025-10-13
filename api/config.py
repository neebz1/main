"""
Configuration settings for the API
Environment variables and constants
"""

import os
from typing import Optional

from pydantic import BaseModel


class Settings(BaseModel):
    """Application settings"""

    # App Info
    APP_NAME: str = "Secure REST API"
    VERSION: str = "1.0.0"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: list = os.getenv(
        "ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000"
    ).split(",")

    # Database (for future SQL implementation)
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")

    # API Keys (if needed for external services)
    OPENROUTER_API_KEY: Optional[str] = os.getenv("OPENROUTER_API_KEY")

    class Config:
        case_sensitive = True


# Global settings instance
settings = Settings()

# Validate SECRET_KEY
if (
    not settings.SECRET_KEY
    or settings.SECRET_KEY
    == "your-secret-key-change-this-in-production-use-openssl-rand-hex-32"
):
    print("⚠️  WARNING: SECRET_KEY not set or using default!")
    print("   Generate a secure key with: openssl rand -hex 32")
    print("   Set in .env file: SECRET_KEY=<your-generated-key>")


# ==================== IMPORTANT: PRODUCTION SECURITY ====================
"""
⚠️  BEFORE DEPLOYING TO PRODUCTION:

1. Generate a secure SECRET_KEY:
   ```bash
   openssl rand -hex 32
   ```

2. Set as environment variable:
   ```bash
   export SECRET_KEY="your-generated-secret-key-here"
   ```

3. Update ALLOWED_ORIGINS in CORS settings:
   ```python
   ALLOWED_ORIGINS = ["https://yourdomain.com"]
   ```

4. Use HTTPS only in production

5. Set up proper database (PostgreSQL/MySQL)

6. Enable rate limiting

7. Add logging and monitoring

8. Configure proper error handling

9. Add input validation and sanitization

10. Implement refresh tokens for better security
"""
