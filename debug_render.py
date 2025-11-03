#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Debug Render Deployment
Check what Render is actually running
"""

import asyncio
import httpx
import json

BASE_URL = "https://fanerstudio-2.onrender.com"

async def debug_render():
    """Debug what Render is serving"""
    
    print("="*60)
    print("🔍 DEBUGGING RENDER DEPLOYMENT")
    print("="*60)
    print(f"Service: {BASE_URL}\n")
    
    async with httpx.AsyncClient(timeout=15.0) as client:
        # Check health endpoint
        print("1. Checking /health endpoint...")
        try:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                data = response.json()
                print("✅ Health check passed")
                print(f"   Service: {data.get('service', 'Unknown')}")
                print(f"   Version: {data.get('version', 'Unknown')}")
                print(f"   Deployment: {data.get('deployment', 'Unknown')}")
                
                # Check features
                features = data.get('features', {})
                if features:
                    print(f"\n   Features found:")
                    for feature, status in features.items():
                        print(f"      {feature}: {status}")
                print()
            else:
                print(f"❌ Status: {response.status_code}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")
        
        # Check if FastAPI docs show all endpoints
        print("2. Checking /docs (OpenAPI schema)...")
        try:
            response = await client.get(f"{BASE_URL}/openapi.json")
            if response.status_code == 200:
                schema = response.json()
                paths = schema.get('paths', {})
                print(f"✅ OpenAPI schema loaded")
                print(f"   Total endpoints in schema: {len(paths)}")
                print(f"\n   Endpoints found:")
                for path in sorted(paths.keys()):
                    methods = list(paths[path].keys())
                    print(f"      {path:40} {', '.join(methods).upper()}")
                print()
            else:
                print(f"❌ Status: {response.status_code}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")
        
        # Test a known new endpoint
        print("3. Testing /api/status (should exist in new code)...")
        try:
            response = await client.get(f"{BASE_URL}/api/status")
            if response.status_code == 200:
                print("✅ /api/status EXISTS - New code is deployed!")
                data = response.json()
                print(f"   Python version: {data.get('python_version')}")
                print(f"   Platform: {data.get('platform')}")
            elif response.status_code == 404:
                print("❌ /api/status NOT FOUND - Old code still running!")
                print("   Render is NOT using the latest code")
            else:
                print(f"⚠️  Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    print("="*60)
    print("DIAGNOSIS")
    print("="*60)
    
    print("""
If /api/status returns 404:
→ Render is running OLD code
→ Need to check Render service configuration

Possible causes:
1. Wrong branch selected (should be 'master')
2. Wrong start command
3. Build failed and using cached version
4. Root directory not empty

SOLUTION:
1. Go to Render Dashboard
2. Select fanerstudio-2
3. Check Settings → Build & Deploy:
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
4. Check Settings → General:
   Branch: master
   Root Directory: (empty)
5. Manual Deploy → Clear build cache → Deploy
    """)
    
    print("="*60)

if __name__ == "__main__":
    asyncio.run(debug_render())

