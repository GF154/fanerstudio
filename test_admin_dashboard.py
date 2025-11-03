#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Test Admin Dashboard
Test all admin endpoints and functionality
"""

import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000"  # Change to your deployment URL if testing production
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

async def test_admin_dashboard():
    """Test admin dashboard endpoints"""
    
    print("="*60)
    print("🧪 TESTING ADMIN DASHBOARD")
    print("="*60)
    print()
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        # Test 1: Login as admin
        print("1️⃣  Testing admin login...")
        try:
            form_data = {
                "username": ADMIN_USERNAME,
                "password": ADMIN_PASSWORD
            }
            
            response = await client.post(
                f"{BASE_URL}/api/auth/login",
                data=form_data
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                print(f"   ✅ Login successful")
                print(f"   🔑 Token: {token[:20]}...")
            else:
                print(f"   ❌ Login failed: {response.status_code}")
                print(f"   💡 Create admin user first with test_database.py")
                return
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # Set auth header for subsequent requests
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test 2: Get admin stats
        print("\n2️⃣  Testing admin stats endpoint...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/admin/stats",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Stats retrieved:")
                print(f"      Total Users: {data.get('total_users')}")
                print(f"      Total Projects: {data.get('total_projects')}")
                print(f"      Total Voices: {data.get('total_voices')}")
                print(f"      New Users (7d): {data.get('users_this_week')}")
            elif response.status_code == 403:
                print(f"   ❌ Access denied: User is not admin")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 3: Get all users
        print("\n3️⃣  Testing get all users endpoint...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/admin/users?limit=10",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Users retrieved: {data.get('total')} total")
                for user in data.get('users', [])[:3]:
                    print(f"      - {user['username']} ({user['email']})")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 4: Get all projects
        print("\n4️⃣  Testing get all projects endpoint...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/admin/projects?limit=10",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Projects retrieved: {data.get('total')} total")
                for project in data.get('projects', [])[:3]:
                    print(f"      - {project['title']} ({project['project_type']}) - {project['status']}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 5: Get all voices
        print("\n5️⃣  Testing get all voices endpoint...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/admin/voices?limit=10",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Voices retrieved: {data.get('total')} total")
                for voice in data.get('voices', [])[:3]:
                    print(f"      - {voice['voice_name']} ({voice['language']}) - Used {voice['times_used']}x")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 6: System monitoring
        print("\n6️⃣  Testing system monitoring endpoint...")
        try:
            response = await client.get(f"{BASE_URL}/api/performance/system")
            
            if response.status_code == 200:
                data = response.json()
                system = data.get('system', {})
                print(f"   ✅ System stats:")
                print(f"      CPU: {system.get('cpu_percent', 0)}%")
                print(f"      Memory: {system.get('memory_percent', 0)}%")
                print(f"      Disk: {system.get('disk_percent', 0)}%")
                print(f"      Cache: {'Enabled' if data.get('cache_enabled') else 'Disabled'}")
                print(f"      Database: {'Enabled' if data.get('database_enabled') else 'Disabled'}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 7: Access admin dashboard HTML
        print("\n7️⃣  Testing admin dashboard HTML...")
        try:
            response = await client.get(f"{BASE_URL}/admin")
            
            if response.status_code == 200:
                print(f"   ✅ Admin dashboard accessible")
                print(f"   📄 Content-Type: {response.headers.get('content-type')}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "="*60)
    print("🎯 TEST SUMMARY")
    print("="*60)
    print("All admin dashboard tests completed!")
    print()
    print("🌐 Open admin dashboard in browser:")
    print(f"   {BASE_URL}/admin")
    print()
    print("🔐 Login credentials:")
    print(f"   Username: {ADMIN_USERNAME}")
    print(f"   Password: {ADMIN_PASSWORD}")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_admin_dashboard())

