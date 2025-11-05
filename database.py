#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗄️ Faner Studio - Supabase Database
Database connection and operations using Supabase
"""

import os
from supabase import create_client, Client
from datetime import datetime
from typing import Optional, List, Dict, Any

# ============================================================
# SUPABASE CONNECTION (LAZY INITIALIZATION)
# ============================================================

# Get Supabase credentials from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Global client (will be initialized on first use)
_supabase_client: Optional[Client] = None
_connection_attempted = False

def get_supabase_client() -> Optional[Client]:
    """
    Get Supabase client with lazy initialization.
    Only connects when first called, not on module import.
    This is important for Vercel serverless functions.
    """
    global _supabase_client, _connection_attempted
    
    if _supabase_client is not None:
        return _supabase_client
    
    if _connection_attempted:
        return None
    
    _connection_attempted = True
    
    # Check credentials
    if not SUPABASE_URL or not SUPABASE_KEY:
        error_msg = f"⚠️ Supabase credentials not set. URL: {bool(SUPABASE_URL)}, KEY: {bool(SUPABASE_KEY)}"
        print(error_msg)
        return None
    
    print(f"🔄 Attempting Supabase connection to: {SUPABASE_URL[:30]}...")
    
    try:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print(f"✅ Supabase connected! URL: {SUPABASE_URL[:30]}...")
        
        # Test connection by making a simple query
        try:
            _supabase_client.table("users").select("id", count="exact").limit(0).execute()
            print("✅ Supabase connection test passed!")
        except Exception as test_error:
            print(f"⚠️ Supabase connection test failed: {test_error}")
            # Keep client anyway, table might not exist yet
        
        return _supabase_client
    except Exception as e:
        error_msg = f"❌ Supabase connection failed: {type(e).__name__}: {str(e)}"
        print(error_msg)
        return None


# ============================================================
# USER OPERATIONS
# ============================================================

class UserDB:
    """User database operations"""
    
    @staticmethod
    def create_user(username: str, email: str, password_hash: str, full_name: Optional[str] = None) -> Dict[str, Any]:
        """Create new user"""
        supabase = get_supabase_client()
        if not supabase:
            return {"error": "Database not available"}
        
        try:
            data = {
                "username": username,
                "email": email,
                "password_hash": password_hash,
                "full_name": full_name,
                "is_active": True,
                "created_at": datetime.now().isoformat()
            }
            
            result = supabase.table("users").insert(data).execute()
            return result.data[0] if result.data else {"error": "Failed to create user"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        supabase = get_supabase_client()
        if not supabase:
            return None
        
        try:
            result = supabase.table("users").select("*").eq("email", email).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    @staticmethod
    def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        supabase = get_supabase_client()
        if not supabase:
            return None
        
        try:
            result = supabase.table("users").select("*").eq("username", username).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        supabase = get_supabase_client()
        if not supabase:
            return None
        
        try:
            result = supabase.table("users").select("*").eq("id", user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None


# ============================================================
# PROJECT OPERATIONS
# ============================================================

class ProjectDB:
    """Project database operations"""
    
    @staticmethod
    def create_project(
        user_id: int,
        project_type: str,
        title: str,
        data: Dict[str, Any],
        status: str = "processing"
    ) -> Dict[str, Any]:
        """Create new project"""
        supabase = get_supabase_client()
        if not supabase:
            return {"error": "Database not available"}
        
        try:
            project_data = {
                "user_id": user_id,
                "project_type": project_type,
                "title": title,
                "data": data,
                "status": status,
                "created_at": datetime.now().isoformat()
            }
            
            result = supabase.table("projects").insert(project_data).execute()
            return result.data[0] if result.data else {"error": "Failed to create project"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_user_projects(user_id: int, project_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all projects for a user"""
        supabase = get_supabase_client()
        if not supabase:
            return []
        
        try:
            query = supabase.table("projects").select("*").eq("user_id", user_id)
            
            if project_type:
                query = query.eq("project_type", project_type)
            
            result = query.order("created_at", desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error getting projects: {e}")
            return []
    
    @staticmethod
    def get_project(project_id: int) -> Optional[Dict[str, Any]]:
        """Get project by ID"""
        supabase = get_supabase_client()
        if not supabase:
            return None
        
        try:
            result = supabase.table("projects").select("*").eq("id", project_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting project: {e}")
            return None
    
    @staticmethod
    def update_project_status(project_id: int, status: str, output_url: Optional[str] = None) -> bool:
        """Update project status"""
        supabase = get_supabase_client()
        if not supabase:
            return False
        
        try:
            data = {"status": status}
            if output_url:
                data["output_url"] = output_url
            
            supabase.table("projects").update(data).eq("id", project_id).execute()
            return True
        except Exception as e:
            print(f"Error updating project: {e}")
            return False
    
    @staticmethod
    def delete_project(project_id: int) -> bool:
        """Delete project"""
        supabase = get_supabase_client()
        if not supabase:
            return False
        
        try:
            supabase.table("projects").delete().eq("id", project_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting project: {e}")
            return False


# ============================================================
# CUSTOM VOICE OPERATIONS
# ============================================================

class VoiceDB:
    """Custom voice database operations"""
    
    @staticmethod
    def create_voice(
        user_id: int,
        voice_name: str,
        quality: str,
        samples_count: int,
        voice_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create custom voice"""
        supabase = get_supabase_client()
        if not supabase:
            return {"error": "Database not available"}
        
        try:
            data = {
                "user_id": user_id,
                "voice_name": voice_name,
                "quality": quality,
                "samples_count": samples_count,
                "voice_data": voice_data,
                "is_active": True,
                "created_at": datetime.now().isoformat()
            }
            
            result = supabase.table("voices").insert(data).execute()
            return result.data[0] if result.data else {"error": "Failed to create voice"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_user_voices(user_id: int) -> List[Dict[str, Any]]:
        """Get all voices for a user"""
        supabase = get_supabase_client()
        if not supabase:
            return []
        
        try:
            result = supabase.table("voices").select("*").eq("user_id", user_id).eq("is_active", True).order("created_at", desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error getting voices: {e}")
            return []
    
    @staticmethod
    def get_voice(voice_id: int) -> Optional[Dict[str, Any]]:
        """Get voice by ID"""
        supabase = get_supabase_client()
        if not supabase:
            return None
        
        try:
            result = supabase.table("voices").select("*").eq("id", voice_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting voice: {e}")
            return None
    
    @staticmethod
    def delete_voice(voice_id: int) -> bool:
        """Delete voice (soft delete)"""
        supabase = get_supabase_client()
        if not supabase:
            return False
        
        try:
            supabase.table("voices").update({"is_active": False}).eq("id", voice_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting voice: {e}")
            return False


# ============================================================
# AUDIO FILE OPERATIONS
# ============================================================

class AudioDB:
    """Audio file database operations"""
    
    @staticmethod
    def save_audio(
        user_id: int,
        project_id: Optional[int],
        filename: str,
        file_url: str,
        file_type: str,
        duration: Optional[str] = None,
        size_mb: Optional[float] = None
    ) -> Dict[str, Any]:
        """Save audio file metadata"""
        supabase = get_supabase_client()
        if not supabase:
            return {"error": "Database not available"}
        
        try:
            data = {
                "user_id": user_id,
                "project_id": project_id,
                "filename": filename,
                "file_url": file_url,
                "file_type": file_type,
                "duration": duration,
                "size_mb": size_mb,
                "created_at": datetime.now().isoformat()
            }
            
            result = supabase.table("audios").insert(data).execute()
            return result.data[0] if result.data else {"error": "Failed to save audio"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_user_audios(user_id: int) -> List[Dict[str, Any]]:
        """Get all audios for a user"""
        supabase = get_supabase_client()
        if not supabase:
            return []
        
        try:
            result = supabase.table("audios").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error getting audios: {e}")
            return []


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def init_database():
    """Initialize database tables"""
    supabase = get_supabase_client()
    if not supabase:
        print("⚠️  Database not enabled, skipping initialization")
        return False
    
    print("✅ Supabase database ready!")
    print("""
    📋 Required tables in Supabase:
    
    1. users (id, username, email, password_hash, full_name, is_active, created_at)
    2. projects (id, user_id, project_type, title, data, status, output_url, created_at)
    3. voices (id, user_id, voice_name, quality, samples_count, voice_data, is_active, created_at)
    4. audios (id, user_id, project_id, filename, file_url, file_type, duration, size_mb, created_at)
    
    Create these tables in your Supabase dashboard!
    """)
    return True


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def check_database_connection() -> bool:
    """Check if database is connected"""
    return get_supabase_client() is not None
