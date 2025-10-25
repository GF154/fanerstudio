#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⏱️ Rate Limiting
Sistèm pou limite kantite requests
"""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from typing import Callable
import os

# ============================================================
# RATE LIMITER CONFIGURATION
# ============================================================

# Rate limit storage (Redis if available, else memory)
REDIS_URL = os.getenv("REDIS_URL", None)

if REDIS_URL:
    # Use Redis for distributed rate limiting
    from slowapi.middleware import SlowAPIMiddleware
    storage_uri = REDIS_URL
    print("✅ Rate Limiter: Using Redis storage (distributed)")
else:
    # Use in-memory storage (single instance only)
    storage_uri = "memory://"
    print("⚠️  Rate Limiter: Using memory storage (single instance)")


# Custom key function that considers authenticated user
def get_rate_limit_key(request: Request) -> str:
    """
    Generate rate limit key based on user or IP
    
    - If authenticated: use user_id
    - If not authenticated: use IP address
    
    Args:
        request: FastAPI request object
    
    Returns:
        Rate limit key (user_id or IP)
    """
    # Try to get user from request state (set by auth middleware)
    user = getattr(request.state, "user", None)
    
    if user and user.get("user_id"):
        # Authenticated user - use user_id
        return f"user:{user['user_id']}"
    else:
        # Anonymous user - use IP address
        return f"ip:{get_remote_address(request)}"


# Initialize limiter
limiter = Limiter(
    key_func=get_rate_limit_key,
    storage_uri=storage_uri,
    default_limits=["100/minute", "1000/hour", "5000/day"]  # Global limits
)


# ============================================================
# CUSTOM RATE LIMIT DECORATORS
# ============================================================

def rate_limit(limit: str):
    """
    Custom rate limit decorator
    
    Usage:
        @app.get("/api/endpoint")
        @rate_limit("10/minute")
        async def my_endpoint():
            return {"status": "ok"}
    
    Args:
        limit: Rate limit string (e.g., "10/minute", "100/hour")
    
    Returns:
        Decorator function
    """
    return limiter.limit(limit)


# Predefined rate limits for different use cases
rate_limit_strict = rate_limit("5/minute")      # Very strict (5 req/min)
rate_limit_normal = rate_limit("30/minute")     # Normal (30 req/min)
rate_limit_relaxed = rate_limit("100/minute")   # Relaxed (100 req/min)
rate_limit_generous = rate_limit("300/minute")  # Generous (300 req/min)


# ============================================================
# CUSTOM EXCEPTION HANDLER
# ============================================================

def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """
    Custom handler for rate limit exceeded
    
    Returns Kreyòl error message
    """
    return {
        "error": "Rate limit exceeded",
        "message": "Ou fè twòp requests! Tanpri tann yon ti moman.",
        "detail": "Too many requests. Please wait a moment.",
        "retry_after": exc.detail
    }


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def get_rate_limit_stats(key: str) -> dict:
    """
    Get rate limit statistics for a key
    
    Args:
        key: Rate limit key (user_id or IP)
    
    Returns:
        Dictionary with rate limit stats
    """
    try:
        # This is a simplified version
        # In production, you'd query the actual rate limit storage
        return {
            "key": key,
            "limits": limiter._default_limits,
            "storage": "redis" if REDIS_URL else "memory"
        }
    except Exception as e:
        return {"error": str(e)}


def reset_rate_limit(key: str) -> bool:
    """
    Reset rate limit for a specific key
    (Admin function)
    
    Args:
        key: Rate limit key to reset
    
    Returns:
        True if successful
    """
    try:
        # This would need to be implemented based on the storage backend
        # For now, just return True
        return True
    except Exception as e:
        print(f"Error resetting rate limit: {e}")
        return False


if __name__ == "__main__":
    print("⏱️  Rate Limiter Initialized")
    print("=" * 60)
    print(f"Storage: {'Redis' if REDIS_URL else 'Memory'}")
    print(f"Default limits: {limiter._default_limits}")
    print("=" * 60)
    print("\nExample usage:")
    print("""
    from app.rate_limiter import rate_limit, rate_limit_strict
    
    @app.post("/api/audiobook")
    @rate_limit("10/hour")  # Custom limit
    async def create_audiobook():
        ...
    
    @app.post("/api/translate")
    @rate_limit_normal  # Predefined normal limit
    async def translate():
        ...
    """)

