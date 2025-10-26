#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Authentication & Authorization Module
JWT-based authentication for API security
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr, Field

logger = logging.getLogger('KreyolAI.Auth')


# Security configuration
SECRET_KEY = "your-secret-key-change-in-production"  # TODO: Move to env variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==================== MODELS ====================

class UserBase(BaseModel):
    """Base user model"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    disabled: bool = False


class UserInDB(UserBase):
    """User model with hashed password"""
    hashed_password: str
    created_at: str
    last_login: Optional[str] = None
    api_key: Optional[str] = None


class User(UserBase):
    """User model for API responses"""
    created_at: str
    last_login: Optional[str] = None


class UserCreate(BaseModel):
    """User creation model"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """User login model"""
    username: str
    password: str


class Token(BaseModel):
    """Token response model"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token payload data"""
    username: Optional[str] = None
    scopes: list[str] = []


class APIKeyCreate(BaseModel):
    """API key creation model"""
    name: str = Field(..., description="API key name/description")
    expires_in_days: int = Field(30, ge=1, le=365, description="Days until expiration")


class APIKey(BaseModel):
    """API key model"""
    key: str
    name: str
    created_at: str
    expires_at: str
    is_active: bool = True


# ==================== PASSWORD UTILITIES ====================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
    
    Returns:
        True if password matches
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password
    
    Args:
        password: Plain text password
    
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


# ==================== JWT TOKEN UTILITIES ====================

def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token
    
    Args:
        data: Token payload data
        expires_delta: Token expiration time
    
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"Access token created for user: {data.get('sub')}")
    
    return encoded_jwt


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT refresh token
    
    Args:
        data: Token payload data
        expires_delta: Token expiration time
    
    Returns:
        Encoded JWT refresh token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"Refresh token created for user: {data.get('sub')}")
    
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify and decode JWT token
    
    Args:
        token: JWT token string
    
    Returns:
        TokenData if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            logger.warning("Token validation failed: no subject")
            return None
        
        token_scopes = payload.get("scopes", [])
        return TokenData(username=username, scopes=token_scopes)
        
    except JWTError as e:
        logger.warning(f"Token validation failed: {e}")
        return None


def create_token_pair(username: str, scopes: list[str] = None) -> Token:
    """
    Create access and refresh token pair
    
    Args:
        username: Username
        scopes: User permissions/scopes
    
    Returns:
        Token pair
    """
    if scopes is None:
        scopes = []
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(
        data={"sub": username, "scopes": scopes},
        expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(
        data={"sub": username, "scopes": scopes},
        expires_delta=refresh_token_expires
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # in seconds
    )


# ==================== API KEY UTILITIES ====================

import secrets
import hashlib


def generate_api_key() -> str:
    """
    Generate a secure API key
    
    Returns:
        Random API key string
    """
    # Generate 32 bytes random string
    random_bytes = secrets.token_bytes(32)
    
    # Create API key with prefix
    api_key = f"ka_{secrets.token_urlsafe(32)}"
    
    logger.info("New API key generated")
    return api_key


def hash_api_key(api_key: str) -> str:
    """
    Hash an API key for storage
    
    Args:
        api_key: Plain API key
    
    Returns:
        Hashed API key
    """
    return hashlib.sha256(api_key.encode()).hexdigest()


def verify_api_key(plain_key: str, hashed_key: str) -> bool:
    """
    Verify API key against its hash
    
    Args:
        plain_key: Plain API key
        hashed_key: Hashed API key
    
    Returns:
        True if key matches
    """
    return hash_api_key(plain_key) == hashed_key


# ==================== USER MANAGEMENT ====================

class UserManager:
    """
    Manage user authentication and authorization
    """
    
    def __init__(self, db_manager):
        """
        Initialize user manager
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager
        logger.info("User manager initialized")
    
    def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user
        
        Args:
            user_data: User creation data
        
        Returns:
            Created user
        
        Raises:
            ValueError: If user already exists
        """
        # Check if user exists
        if self.get_user(user_data.username):
            raise ValueError(f"User {user_data.username} already exists")
        
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user in database
        user_in_db = UserInDB(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            created_at=datetime.utcnow().isoformat(),
            disabled=False
        )
        
        # Save to database
        self.db.create_user(user_in_db.dict())
        
        logger.info(f"User created: {user_data.username}")
        
        return User(
            username=user_in_db.username,
            email=user_in_db.email,
            full_name=user_in_db.full_name,
            created_at=user_in_db.created_at,
            disabled=user_in_db.disabled
        )
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user
        
        Args:
            username: Username
            password: Plain text password
        
        Returns:
            User if authentication successful, None otherwise
        """
        user_data = self.db.get_user(username)
        
        if not user_data:
            logger.warning(f"Authentication failed: user {username} not found")
            return None
        
        user = UserInDB(**user_data)
        
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Authentication failed: invalid password for {username}")
            return None
        
        if user.disabled:
            logger.warning(f"Authentication failed: user {username} is disabled")
            return None
        
        # Update last login
        self.db.update_user(username, {"last_login": datetime.utcnow().isoformat()})
        
        logger.info(f"User authenticated: {username}")
        
        return User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            created_at=user.created_at,
            last_login=datetime.utcnow().isoformat(),
            disabled=user.disabled
        )
    
    def get_user(self, username: str) -> Optional[User]:
        """
        Get user by username
        
        Args:
            username: Username
        
        Returns:
            User if found, None otherwise
        """
        user_data = self.db.get_user(username)
        
        if not user_data:
            return None
        
        return User(**{k: v for k, v in user_data.items() if k != 'hashed_password'})
    
    def create_api_key(
        self,
        username: str,
        key_data: APIKeyCreate
    ) -> APIKey:
        """
        Create API key for user
        
        Args:
            username: Username
            key_data: API key creation data
        
        Returns:
            Created API key
        
        Raises:
            ValueError: If user not found
        """
        user = self.get_user(username)
        if not user:
            raise ValueError(f"User {username} not found")
        
        # Generate API key
        api_key = generate_api_key()
        hashed_key = hash_api_key(api_key)
        
        # Calculate expiration
        expires_at = datetime.utcnow() + timedelta(days=key_data.expires_in_days)
        
        # Save to database
        key_info = {
            "username": username,
            "name": key_data.name,
            "hashed_key": hashed_key,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": expires_at.isoformat(),
            "is_active": True
        }
        
        self.db.create_api_key(key_info)
        
        logger.info(f"API key created for user {username}: {key_data.name}")
        
        return APIKey(
            key=api_key,  # Return plain key only once
            name=key_data.name,
            created_at=key_info["created_at"],
            expires_at=key_info["expires_at"],
            is_active=True
        )
    
    def verify_api_key(self, api_key: str) -> Optional[str]:
        """
        Verify API key and return username
        
        Args:
            api_key: Plain API key
        
        Returns:
            Username if key is valid, None otherwise
        """
        hashed_key = hash_api_key(api_key)
        key_data = self.db.get_api_key_by_hash(hashed_key)
        
        if not key_data:
            logger.warning("API key verification failed: key not found")
            return None
        
        # Check if key is active
        if not key_data.get("is_active"):
            logger.warning("API key verification failed: key is inactive")
            return None
        
        # Check if key is expired
        expires_at = datetime.fromisoformat(key_data["expires_at"])
        if datetime.utcnow() > expires_at:
            logger.warning("API key verification failed: key is expired")
            return None
        
        logger.info(f"API key verified for user: {key_data['username']}")
        return key_data["username"]






