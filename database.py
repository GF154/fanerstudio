#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇭🇹 Faner Studio - Database Module
SQLite database for user data, projects, and voice storage
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from pathlib import Path
import os

# ============================================================
# DATABASE SETUP
# ============================================================

# Database file location
DB_DIR = Path("data")
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "fanerstudio.db"

# SQLAlchemy setup
DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ============================================================
# DATABASE MODELS
# ============================================================

class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    custom_voices = relationship("CustomVoice", back_populates="owner", cascade="all, delete-orphan")

class Project(Base):
    """Project model (audiobooks, podcasts, etc.)"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_type = Column(String(50), nullable=False)  # audiobook, podcast, video, etc.
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="pending")  # pending, processing, completed, failed
    progress = Column(Float, default=0.0)  # 0-100
    voice_id = Column(String(100), nullable=True)
    input_file = Column(String(500), nullable=True)
    output_files = Column(Text, nullable=True)  # JSON string
    settings = Column(Text, nullable=True)  # JSON string
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    owner = relationship("User", back_populates="projects")

class CustomVoice(Base):
    """Custom voice model"""
    __tablename__ = "custom_voices"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    voice_id = Column(String(100), unique=True, index=True, nullable=False)
    voice_name = Column(String(200), nullable=False)
    speaker_name = Column(String(200), nullable=True)
    language = Column(String(10), default="ht")
    gender = Column(String(20), default="unknown")
    age_range = Column(String(20), default="adult")
    region = Column(String(100), default="Haiti")
    audio_file = Column(String(500), nullable=False)
    audio_format = Column(String(10), nullable=False)
    duration_seconds = Column(Float, default=0.0)
    file_size_mb = Column(Float, default=0.0)
    text_content = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    times_used = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="custom_voices")

class APIKey(Base):
    """API key model for external service authentication"""
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key_name = Column(String(100), nullable=False)  # huggingface, openai, elevenlabs, etc.
    api_key = Column(String(500), nullable=False)  # Encrypted
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)

class ActivityLog(Base):
    """Activity log for tracking user actions"""
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)  # login, create_project, upload_voice, etc.
    resource_type = Column(String(50), nullable=True)  # project, voice, etc.
    resource_id = Column(Integer, nullable=True)
    details = Column(Text, nullable=True)  # JSON string
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# ============================================================
# DATABASE UTILITIES
# ============================================================

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized: fanerstudio.db")

def get_db():
    """Get database session (dependency injection)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def reset_db():
    """Reset database (drop and recreate all tables)"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Database reset complete")

# ============================================================
# CRUD UTILITIES
# ============================================================

class UserCRUD:
    """User CRUD operations"""
    
    @staticmethod
    def create_user(db, username: str, email: str, hashed_password: str, full_name: str = None):
        """Create new user"""
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user_by_email(db, email: str):
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_username(db, username: str):
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_id(db, user_id: int):
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()

class ProjectCRUD:
    """Project CRUD operations"""
    
    @staticmethod
    def create_project(db, user_id: int, project_type: str, title: str, **kwargs):
        """Create new project"""
        project = Project(
            user_id=user_id,
            project_type=project_type,
            title=title,
            **kwargs
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    
    @staticmethod
    def get_user_projects(db, user_id: int, limit: int = 50):
        """Get user's projects"""
        return db.query(Project).filter(Project.user_id == user_id).order_by(Project.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def update_project_status(db, project_id: int, status: str, progress: float = None):
        """Update project status"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if project:
            project.status = status
            if progress is not None:
                project.progress = progress
            project.updated_at = datetime.utcnow()
            if status == "completed":
                project.completed_at = datetime.utcnow()
            db.commit()
            db.refresh(project)
        return project

class VoiceCRUD:
    """Custom voice CRUD operations"""
    
    @staticmethod
    def create_voice(db, user_id: int, voice_id: str, voice_name: str, **kwargs):
        """Create new custom voice"""
        voice = CustomVoice(
            user_id=user_id,
            voice_id=voice_id,
            voice_name=voice_name,
            **kwargs
        )
        db.add(voice)
        db.commit()
        db.refresh(voice)
        return voice
    
    @staticmethod
    def get_user_voices(db, user_id: int):
        """Get user's custom voices"""
        return db.query(CustomVoice).filter(CustomVoice.user_id == user_id).all()
    
    @staticmethod
    def get_public_voices(db):
        """Get all public voices"""
        return db.query(CustomVoice).filter(CustomVoice.is_public == True).all()
    
    @staticmethod
    def increment_voice_usage(db, voice_id: str):
        """Increment voice usage counter"""
        voice = db.query(CustomVoice).filter(CustomVoice.voice_id == voice_id).first()
        if voice:
            voice.times_used += 1
            db.commit()

# ============================================================
# INITIALIZE ON IMPORT
# ============================================================

if __name__ == "__main__":
    # Initialize database when run directly
    init_db()
    print(f"📁 Database location: {DB_PATH}")
    print("✅ All tables created successfully")
else:
    # Auto-initialize when imported
    if not DB_PATH.exists():
        init_db()

