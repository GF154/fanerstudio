#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇭🇹 Faner Studio - Authentication Module
JWT-based authentication with bcrypt password hashing
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import os

# ============================================================
# CONFIGURATION
# ============================================================

# Secret key for JWT (should be in environment variables)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# ============================================================
# PYDANTIC MODELS
# ============================================================

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================
# PASSWORD UTILITIES
# ============================================================

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

# Alias for compatibility
get_password_hash = hash_password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# ============================================================
# JWT UTILITIES
# ============================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> TokenData:
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
        if username is None:
            return None
        
        token_data = TokenData(username=username, user_id=user_id)
        return token_data
    except JWTError:
        return None

# ============================================================
# AUTHENTICATION DEPENDENCIES
# ============================================================

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current authenticated user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = decode_access_token(token)
    if token_data is None:
        raise credentials_exception
    
    # Import here to avoid circular imports
    from database import SessionLocal, UserCRUD
    
    db = SessionLocal()
    try:
        user = UserCRUD.get_user_by_username(db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
    finally:
        db.close()

async def get_current_active_user(current_user = Depends(get_current_user)):
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_admin_user(current_user = Depends(get_current_user)):
    """Get current admin user"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )
    return current_user

# ============================================================
# OPTIONAL: SIMPLE AUTH (No JWT)
# ============================================================

class OptionalAuth:
    """Optional authentication - returns user if authenticated, None otherwise"""
    
    async def __call__(self, token: Optional[str] = Depends(oauth2_scheme)):
        if token is None:
            return None
        
        try:
            token_data = decode_access_token(token)
            if token_data is None:
                return None
            
            from database import SessionLocal, UserCRUD
            db = SessionLocal()
            try:
                user = UserCRUD.get_user_by_username(db, username=token_data.username)
                return user
            finally:
                db.close()
        except:
            return None

optional_auth = OptionalAuth()

# ============================================================
# UTILITIES
# ============================================================

def authenticate_user(username: str, password: str):
    """Authenticate user by username and password"""
    from database import SessionLocal, UserCRUD
    
    db = SessionLocal()
    try:
        user = UserCRUD.get_user_by_username(db, username=username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user
    finally:
        db.close()

def create_user_account(username: str, email: str, password: str, full_name: str = None):
    """Create new user account"""
    from database import SessionLocal, UserCRUD
    
    db = SessionLocal()
    try:
        # Check if user already exists
        if UserCRUD.get_user_by_username(db, username=username):
            raise ValueError("Username already exists")
        if UserCRUD.get_user_by_email(db, email=email):
            raise ValueError("Email already exists")
        
        # Create user
        hashed_password = hash_password(password)
        user = UserCRUD.create_user(
            db=db,
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name
        )
        return user
    finally:
        db.close()

