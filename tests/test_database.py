#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Test Database CRUD Operations
Tests for database models and CRUD operations
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from database import Base, User, Project, CustomVoice, APIKey, ActivityLog
from database import UserCRUD, ProjectCRUD, VoiceCRUD
from auth import hash_password

# ============================================================
# TEST DATABASE SETUP
# ============================================================

TEST_DATABASE_URL = "sqlite:///./test_database.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

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
def db_session(setup_database):
    """Create database session for tests"""
    session = TestingSessionLocal()
    yield session
    session.rollback()
    session.close()

# ============================================================
# USER MODEL TESTS
# ============================================================

class TestUserModel:
    """Test User model"""
    
    def test_create_user(self, db_session):
        """Test creating a user"""
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=hash_password("password123"),
            full_name="Test User"
        )
        
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.is_active is True
        assert user.is_admin is False
        assert user.created_at is not None
    
    def test_user_relationships(self, db_session):
        """Test user relationships (projects, voices)"""
        user = User(
            username="reluser",
            email="rel@example.com",
            hashed_password=hash_password("password123")
        )
        db_session.add(user)
        db_session.commit()
        
        # Add project
        project = Project(
            user_id=user.id,
            project_type="audiobook",
            title="Test Audiobook"
        )
        db_session.add(project)
        
        # Add voice
        voice = CustomVoice(
            user_id=user.id,
            voice_id="voice_123",
            voice_name="Test Voice",
            language="ht",
            audio_file="/path/to/audio.mp3",
            audio_format="mp3"
        )
        db_session.add(voice)
        db_session.commit()
        
        # Test relationships
        assert len(user.projects) == 1
        assert len(user.custom_voices) == 1
        assert user.projects[0].title == "Test Audiobook"
        assert user.custom_voices[0].voice_name == "Test Voice"

# ============================================================
# USER CRUD TESTS
# ============================================================

class TestUserCRUD:
    """Test User CRUD operations"""
    
    def test_create_user(self, db_session):
        """Test creating user with CRUD"""
        user = UserCRUD.create_user(
            db=db_session,
            username="cruduser",
            email="crud@example.com",
            hashed_password=hash_password("password123"),
            full_name="CRUD User"
        )
        
        assert user.id is not None
        assert user.username == "cruduser"
    
    def test_get_user_by_username(self, db_session):
        """Test getting user by username"""
        # Create user
        UserCRUD.create_user(
            db=db_session,
            username="finduser",
            email="find@example.com",
            hashed_password=hash_password("password123")
        )
        
        # Find user
        user = UserCRUD.get_user_by_username(db_session, "finduser")
        
        assert user is not None
        assert user.username == "finduser"
    
    def test_get_user_by_email(self, db_session):
        """Test getting user by email"""
        # Create user
        UserCRUD.create_user(
            db=db_session,
            username="emailuser",
            email="email@example.com",
            hashed_password=hash_password("password123")
        )
        
        # Find user
        user = UserCRUD.get_user_by_email(db_session, "email@example.com")
        
        assert user is not None
        assert user.email == "email@example.com"
    
    def test_get_user_by_id(self, db_session):
        """Test getting user by ID"""
        # Create user
        user = UserCRUD.create_user(
            db=db_session,
            username="iduser",
            email="id@example.com",
            hashed_password=hash_password("password123")
        )
        
        # Find user
        found_user = UserCRUD.get_user_by_id(db_session, user.id)
        
        assert found_user is not None
        assert found_user.id == user.id

# ============================================================
# PROJECT MODEL TESTS
# ============================================================

class TestProjectModel:
    """Test Project model"""
    
    def test_create_project(self, db_session):
        """Test creating a project"""
        # Create user first
        user = User(
            username="projuser",
            email="proj@example.com",
            hashed_password=hash_password("password123")
        )
        db_session.add(user)
        db_session.commit()
        
        # Create project
        project = Project(
            user_id=user.id,
            project_type="audiobook",
            title="Test Audiobook",
            description="Test description",
            status="pending",
            progress=0.0
        )
        
        db_session.add(project)
        db_session.commit()
        
        assert project.id is not None
        assert project.user_id == user.id
        assert project.title == "Test Audiobook"
        assert project.status == "pending"
        assert project.progress == 0.0

# ============================================================
# PROJECT CRUD TESTS
# ============================================================

class TestProjectCRUD:
    """Test Project CRUD operations"""
    
    def test_create_project(self, db_session):
        """Test creating project with CRUD"""
        # Create user
        user = UserCRUD.create_user(
            db=db_session,
            username="projectowner",
            email="owner@example.com",
            hashed_password=hash_password("password123")
        )
        
        # Create project
        project = ProjectCRUD.create_project(
            db=db_session,
            user_id=user.id,
            project_type="podcast",
            title="Test Podcast",
            description="A test podcast"
        )
        
        assert project.id is not None
        assert project.title == "Test Podcast"
    
    def test_get_user_projects(self, db_session):
        """Test getting user's projects"""
        # Create user
        user = UserCRUD.create_user(
            db=db_session,
            username="multiproj",
            email="multi@example.com",
            hashed_password=hash_password("password123")
        )
        
        # Create multiple projects
        for i in range(3):
            ProjectCRUD.create_project(
                db=db_session,
                user_id=user.id,
                project_type="audiobook",
                title=f"Audiobook {i}"
            )
        
        # Get projects
        projects = ProjectCRUD.get_user_projects(db_session, user.id)
        
        assert len(projects) == 3
    
    def test_update_project_status(self, db_session):
        """Test updating project status"""
        # Create user and project
        user = UserCRUD.create_user(
            db=db_session,
            username="statususer",
            email="status@example.com",
            hashed_password=hash_password("password123")
        )
        
        project = ProjectCRUD.create_project(
            db=db_session,
            user_id=user.id,
            project_type="audiobook",
            title="Status Test"
        )
        
        # Update status
        updated_project = ProjectCRUD.update_project_status(
            db=db_session,
            project_id=project.id,
            status="completed",
            progress=100.0
        )
        
        assert updated_project.status == "completed"
        assert updated_project.progress == 100.0
        assert updated_project.completed_at is not None

# ============================================================
# CUSTOM VOICE MODEL TESTS
# ============================================================

class TestCustomVoiceModel:
    """Test CustomVoice model"""
    
    def test_create_voice(self, db_session):
        """Test creating a custom voice"""
        # Create user
        user = User(
            username="voiceuser",
            email="voice@example.com",
            hashed_password=hash_password("password123")
        )
        db_session.add(user)
        db_session.commit()
        
        # Create voice
        voice = CustomVoice(
            user_id=user.id,
            voice_id="voice_unique_123",
            voice_name="My Voice",
            speaker_name="Speaker Name",
            language="ht",
            gender="female",
            audio_file="/path/to/voice.mp3",
            audio_format="mp3",
            duration_seconds=120.5,
            file_size_mb=5.2
        )
        
        db_session.add(voice)
        db_session.commit()
        
        assert voice.id is not None
        assert voice.voice_id == "voice_unique_123"
        assert voice.times_used == 0
        assert voice.rating == 0.0

# ============================================================
# VOICE CRUD TESTS
# ============================================================

class TestVoiceCRUD:
    """Test Voice CRUD operations"""
    
    def test_create_voice(self, db_session):
        """Test creating voice with CRUD"""
        # Create user
        user = UserCRUD.create_user(
            db=db_session,
            username="voiceowner",
            email="voiceowner@example.com",
            hashed_password=hash_password("password123")
        )
        
        # Create voice
        voice = VoiceCRUD.create_voice(
            db=db_session,
            user_id=user.id,
            voice_id="crud_voice_123",
            voice_name="CRUD Voice",
            language="ht",
            audio_file="/path/to/audio.mp3",
            audio_format="mp3"
        )
        
        assert voice.id is not None
        assert voice.voice_name == "CRUD Voice"
    
    def test_get_user_voices(self, db_session):
        """Test getting user's voices"""
        # Create user
        user = UserCRUD.create_user(
            db=db_session,
            username="multivoice",
            email="multivoice@example.com",
            hashed_password=hash_password("password123")
        )
        
        # Create multiple voices
        for i in range(3):
            VoiceCRUD.create_voice(
                db=db_session,
                user_id=user.id,
                voice_id=f"voice_{i}",
                voice_name=f"Voice {i}",
                language="ht",
                audio_file=f"/path/voice{i}.mp3",
                audio_format="mp3"
            )
        
        # Get voices
        voices = VoiceCRUD.get_user_voices(db_session, user.id)
        
        assert len(voices) == 3
    
    def test_increment_voice_usage(self, db_session):
        """Test incrementing voice usage counter"""
        # Create user and voice
        user = UserCRUD.create_user(
            db=db_session,
            username="usageuser",
            email="usage@example.com",
            hashed_password=hash_password("password123")
        )
        
        voice = VoiceCRUD.create_voice(
            db=db_session,
            user_id=user.id,
            voice_id="usage_voice",
            voice_name="Usage Voice",
            language="ht",
            audio_file="/path/voice.mp3",
            audio_format="mp3"
        )
        
        # Increment usage
        VoiceCRUD.increment_voice_usage(db_session, voice.voice_id)
        
        # Verify
        db_session.refresh(voice)
        assert voice.times_used == 1
        
        # Increment again
        VoiceCRUD.increment_voice_usage(db_session, voice.voice_id)
        db_session.refresh(voice)
        assert voice.times_used == 2

# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

