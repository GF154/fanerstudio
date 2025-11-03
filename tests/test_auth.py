#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Test Authentication Module
Tests for user authentication, registration, login, and JWT tokens
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from main import app
from database import Base, get_db
from auth import hash_password, verify_password, create_access_token, decode_access_token

# ============================================================
# TEST DATABASE SETUP
# ============================================================

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    """Override database dependency for testing"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)

# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture(scope="module")
def setup_database():
    """Setup test database"""
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    yield
    # Drop tables after tests
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def test_user_data():
    """Test user data"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    }

@pytest.fixture
def test_admin_data():
    """Test admin user data"""
    return {
        "username": "admin",
        "email": "admin@example.com",
        "password": "admin123",
        "full_name": "Admin User"
    }

# ============================================================
# PASSWORD HASHING TESTS
# ============================================================

class TestPasswordHashing:
    """Test password hashing and verification"""
    
    def test_hash_password(self):
        """Test password hashing"""
        password = "testpassword123"
        hashed = hash_password(password)
        
        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("$2b$")  # bcrypt format
    
    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "testpassword123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_hash_different_passwords_different_hashes(self):
        """Test that different passwords produce different hashes"""
        password1 = "password1"
        password2 = "password2"
        
        hash1 = hash_password(password1)
        hash2 = hash_password(password2)
        
        assert hash1 != hash2
    
    def test_hash_same_password_different_hashes(self):
        """Test that same password hashed twice produces different hashes (salt)"""
        password = "testpassword123"
        
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Different due to different salts
        assert hash1 != hash2
        # But both should verify correctly
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True

# ============================================================
# JWT TOKEN TESTS
# ============================================================

class TestJWTTokens:
    """Test JWT token creation and validation"""
    
    def test_create_access_token(self):
        """Test JWT token creation"""
        data = {"sub": "testuser", "user_id": 1}
        token = create_access_token(data)
        
        assert token is not None
        assert len(token) > 0
        assert isinstance(token, str)
    
    def test_decode_access_token_valid(self):
        """Test decoding valid JWT token"""
        data = {"sub": "testuser", "user_id": 1}
        token = create_access_token(data)
        
        decoded = decode_access_token(token)
        
        assert decoded is not None
        assert decoded.username == "testuser"
        assert decoded.user_id == 1
    
    def test_decode_access_token_invalid(self):
        """Test decoding invalid JWT token"""
        invalid_token = "invalid.token.here"
        
        decoded = decode_access_token(invalid_token)
        
        assert decoded is None
    
    def test_token_contains_expiration(self):
        """Test that token contains expiration claim"""
        import jwt
        from auth import SECRET_KEY, ALGORITHM
        
        data = {"sub": "testuser", "user_id": 1}
        token = create_access_token(data)
        
        # Decode without verification to check payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        assert "exp" in payload
        assert "sub" in payload

# ============================================================
# USER REGISTRATION TESTS
# ============================================================

class TestUserRegistration:
    """Test user registration endpoint"""
    
    def test_register_new_user(self, setup_database, test_user_data):
        """Test registering a new user"""
        response = client.post("/api/auth/register", json=test_user_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["username"] == test_user_data["username"]
        assert data["email"] == test_user_data["email"]
        assert data["full_name"] == test_user_data["full_name"]
        assert data["is_active"] is True
        assert "id" in data
        assert "hashed_password" not in data  # Should not expose password
    
    def test_register_duplicate_username(self, setup_database, test_user_data):
        """Test registering user with duplicate username"""
        # Register first user
        client.post("/api/auth/register", json=test_user_data)
        
        # Try to register again with same username
        response = client.post("/api/auth/register", json=test_user_data)
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()
    
    def test_register_duplicate_email(self, setup_database, test_user_data):
        """Test registering user with duplicate email"""
        # Register first user
        client.post("/api/auth/register", json=test_user_data)
        
        # Try to register with different username but same email
        duplicate_email_user = test_user_data.copy()
        duplicate_email_user["username"] = "differentuser"
        
        response = client.post("/api/auth/register", json=duplicate_email_user)
        
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()
    
    def test_register_missing_fields(self, setup_database):
        """Test registering user with missing fields"""
        incomplete_data = {"username": "testuser"}
        
        response = client.post("/api/auth/register", json=incomplete_data)
        
        assert response.status_code == 422  # Validation error

# ============================================================
# USER LOGIN TESTS
# ============================================================

class TestUserLogin:
    """Test user login endpoint"""
    
    def test_login_success(self, setup_database, test_user_data):
        """Test successful login"""
        # Register user first
        client.post("/api/auth/register", json=test_user_data)
        
        # Login
        login_data = {
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
        
        response = client.post(
            "/api/auth/login",
            data=login_data
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0
    
    def test_login_wrong_password(self, setup_database, test_user_data):
        """Test login with wrong password"""
        # Register user first
        client.post("/api/auth/register", json=test_user_data)
        
        # Try to login with wrong password
        login_data = {
            "username": test_user_data["username"],
            "password": "wrongpassword"
        }
        
        response = client.post(
            "/api/auth/login",
            data=login_data
        )
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_login_nonexistent_user(self, setup_database):
        """Test login with non-existent user"""
        login_data = {
            "username": "nonexistent",
            "password": "password123"
        }
        
        response = client.post(
            "/api/auth/login",
            data=login_data
        )
        
        assert response.status_code == 401
    
    def test_login_missing_credentials(self, setup_database):
        """Test login with missing credentials"""
        response = client.post("/api/auth/login", data={})
        
        assert response.status_code == 422  # Validation error

# ============================================================
# AUTHENTICATED ENDPOINTS TESTS
# ============================================================

class TestAuthenticatedEndpoints:
    """Test endpoints that require authentication"""
    
    def test_get_current_user_authenticated(self, setup_database, test_user_data):
        """Test getting current user info when authenticated"""
        # Register and login
        client.post("/api/auth/register", json=test_user_data)
        
        login_response = client.post(
            "/api/auth/login",
            data={
                "username": test_user_data["username"],
                "password": test_user_data["password"]
            }
        )
        token = login_response.json()["access_token"]
        
        # Get current user
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["username"] == test_user_data["username"]
        assert data["email"] == test_user_data["email"]
    
    def test_get_current_user_unauthenticated(self, setup_database):
        """Test getting current user info without authentication"""
        response = client.get("/api/auth/me")
        
        assert response.status_code == 401
    
    def test_get_current_user_invalid_token(self, setup_database):
        """Test getting current user info with invalid token"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        
        assert response.status_code == 401

# ============================================================
# ADMIN ROLE TESTS
# ============================================================

class TestAdminRole:
    """Test admin role functionality"""
    
    def test_admin_endpoints_require_admin_role(self, setup_database, test_user_data):
        """Test that admin endpoints require admin role"""
        # Register regular user
        client.post("/api/auth/register", json=test_user_data)
        
        # Login
        login_response = client.post(
            "/api/auth/login",
            data={
                "username": test_user_data["username"],
                "password": test_user_data["password"]
            }
        )
        token = login_response.json()["access_token"]
        
        # Try to access admin endpoint
        response = client.get(
            "/api/admin/stats",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 403  # Forbidden
        assert "admin" in response.json()["detail"].lower()

# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

