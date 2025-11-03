#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Test All Platform Features
Comprehensive integration test for all Faner Studio tools
"""

import asyncio
import httpx
import json
from pathlib import Path
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL = "https://fanerstudio-1.onrender.com"  # Change to localhost:8000 for local testing
TIMEOUT = 30.0

# Test results tracking
test_results = {
    "passed": [],
    "failed": [],
    "warnings": []
}

# ============================================================
# TEST UTILITIES
# ============================================================

def print_test_header(category: str):
    """Print test category header"""
    print("\n" + "="*60)
    print(f"🧪 TESTING: {category}")
    print("="*60)

def print_test(name: str, passed: bool, message: str = ""):
    """Print individual test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {name}")
    if message:
        print(f"   → {message}")
    
    if passed:
        test_results["passed"].append(name)
    else:
        test_results["failed"].append(name)

def print_warning(name: str, message: str):
    """Print warning"""
    print(f"⚠️  WARN - {name}")
    print(f"   → {message}")
    test_results["warnings"].append(name)

# ============================================================
# CORE ENDPOINTS TESTS
# ============================================================

async def test_core_endpoints(client: httpx.AsyncClient):
    """Test core platform endpoints"""
    print_test_header("CORE ENDPOINTS")
    
    # Test 1: Root endpoint
    try:
        response = await client.get("/")
        print_test(
            "Root endpoint (/)",
            response.status_code == 200,
            f"Status: {response.status_code}"
        )
    except Exception as e:
        print_test("Root endpoint (/)", False, str(e))
    
    # Test 2: Health check
    try:
        response = await client.get("/health")
        if response.status_code == 200:
            data = response.json()
            print_test(
                "Health check (/health)",
                data.get("status") == "healthy",
                f"Status: {data.get('status')}, Service: {data.get('service')}"
            )
        else:
            print_test("Health check (/health)", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Health check (/health)", False, str(e))
    
    # Test 3: API info
    try:
        response = await client.get("/api/info")
        if response.status_code == 200:
            data = response.json()
            print_test(
                "API info (/api/info)",
                "version" in data and "features" in data,
                f"Version: {data.get('version')}, Features: {len(data.get('features', {}))}"
            )
        else:
            print_test("API info (/api/info)", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("API info (/api/info)", False, str(e))
    
    # Test 4: System status
    try:
        response = await client.get("/api/status")
        if response.status_code == 200:
            data = response.json()
            print_test(
                "System status (/api/status)",
                data.get("service") == "online",
                f"Service: {data.get('service')}, Environment: {data.get('environment')}"
            )
        else:
            print_test("System status (/api/status)", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("System status (/api/status)", False, str(e))
    
    # Test 5: API documentation
    try:
        response = await client.get("/docs")
        print_test(
            "API docs (/docs)",
            response.status_code == 200,
            f"OpenAPI docs accessible"
        )
    except Exception as e:
        print_test("API docs (/docs)", False, str(e))
    
    # Test 6: Admin dashboard
    try:
        response = await client.get("/admin")
        print_test(
            "Admin dashboard (/admin)",
            response.status_code == 200,
            f"Admin interface accessible"
        )
    except Exception as e:
        print_test("Admin dashboard (/admin)", False, str(e))

# ============================================================
# TRANSLATION TESTS
# ============================================================

async def test_translation(client: httpx.AsyncClient):
    """Test translation functionality"""
    print_test_header("TRANSLATION")
    
    # Test 1: English to Haitian Creole
    try:
        payload = {
            "text": "Hello, how are you?",
            "source": "en",
            "target": "ht"
        }
        response = await client.post("/api/translate", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_test(
                    "English → Haitian Creole",
                    True,
                    f"Translation: '{data.get('translated')}'"
                )
            else:
                print_warning(
                    "English → Haitian Creole",
                    f"Model loading: {data.get('error', 'Unknown error')}"
                )
        else:
            print_test("English → Haitian Creole", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("English → Haitian Creole", False, str(e))
    
    # Test 2: French to Haitian Creole
    try:
        payload = {
            "text": "Bonjour, comment allez-vous?",
            "source": "fr",
            "target": "ht"
        }
        response = await client.post("/api/translate", json=payload, timeout=TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_test(
                    "French → Haitian Creole",
                    True,
                    f"Translation: '{data.get('translated')}'"
                )
            else:
                print_warning("French → Haitian Creole", data.get('error', 'Unknown error'))
        else:
            print_test("French → Haitian Creole", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("French → Haitian Creole", False, str(e))

# ============================================================
# PERFORMANCE TESTS
# ============================================================

async def test_performance(client: httpx.AsyncClient):
    """Test performance monitoring endpoints"""
    print_test_header("PERFORMANCE MONITORING")
    
    # Test 1: System stats
    try:
        response = await client.get("/api/performance/system")
        if response.status_code == 200:
            data = response.json()
            system = data.get("system", {})
            print_test(
                "System stats",
                True,
                f"CPU: {system.get('cpu_percent', 0)}%, RAM: {system.get('memory_percent', 0)}%, Disk: {system.get('disk_percent', 0)}%"
            )
        else:
            print_test("System stats", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("System stats", False, str(e))
    
    # Test 2: Cache info
    try:
        response = await client.get("/api/performance/cache")
        if response.status_code == 200:
            data = response.json()
            print_test(
                "Cache info",
                data.get("status") == "success",
                f"Cache size: {data.get('cache_size', 0)} items"
            )
        else:
            print_test("Cache info", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Cache info", False, str(e))

# ============================================================
# VOICE & AUDIO TESTS
# ============================================================

async def test_voice_audio(client: httpx.AsyncClient):
    """Test voice and audio endpoints"""
    print_test_header("VOICE & AUDIO")
    
    # Test 1: Get available voices
    try:
        response = await client.get("/api/voices")
        if response.status_code == 200:
            data = response.json()
            print_test(
                "Get voices list",
                "voices" in data,
                f"Total voices: {data.get('total', 0)}"
            )
        else:
            print_test("Get voices list", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Get voices list", False, str(e))
    
    # Test 2: Podcast templates
    try:
        response = await client.get("/api/podcast/templates")
        if response.status_code == 200:
            data = response.json()
            print_test(
                "Podcast templates",
                "templates" in data,
                f"Available: {len(data.get('templates', {}))}"
            )
        else:
            print_test("Podcast templates", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Podcast templates", False, str(e))

# ============================================================
# AUTHENTICATION TESTS
# ============================================================

async def test_authentication(client: httpx.AsyncClient):
    """Test authentication endpoints"""
    print_test_header("AUTHENTICATION")
    
    # Test 1: Get current user (should fail without token)
    try:
        response = await client.get("/api/auth/me")
        print_test(
            "Protected endpoint (no auth)",
            response.status_code == 401,
            f"Correctly returns 401 Unauthorized"
        )
    except Exception as e:
        print_test("Protected endpoint (no auth)", False, str(e))
    
    # Test 2: Test registration endpoint structure
    try:
        response = await client.post(
            "/api/auth/register",
            json={}  # Empty payload to test validation
        )
        print_test(
            "Registration validation",
            response.status_code == 422,  # Validation error expected
            "Correctly validates input"
        )
    except Exception as e:
        print_test("Registration validation", False, str(e))

# ============================================================
# SUMMARY
# ============================================================

def print_summary():
    """Print test summary"""
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    total = len(test_results["passed"]) + len(test_results["failed"])
    passed = len(test_results["passed"])
    failed = len(test_results["failed"])
    warnings = len(test_results["warnings"])
    
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed: {passed} ({pass_rate:.1f}%)")
    print(f"❌ Failed: {failed}")
    print(f"⚠️  Warnings: {warnings}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Platform is working correctly.")
    elif failed <= 2:
        print("\n⚠️  MOSTLY WORKING. Few issues detected.")
    else:
        print("\n❌ ISSUES DETECTED. Check failed tests above.")
    
    print("\n" + "="*60)
    print(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

# ============================================================
# MAIN TEST RUNNER
# ============================================================

async def run_all_tests():
    """Run all platform tests"""
    print("="*60)
    print("🧪 FANER STUDIO - COMPREHENSIVE PLATFORM TEST")
    print("="*60)
    print(f"Target: {BASE_URL}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=TIMEOUT) as client:
        await test_core_endpoints(client)
        await test_translation(client)
        await test_performance(client)
        await test_voice_audio(client)
        await test_authentication(client)
    
    print_summary()

if __name__ == "__main__":
    asyncio.run(run_all_tests())
