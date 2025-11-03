#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Test Fanerstudio-2
Quick test for the new service
"""

import asyncio
import httpx
from datetime import datetime

BASE_URL = "https://fanerstudio-2.onrender.com"

ENDPOINTS = [
    ("/", "Main platform"),
    ("/health", "Health check"),
    ("/api/info", "API info"),
    ("/api/status", "System status"),
    ("/admin", "Admin dashboard"),
    ("/docs", "API documentation"),
    ("/api/translate", "Translation"),
    ("/api/performance/system", "Performance monitoring"),
    ("/api/voices", "Voice list"),
    ("/api/podcast/templates", "Podcast templates")
]

async def test_fanerstudio2():
    """Test fanerstudio-2 service"""
    
    print("="*60)
    print("🧪 TESTING FANERSTUDIO-2")
    print("="*60)
    print(f"URL: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    passed = 0
    failed = 0
    
    async with httpx.AsyncClient(timeout=15.0) as client:
        # Test service availability
        print("Checking service availability...")
        try:
            response = await client.get(BASE_URL)
            if response.status_code == 200:
                print("✅ Service is ONLINE\n")
            else:
                print(f"⚠️  Service returned: {response.status_code}\n")
        except Exception as e:
            print(f"❌ Service is OFFLINE: {e}\n")
            return
        
        # Test each endpoint
        print("Testing endpoints:")
        print("-" * 60)
        
        for endpoint, description in ENDPOINTS:
            try:
                response = await client.get(f"{BASE_URL}{endpoint}")
                if response.status_code == 200:
                    print(f"✅ {endpoint:30} {description}")
                    passed += 1
                else:
                    print(f"❌ {endpoint:30} Status: {response.status_code}")
                    failed += 1
            except Exception as e:
                print(f"❌ {endpoint:30} Error: {str(e)[:30]}")
                failed += 1
        
        print("-" * 60)
        print()
        
        # Summary
        total = passed + failed
        percentage = (passed / total * 100) if total > 0 else 0
        
        print("="*60)
        print("📊 RESULTS")
        print("="*60)
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {passed} ({percentage:.1f}%)")
        print(f"❌ Failed: {failed}")
        print()
        
        if passed == total:
            print("🎉 ALL TESTS PASSED!")
            print("✅ fanerstudio-2 is fully operational!")
        elif passed >= 8:
            print("✅ SERVICE WORKING WELL!")
            print("⚠️  Few minor issues detected")
        elif passed >= 5:
            print("⚠️  SERVICE PARTIALLY WORKING")
            print("Some endpoints need attention")
        else:
            print("❌ SERVICE HAS ISSUES")
            print("Check Render logs and configuration")
        
        print("="*60)

if __name__ == "__main__":
    asyncio.run(test_fanerstudio2())

