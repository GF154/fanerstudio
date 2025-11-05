#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Test Supabase Database - Create Test Project
Test if we can save projects to Supabase
"""

import httpx
import asyncio
from datetime import datetime

# Supabase credentials
SUPABASE_URL = "https://cxxbakzhlnuhkfgoaslv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN4eGJha3pobG51aGtmZ29hc2x2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIzMzkxOTQsImV4cCI6MjA3NzkxNTE5NH0.0iIoT5aVReYImBtsqZdKdbSNhM8XVv7MQbI5_6AbdhY"

async def test_database():
    """Test database connection and create a test project"""
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    print("🧪 Testing Supabase Database Connection...")
    print(f"📍 URL: {SUPABASE_URL}")
    print()
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        
        # TEST 1: Check users table
        print("1️⃣ Testing users table...")
        try:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/users",
                headers=headers,
                params={"select": "id", "limit": "1"}
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Users table accessible!")
            else:
                print(f"   ❌ Failed: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
        
        # TEST 2: Create a test project
        print("2️⃣ Creating test project...")
        try:
            test_project = {
                "user_id": 1,
                "project_type": "audiobook",
                "title": "Test Audiobook - Database Connection Test",
                "data": {
                    "voice": "natural",
                    "speed": 1.0,
                    "format": "mp3",
                    "test": True
                },
                "status": "completed",
                "created_at": datetime.now().isoformat()
            }
            
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/projects",
                headers=headers,
                json=test_project
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                data = response.json()
                project = data[0] if isinstance(data, list) else data
                print(f"   ✅ Project created!")
                print(f"   📝 ID: {project.get('id')}")
                print(f"   📝 Title: {project.get('title')}")
                print(f"   📝 Type: {project.get('project_type')}")
                return project
            else:
                print(f"   ❌ Failed: {response.text}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
        
        print()
        
        # TEST 3: Retrieve the project
        if response.status_code in [200, 201]:
            print("3️⃣ Retrieving test project...")
            try:
                response = await client.get(
                    f"{SUPABASE_URL}/rest/v1/projects",
                    headers=headers,
                    params={
                        "user_id": "eq.1",
                        "project_type": "eq.audiobook",
                        "select": "*",
                        "order": "created_at.desc",
                        "limit": "1"
                    }
                )
                
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    projects = response.json()
                    if projects:
                        project = projects[0]
                        print(f"   ✅ Project retrieved!")
                        print(f"   📝 ID: {project.get('id')}")
                        print(f"   📝 Title: {project.get('title')}")
                        print(f"   📝 Status: {project.get('status')}")
                    else:
                        print("   ⚠️  No projects found")
                else:
                    print(f"   ❌ Failed: {response.text}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            print()
    
    print("=" * 60)
    print("🎉 DATABASE TEST COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_database())

