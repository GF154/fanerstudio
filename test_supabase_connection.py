#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Test Supabase Connection
Verify that Faner Studio is connected to Supabase
"""

import asyncio
import httpx

BASE_URL = "https://fanerstudio-1.onrender.com"

async def test_supabase_connection():
    """Test if platform is using Supabase"""
    
    print("="*60)
    print("🧪 TESTING SUPABASE CONNECTION")
    print("="*60)
    print(f"\nTarget: {BASE_URL}")
    print("Waiting for deployment to complete...\n")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        # Test 1: Health Check
        print("1️⃣  Testing health endpoint...")
        try:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Status: {data.get('status')}")
            else:
                print(f"   ⚠️  Status code: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 2: System Status (should show database info)
        print("\n2️⃣  Testing system status...")
        try:
            response = await client.get(f"{BASE_URL}/api/status")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Service: {data.get('service')}")
                print(f"   ✅ Environment: {data.get('environment')}")
                deployment = data.get('deployment', {})
                print(f"   ✅ Platform: {deployment.get('platform')}")
            else:
                print(f"   ⚠️  Status code: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 3: Performance System (checks if database is accessible)
        print("\n3️⃣  Testing performance/system endpoint...")
        try:
            response = await client.get(f"{BASE_URL}/api/performance/system")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Cache enabled: {data.get('cache_enabled')}")
                print(f"   ✅ Database enabled: {data.get('database_enabled')}")
                if data.get('database_enabled'):
                    print("   🎉 DATABASE IS CONNECTED!")
                else:
                    print("   ⚠️  Database not enabled")
            else:
                print(f"   ⚠️  Status code: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 4: Try to access authentication endpoint
        print("\n4️⃣  Testing authentication endpoint...")
        try:
            response = await client.get(f"{BASE_URL}/api/auth/me")
            # Should return 401 (unauthorized) - that's good, means it's working
            if response.status_code == 401:
                print("   ✅ Auth endpoint working (401 expected)")
            elif response.status_code == 503:
                print("   ⚠️  Database not available (503)")
            else:
                print(f"   ⚠️  Status code: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "="*60)
    print("🎯 TEST SUMMARY")
    print("="*60)
    print("If you see '✅ DATABASE IS CONNECTED!' above,")
    print("then Supabase integration is SUCCESSFUL!")
    print("\nIf not, wait a few more minutes for deployment")
    print("to complete, then run this test again.")
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(test_supabase_connection())

