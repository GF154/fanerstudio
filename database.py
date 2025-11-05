#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗄️ Faner Studio - Supabase Database via REST API
Database operations using Supabase REST API (Vercel compatible)
"""

import os
import httpx
from datetime import datetime
from typing import Optional, List, Dict, Any

# ============================================================
# SUPABASE REST API CONNECTION
# ============================================================

# Get Supabase credentials from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_headers() -> Dict[str, str]:
    """Get headers for Supabase REST API requests"""
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def check_credentials() -> bool:
    """Check if Supabase credentials are available"""
    return bool(SUPABASE_URL and SUPABASE_KEY)


# ============================================================
# USER OPERATIONS
# ============================================================

class UserDB:
    """User database operations via REST API"""
    
    @staticmethod
    async def create_user(username: str, email: str, password_hash: str, full_name: Optional[str] = None) -> Dict[str, Any]:
        """Create new user"""
        if not check_credentials():
            return {"error": "Database credentials not available"}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{SUPABASE_URL}/rest/v1/users",
                    headers=get_headers(),
                    json={
                        "username": username,
                        "email": email,
                        "password_hash": password_hash,
                        "full_name": full_name,
                        "is_active": True,
                        "created_at": datetime.now().isoformat()
                    }
                )
                
                if response.status_code in [200, 201]:
                    data = response.json()
                    return data[0] if isinstance(data, list) else data
                else:
                    return {"error": f"Failed to create user: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        if not check_credentials():
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{SUPABASE_URL}/rest/v1/users",
                    headers=get_headers(),
                    params={"email": f"eq.{email}", "select": "*"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data[0] if data else None
                return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    @staticmethod
    async def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        if not check_credentials():
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{SUPABASE_URL}/rest/v1/users",
                    headers=get_headers(),
                    params={"username": f"eq.{username}", "select": "*"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data[0] if data else None
                return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        if not check_credentials():
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{SUPABASE_URL}/rest/v1/users",
                    headers=get_headers(),
                    params={"id": f"eq.{user_id}", "select": "*"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data[0] if data else None
                return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None


# ============================================================
# PROJECT OPERATIONS
# ============================================================

class ProjectDB:
    """Project database operations via REST API"""
    
    @staticmethod
    async def create_project(
        user_id: int,
        project_type: str,
        title: str,
        data: Dict[str, Any],
        status: str = "processing"
    ) -> Dict[str, Any]:
        """Create new project"""
        if not check_credentials():
            return {"error": "Database credentials not available"}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{SUPABASE_URL}/rest/v1/projects",
                    headers=get_headers(),
                    json={
                        "user_id": user_id,
                        "project_type": project_type,
                        "title": title,
                        "data": data,
                        "status": status,
                        "created_at": datetime.now().isoformat()
                    }
                )
                
                if response.status_code in [200, 201]:
                    data = response.json()
                    return data[0] if isinstance(data, list) else data
                else:
                    return {"error": f"Failed to create project: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    async def get_user_projects(user_id: int, project_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all projects for a user"""
        if not check_credentials():
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "user_id": f"eq.{user_id}",
                    "select": "*",
                    "order": "created_at.desc"
                }
                
                if project_type:
                    params["project_type"] = f"eq.{project_type}"
                
                response = await client.get(
                    f"{SUPABASE_URL}/rest/v1/projects",
                    headers=get_headers(),
                    params=params
                )
                
                if response.status_code == 200:
                    return response.json()
                return []
        except Exception as e:
            print(f"Error getting projects: {e}")
            return []
    
    @staticmethod
    async def get_project(project_id: int) -> Optional[Dict[str, Any]]:
        """Get project by ID"""
        if not check_credentials():
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{SUPABASE_URL}/rest/v1/projects",
                    headers=get_headers(),
                    params={"id": f"eq.{project_id}", "select": "*"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data[0] if data else None
                return None
        except Exception as e:
            print(f"Error getting project: {e}")
            return None
    
    @staticmethod
    async def update_project_status(project_id: int, status: str, output_url: Optional[str] = None) -> bool:
        """Update project status"""
        if not check_credentials():
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                update_data = {"status": status}
                if output_url:
                    update_data["output_url"] = output_url
                
                response = await client.patch(
                    f"{SUPABASE_URL}/rest/v1/projects",
                    headers=get_headers(),
                    params={"id": f"eq.{project_id}"},
                    json=update_data
                )
                
                return response.status_code in [200, 204]
        except Exception as e:
            print(f"Error updating project: {e}")
            return False
    
    @staticmethod
    async def delete_project(project_id: int) -> bool:
        """Delete project"""
        if not check_credentials():
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"{SUPABASE_URL}/rest/v1/projects",
                    headers=get_headers(),
                    params={"id": f"eq.{project_id}"}
                )
                
                return response.status_code in [200, 204]
        except Exception as e:
            print(f"Error deleting project: {e}")
            return False


# ============================================================
# CUSTOM VOICE OPERATIONS
# ============================================================

class VoiceDB:
    """Custom voice database operations via REST API"""
    
    @staticmethod
    async def create_voice(
        user_id: int,
        voice_name: str,
        quality: str,
        samples_count: int,
        voice_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create custom voice"""
        if not check_credentials():
            return {"error": "Database credentials not available"}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{SUPABASE_URL}/rest/v1/voices",
                    headers=get_headers(),
                    json={
                        "user_id": user_id,
                        "voice_name": voice_name,
                        "quality": quality,
                        "samples_count": samples_count,
                        "voice_data": voice_data,
                        "is_active": True,
                        "created_at": datetime.now().isoformat()
                    }
                )
                
                if response.status_code in [200, 201]:
                    data = response.json()
                    return data[0] if isinstance(data, list) else data
                else:
                    return {"error": f"Failed to create voice: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    async def get_user_voices(user_id: int) -> List[Dict[str, Any]]:
        """Get all voices for a user"""
        if not check_credentials():
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{SUPABASE_URL}/rest/v1/voices",
                    headers=get_headers(),
                    params={
                        "user_id": f"eq.{user_id}",
                        "is_active": "eq.true",
                        "select": "*",
                        "order": "created_at.desc"
                    }
                )
                
                if response.status_code == 200:
                    return response.json()
                return []
        except Exception as e:
            print(f"Error getting voices: {e}")
            return []
    
    @staticmethod
    async def get_voice(voice_id: int) -> Optional[Dict[str, Any]]:
        """Get voice by ID"""
        if not check_credentials():
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{SUPABASE_URL}/rest/v1/voices",
                    headers=get_headers(),
                    params={"id": f"eq.{voice_id}", "select": "*"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data[0] if data else None
                return None
        except Exception as e:
            print(f"Error getting voice: {e}")
            return None
    
    @staticmethod
    async def delete_voice(voice_id: int) -> bool:
        """Delete voice (soft delete)"""
        if not check_credentials():
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"{SUPABASE_URL}/rest/v1/voices",
                    headers=get_headers(),
                    params={"id": f"eq.{voice_id}"},
                    json={"is_active": False}
                )
                
                return response.status_code in [200, 204]
        except Exception as e:
            print(f"Error deleting voice: {e}")
            return False


# ============================================================
# AUDIO FILE OPERATIONS
# ============================================================

class AudioDB:
    """Audio file database operations via REST API"""
    
    @staticmethod
    async def save_audio(
        user_id: int,
        project_id: Optional[int],
        filename: str,
        file_url: str,
        file_type: str,
        duration: Optional[str] = None,
        size_mb: Optional[float] = None
    ) -> Dict[str, Any]:
        """Save audio file metadata"""
        if not check_credentials():
            return {"error": "Database credentials not available"}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{SUPABASE_URL}/rest/v1/audios",
                    headers=get_headers(),
                    json={
                        "user_id": user_id,
                        "project_id": project_id,
                        "filename": filename,
                        "file_url": file_url,
                        "file_type": file_type,
                        "duration": duration,
                        "size_mb": size_mb,
                        "created_at": datetime.now().isoformat()
                    }
                )
                
                if response.status_code in [200, 201]:
                    data = response.json()
                    return data[0] if isinstance(data, list) else data
                else:
                    return {"error": f"Failed to save audio: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    async def get_user_audios(user_id: int) -> List[Dict[str, Any]]:
        """Get all audios for a user"""
        if not check_credentials():
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{SUPABASE_URL}/rest/v1/audios",
                    headers=get_headers(),
                    params={
                        "user_id": f"eq.{user_id}",
                        "select": "*",
                        "order": "created_at.desc"
                    }
                )
                
                if response.status_code == 200:
                    return response.json()
                return []
        except Exception as e:
            print(f"Error getting audios: {e}")
            return []


# ============================================================
# DATABASE INITIALIZATION & HELPERS
# ============================================================

async def init_database():
    """Initialize database - check connection"""
    if not check_credentials():
        print("⚠️  Database credentials not set")
        return False
    
    print("✅ Supabase REST API configured!")
    print(f"📍 URL: {SUPABASE_URL}")
    print("""
    📋 Required tables in Supabase:
    
    1. users (id, username, email, password_hash, full_name, is_active, created_at)
    2. projects (id, user_id, project_type, title, data, status, output_url, created_at)
    3. voices (id, user_id, voice_name, quality, samples_count, voice_data, is_active, created_at)
    4. audios (id, user_id, project_id, filename, file_url, file_type, duration, size_mb, created_at)
    
    Tables should already exist in your Supabase dashboard!
    """)
    return True


async def check_database_connection() -> bool:
    """Check if database credentials are available and can connect"""
    if not check_credentials():
        return False
    
    try:
        # Test connection with a simple query
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/users",
                headers=get_headers(),
                params={"select": "id", "limit": "0"}
            )
            return response.status_code == 200
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False
