#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔐 Authentication & Authorization
Sistèm otantifikasyon ak JWT
"""

from fastapi import Security, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import os

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "CHANGE-THIS-IN-PRODUCTION-8f4e9c2b1a7d6e3f")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24 hours

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()


# ============================================================
# PASSWORD UTILITIES
# ============================================================

def hash_password(password: str) -> str:
    """
    Hash yon password
    
    Args:
        password: Password an klè
    
    Returns:
        Password hashed
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifye si password la kòrèk
    
    Args:
        plain_password: Password an klè
        hashed_password: Password hashed
    
    Returns:
        True si password la bon
    """
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================
# JWT TOKEN UTILITIES
# ============================================================

def create_access_token(
    user_id: str,
    email: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Kreye JWT access token
    
    Args:
        user_id: ID itilizatè a
        email: Email itilizatè a
        expires_delta: Tan ekspirasyon (optional)
    
    Returns:
        JWT token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "sub": user_id,
        "email": email,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Dekode JWT token
    
    Args:
        token: JWT token
    
    Returns:
        Token payload
    
    Raises:
        HTTPException si token la invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalid - pa gen user ID"
            )
        
        return payload
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token invalid oswa eksipe: {str(e)}"
        )


# ============================================================
# AUTHENTICATION DEPENDENCIES
# ============================================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """
    Get current authenticated user from JWT token
    
    Usage:
        @app.get("/protected")
        async def protected_route(user: dict = Depends(get_current_user)):
            return {"user_id": user["user_id"]}
    
    Args:
        credentials: HTTP Bearer credentials (auto-extracted)
    
    Returns:
        User information dict
    
    Raises:
        HTTPException si token la invalid
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    return {
        "user_id": payload.get("sub"),
        "email": payload.get("email")
    }


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security, auto_error=False)
) -> Optional[dict]:
    """
    Get current user if authenticated, None otherwise
    Useful pou endpoints ki opsyonèlman mande authentication
    
    Args:
        credentials: HTTP Bearer credentials (optional)
    
    Returns:
        User dict or None
    """
    if credentials is None:
        return None
    
    try:
        return await get_current_user(credentials)
    except:
        return None


# ============================================================
# SIMPLE USER STORE (In-Memory - pou demo)
# ============================================================

# TODO: Replace with real database!
USERS_DB = {
    "demo@kreyolia.ht": {
        "id": "user_001",
        "email": "demo@kreyolia.ht",
        "hashed_password": hash_password("demo123"),  # Demo password
        "full_name": "Demo User",
        "disabled": False,
        "created_at": datetime.now().isoformat()
    }
}


def get_user_by_email(email: str) -> Optional[dict]:
    """
    Get user by email
    
    Args:
        email: User email
    
    Returns:
        User dict or None
    """
    return USERS_DB.get(email)


def create_user(
    email: str,
    password: str,
    full_name: str = None
) -> dict:
    """
    Create a new user
    
    Args:
        email: User email
        password: Plain password
        full_name: Full name (optional)
    
    Returns:
        Created user dict
    
    Raises:
        ValueError if user already exists
    """
    if email in USERS_DB:
        raise ValueError(f"User {email} already exists")
    
    user_id = f"user_{len(USERS_DB) + 1:03d}"
    
    user = {
        "id": user_id,
        "email": email,
        "hashed_password": hash_password(password),
        "full_name": full_name or email.split('@')[0],
        "disabled": False,
        "created_at": datetime.now().isoformat()
    }
    
    USERS_DB[email] = user
    return user


def authenticate_user(email: str, password: str) -> Optional[dict]:
    """
    Authenticate a user with email and password
    
    Args:
        email: User email
        password: Plain password
    
    Returns:
        User dict if authenticated, None otherwise
    """
    user = get_user_by_email(email)
    
    if not user:
        return None
    
    if not verify_password(password, user["hashed_password"]):
        return None
    
    if user.get("disabled"):
        return None
    
    return user


# ============================================================
# DEMO FUNCTION
# ============================================================

def create_demo_users():
    """Create demo users for testing"""
    demo_users = [
        ("demo@kreyolia.ht", "demo123", "Demo User"),
        ("admin@kreyolia.ht", "admin123", "Admin User"),
        ("test@kreyolia.ht", "test123", "Test User"),
    ]
    
    for email, password, full_name in demo_users:
        if email not in USERS_DB:
            try:
                create_user(email, password, full_name)
                print(f"✅ Demo user created: {email}")
            except ValueError:
                pass


if __name__ == "__main__":
    print("🔐 Auth System Test")
    print("=" * 60)
    
    # Create demo users
    create_demo_users()
    
    # Test authentication
    user = authenticate_user("demo@kreyolia.ht", "demo123")
    if user:
        print(f"✅ Authentication successful: {user['email']}")
        
        # Create token
        token = create_access_token(user["id"], user["email"])
        print(f"✅ Token created: {token[:50]}...")
        
        # Decode token
        payload = decode_access_token(token)
        print(f"✅ Token decoded: {payload}")
    else:
        print("❌ Authentication failed")
    
    print("=" * 60)

