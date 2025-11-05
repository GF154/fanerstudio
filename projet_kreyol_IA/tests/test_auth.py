#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for authentication module
"""

import pytest
from src.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token,
    create_token_pair,
    generate_api_key,
    hash_api_key,
    verify_api_key
)


def test_password_hashing():
    """Test password hashing and verification"""
    password = "test_password_123"
    
    # Hash password
    hashed = get_password_hash(password)
    
    # Verify correct password
    assert verify_password(password, hashed) is True
    
    # Verify incorrect password
    assert verify_password("wrong_password", hashed) is False


def test_password_hash_uniqueness():
    """Test that same password generates different hashes"""
    password = "test_password"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    
    # Hashes should be different (due to salt)
    assert hash1 != hash2
    
    # But both should verify
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)


def test_create_access_token():
    """Test JWT access token creation"""
    data = {"sub": "testuser", "scopes": ["read"]}
    token = create_access_token(data)
    
    # Token should be a string
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_refresh_token():
    """Test JWT refresh token creation"""
    data = {"sub": "testuser"}
    token = create_refresh_token(data)
    
    assert isinstance(token, str)
    assert len(token) > 0


def test_verify_token_valid():
    """Test token verification with valid token"""
    username = "testuser"
    scopes = ["read", "write"]
    token = create_access_token({"sub": username, "scopes": scopes})
    
    # Verify token
    token_data = verify_token(token)
    
    assert token_data is not None
    assert token_data.username == username
    assert token_data.scopes == scopes


def test_verify_token_invalid():
    """Test token verification with invalid token"""
    invalid_token = "invalid.token.string"
    
    # Should return None for invalid token
    token_data = verify_token(invalid_token)
    assert token_data is None


def test_create_token_pair():
    """Test creating access and refresh token pair"""
    username = "testuser"
    scopes = ["read"]
    
    tokens = create_token_pair(username, scopes)
    
    # Check token pair structure
    assert hasattr(tokens, 'access_token')
    assert hasattr(tokens, 'refresh_token')
    assert hasattr(tokens, 'token_type')
    assert hasattr(tokens, 'expires_in')
    
    assert tokens.token_type == "bearer"
    assert isinstance(tokens.expires_in, int)
    
    # Verify both tokens
    access_data = verify_token(tokens.access_token)
    assert access_data is not None
    assert access_data.username == username


def test_generate_api_key():
    """Test API key generation"""
    key1 = generate_api_key()
    key2 = generate_api_key()
    
    # Keys should be strings
    assert isinstance(key1, str)
    assert isinstance(key2, str)
    
    # Keys should have prefix
    assert key1.startswith("ka_")
    assert key2.startswith("ka_")
    
    # Keys should be unique
    assert key1 != key2
    
    # Keys should be of reasonable length
    assert len(key1) > 40


def test_api_key_hashing():
    """Test API key hashing"""
    api_key = "test_api_key_123"
    
    # Hash the key
    hashed = hash_api_key(api_key)
    
    # Hash should be consistent
    assert hash_api_key(api_key) == hashed
    
    # Different keys should have different hashes
    assert hash_api_key("different_key") != hashed


def test_verify_api_key():
    """Test API key verification"""
    api_key = generate_api_key()
    hashed = hash_api_key(api_key)
    
    # Verify correct key
    assert verify_api_key(api_key, hashed) is True
    
    # Verify incorrect key
    assert verify_api_key("wrong_key", hashed) is False


def test_token_expiration():
    """Test that tokens contain expiration"""
    from datetime import timedelta
    from jose import jwt
    from src.auth import SECRET_KEY, ALGORITHM
    
    # Create token with custom expiration
    token = create_access_token(
        {"sub": "testuser"},
        expires_delta=timedelta(minutes=5)
    )
    
    # Decode without verification to check payload
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    # Should have expiration
    assert "exp" in payload
    assert "iat" in payload
    assert payload["exp"] > payload["iat"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])












