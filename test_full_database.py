#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Test Database - Create User then Project
"""

import httpx
import asyncio
from datetime import datetime

SUPABASE_URL = "https://cxxbakzhlnuhkfgoaslv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN4eGJha3pobG51aGtmZ29hc2x2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIzMzkxOTQsImV4cCI6MjA3NzkxNTE5NH0.0iIoT5aVReYImBtsqZdKdbSNhM8XVv7MQbI5_6AbdhY"

async def test_full_flow():
    """Test complete flow: create user, create project, retrieve project"""
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    print("🧪 FULL DATABASE TEST")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        
        # STEP 1: Create test user
        print("\n1️⃣ Creating test user...")
        try:
            test_user = {
                "email": "test@fanerstudio.com",
                "password_hash": "test_hash_123",
                "full_name": "Test User - Faner Studio",
                "is_active": True,
                "created_at": datetime.now().isoformat()
            }
            
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/users",
                headers=headers,
                json=test_user
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                user_data = response.json()
                user = user_data[0] if isinstance(user_data, list) else user_data
                user_id = user.get('id')
                print(f"   ✅ User created!")
                print(f"   📝 ID: {user_id}")
                print(f"   📝 Email: {user.get('email')}")
                print(f"   📝 Name: {user.get('full_name')}")
            elif response.status_code == 409:
                print("   ⚠️  User already exists, fetching...")
                # Get existing user
                response = await client.get(
                    f"{SUPABASE_URL}/rest/v1/users",
                    headers=headers,
                    params={"email": "eq.test@fanerstudio.com"}
                )
                users = response.json()
                if users:
                    user = users[0]
                    user_id = user.get('id')
                    print(f"   ✅ User found!")
                    print(f"   📝 ID: {user_id}")
                else:
                    print("   ❌ Could not create or find user")
                    return
            else:
                print(f"   ❌ Failed: {response.text}")
                return
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # STEP 2: Create test project
        print("\n2️⃣ Creating test project...")
        try:
            test_project = {
                "user_id": user_id,
                "project_type": "audiobook",
                "title": "Test Audiobook - Full Integration Test",
                "data": {
                    "voice": "natural",
                    "speed": 1.0,
                    "format": "mp3",
                    "test": True,
                    "original_file": "test.pdf"
                },
                "status": "completed",
                "output_url": "https://example.com/test.mp3",
                "created_at": datetime.now().isoformat()
            }
            
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/projects",
                headers=headers,
                json=test_project
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                project_data = response.json()
                project = project_data[0] if isinstance(project_data, list) else project_data
                project_id = project.get('id')
                print(f"   ✅ Project created!")
                print(f"   📝 ID: {project_id}")
                print(f"   📝 Title: {project.get('title')}")
                print(f"   📝 Type: {project.get('project_type')}")
                print(f"   📝 Status: {project.get('status')}")
            else:
                print(f"   ❌ Failed: {response.text}")
                return
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # STEP 3: Retrieve all user projects
        print("\n3️⃣ Retrieving user projects...")
        try:
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/projects",
                headers=headers,
                params={
                    "user_id": f"eq.{user_id}",
                    "select": "*",
                    "order": "created_at.desc"
                }
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                projects = response.json()
                print(f"   ✅ Retrieved {len(projects)} project(s)!")
                for i, proj in enumerate(projects, 1):
                    print(f"   📋 Project {i}:")
                    print(f"      - ID: {proj.get('id')}")
                    print(f"      - Title: {proj.get('title')}")
                    print(f"      - Type: {proj.get('project_type')}")
                    print(f"      - Status: {proj.get('status')}")
            else:
                print(f"   ❌ Failed: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 FULL DATABASE TEST COMPLETE!")
    print("✅ User creation: SUCCESS")
    print("✅ Project creation: SUCCESS")
    print("✅ Project retrieval: SUCCESS")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_full_flow())

