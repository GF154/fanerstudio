#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Test Admin Endpoints
Tests for admin dashboard endpoints (stats, user management, projects)
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app
from database import Base, get_db, User, Project, CustomVoice
from auth import hash_password

# ============================================================
# TEST DATABASE SETUP
# ============================================================

TEST_DATABASE_URL = "sqlite:///./test_admin.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture(scope="module")
def setup_database():
    """Setup test database"""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def admin_token(setup_database):
    """Create admin user and return auth token"""
    # Create admin user
    db = TestingSessionLocal()
    
    admin = User(
        username="admin",
        email="admin@test.com",
        hashed_password=hash_password("admin123"),
        full_name="Admin User",
        is_active=True,
        is_admin=True
    )
    db.add(admin)
    db.commit()
    db.close()
    
    # Login
    response = client.post(
        "/api/auth/login",
        data={"username": "admin", "password": "admin123"}
    )
    
    return response.json()["access_token"]

@pytest.fixture
def regular_user_token(setup_database):
    """Create regular user and return auth token"""
    # Create regular user
    db = TestingSessionLocal()
    
    user = User(
        username="user",
        email="user@test.com",
        hashed_password=hash_password("user123"),
        full_name="Regular User",
        is_active=True,
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.close()
    
    # Login
    response = client.post(
        "/api/auth/login",
        data={"username": "user", "password": "user123"}
    )
    
    return response.json()["access_token"]

@pytest.fixture
def sample_users(setup_database):
    """Create sample users for testing"""
    db = TestingSessionLocal()
    
    users = []
    for i in range(5):
        user = User(
            username=f"user{i}",
            email=f"user{i}@test.com",
            hashed_password=hash_password(f"pass{i}"),
            full_name=f"User {i}",
            is_active=True,
            is_admin=False
        )
        db.add(user)
        users.append(user)
    
    db.commit()
    db.close()
    
    return users

# ============================================================
# ADMIN STATS TESTS
# ============================================================

class TestAdminStats:
    """Test admin statistics endpoint"""
    
    def test_get_stats_as_admin(self, admin_token, sample_users):
        """Test getting stats as admin"""
        response = client.get(
            "/api/admin/stats",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "total_users" in data
        assert "total_projects" in data
        assert "total_voices" in data
        assert "users_this_week" in data
        assert data["status"] == "success"
        assert data["total_users"] >= 5  # At least 5 sample users
    
    def test_get_stats_as_regular_user(self, regular_user_token):
        """Test getting stats as regular user (should fail)"""
        response = client.get(
            "/api/admin/stats",
            headers={"Authorization": f"Bearer {regular_user_token}"}
        )
        
        assert response.status_code == 403
        assert "admin" in response.json()["detail"].lower()
    
    def test_get_stats_unauthenticated(self):
        """Test getting stats without authentication"""
        response = client.get("/api/admin/stats")
        
        assert response.status_code == 401

# ============================================================
# ADMIN USER MANAGEMENT TESTS
# ============================================================

class TestAdminUserManagement:
    """Test admin user management endpoints"""
    
    def test_get_all_users_as_admin(self, admin_token, sample_users):
        """Test getting all users as admin"""
        response = client.get(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "users" in data
        assert "total" in data
        assert len(data["users"]) >= 5
        assert data["status"] == "success"
        
        # Check user data structure
        user = data["users"][0]
        assert "id" in user
        assert "username" in user
        assert "email" in user
        assert "is_active" in user
        assert "is_admin" in user
    
    def test_get_all_users_with_pagination(self, admin_token, sample_users):
        """Test getting users with pagination"""
        response = client.get(
            "/api/admin/users?limit=2&offset=0",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["users"]) <= 2
    
    def test_get_all_users_as_regular_user(self, regular_user_token):
        """Test getting all users as regular user (should fail)"""
        response = client.get(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {regular_user_token}"}
        )
        
        assert response.status_code == 403
    
    def test_update_user_as_admin(self, admin_token, sample_users):
        """Test updating user as admin"""
        # Get first user ID
        db = TestingSessionLocal()
        user = db.query(User).filter(User.username == "user0").first()
        user_id = user.id
        db.close()
        
        # Update user
        response = client.put(
            f"/api/admin/user/{user_id}?is_active=false",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        assert data["user"]["is_active"] is False
    
    def test_delete_user_as_admin(self, admin_token, sample_users):
        """Test deleting user as admin"""
        # Get user ID
        db = TestingSessionLocal()
        user = db.query(User).filter(User.username == "user1").first()
        user_id = user.id
        db.close()
        
        # Delete user
        response = client.delete(
            f"/api/admin/user/{user_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        
        # Verify user is deleted
        db = TestingSessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        assert user is None
        db.close()
    
    def test_delete_self_as_admin(self, admin_token):
        """Test that admin cannot delete their own account"""
        # Get admin user ID
        db = TestingSessionLocal()
        admin = db.query(User).filter(User.username == "admin").first()
        admin_id = admin.id
        db.close()
        
        # Try to delete self
        response = client.delete(
            f"/api/admin/user/{admin_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 400
        assert "cannot delete your own account" in response.json()["detail"].lower()

# ============================================================
# ADMIN PROJECT MANAGEMENT TESTS
# ============================================================

class TestAdminProjectManagement:
    """Test admin project management endpoints"""
    
    def test_get_all_projects_as_admin(self, admin_token):
        """Test getting all projects as admin"""
        # Create sample projects
        db = TestingSessionLocal()
        user = db.query(User).first()
        
        for i in range(3):
            project = Project(
                user_id=user.id,
                project_type="audiobook",
                title=f"Test Project {i}",
                status="completed",
                progress=100.0
            )
            db.add(project)
        
        db.commit()
        db.close()
        
        # Get projects
        response = client.get(
            "/api/admin/projects",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "projects" in data
        assert "total" in data
        assert len(data["projects"]) >= 3
        
        # Check project data structure
        project = data["projects"][0]
        assert "id" in project
        assert "user_id" in project
        assert "project_type" in project
        assert "title" in project
        assert "status" in project
    
    def test_delete_project_as_admin(self, admin_token):
        """Test deleting project as admin"""
        # Create project
        db = TestingSessionLocal()
        user = db.query(User).first()
        
        project = Project(
            user_id=user.id,
            project_type="podcast",
            title="Test Delete Project",
            status="pending",
            progress=0.0
        )
        db.add(project)
        db.commit()
        project_id = project.id
        db.close()
        
        # Delete project
        response = client.delete(
            f"/api/admin/project/{project_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "success"
        
        # Verify project is deleted
        db = TestingSessionLocal()
        project = db.query(Project).filter(Project.id == project_id).first()
        assert project is None
        db.close()

# ============================================================
# ADMIN VOICE MANAGEMENT TESTS
# ============================================================

class TestAdminVoiceManagement:
    """Test admin voice management endpoints"""
    
    def test_get_all_voices_as_admin(self, admin_token):
        """Test getting all voices as admin"""
        # Create sample voices
        db = TestingSessionLocal()
        user = db.query(User).first()
        
        for i in range(3):
            voice = CustomVoice(
                user_id=user.id,
                voice_id=f"voice_{i}",
                voice_name=f"Test Voice {i}",
                language="ht",
                audio_file=f"/path/to/voice{i}.mp3",
                audio_format="mp3",
                times_used=i * 10
            )
            db.add(voice)
        
        db.commit()
        db.close()
        
        # Get voices
        response = client.get(
            "/api/admin/voices",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "voices" in data
        assert "total" in data
        assert len(data["voices"]) >= 3
        
        # Check voice data structure
        voice = data["voices"][0]
        assert "id" in voice
        assert "voice_id" in voice
        assert "voice_name" in voice
        assert "times_used" in voice

# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

