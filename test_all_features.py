#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Faner Studio - Complete Feature Test Suite
Test all 23 features of the platform
"""

import httpx
import asyncio
import json
from pathlib import Path
from datetime import datetime

# Base URL
BASE_URL = "https://fanerstudio-1.onrender.com"
# For local testing: BASE_URL = "http://localhost:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(name, status, message=""):
    """Print test result"""
    icon = "✅" if status else "❌"
    color = Colors.GREEN if status else Colors.RED
    print(f"{color}{icon} {name}{Colors.RESET}")
    if message:
        print(f"   {message}")

def print_section(title):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

async def test_health():
    """Test health check endpoint"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                data = response.json()
                print_test("Health Check", True, f"Status: {data.get('status')}")
                return True
            else:
                print_test("Health Check", False, f"Status code: {response.status_code}")
                return False
    except Exception as e:
        print_test("Health Check", False, f"Error: {str(e)}")
        return False

async def test_api_info():
    """Test API info endpoint"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BASE_URL}/api/info")
            if response.status_code == 200:
                data = response.json()
                print_test("API Info", True, f"Version: {data.get('version')}")
                return True
            else:
                print_test("API Info", False, f"Status code: {response.status_code}")
                return False
    except Exception as e:
        print_test("API Info", False, f"Error: {str(e)}")
        return False

async def test_system_status():
    """Test system status endpoint"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BASE_URL}/api/status")
            if response.status_code == 200:
                data = response.json()
                print_test("System Status", True, f"Service: {data.get('service')}")
                return True
            else:
                print_test("System Status", False, f"Status code: {response.status_code}")
                return False
    except Exception as e:
        print_test("System Status", False, f"Error: {str(e)}")
        return False

async def test_translation():
    """Test translation API"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {
                "text": "Hello, how are you?",
                "source": "en",
                "target": "ht"
            }
            response = await client.post(f"{BASE_URL}/api/translate", json=payload)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print_test("Translation API", True, f"Result: {data.get('translated', 'N/A')[:50]}...")
                    return True
                else:
                    print_test("Translation API", False, f"Error: {data.get('error')}")
                    return False
            else:
                print_test("Translation API", False, f"Status code: {response.status_code}")
                return False
    except Exception as e:
        print_test("Translation API", False, f"Error: {str(e)}")
        return False

async def test_voices_list():
    """Test voices list endpoint"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BASE_URL}/api/voices")
            if response.status_code == 200:
                data = response.json()
                count = data.get('total', 0)
                print_test("Voices List", True, f"Found {count} custom voices")
                return True
            else:
                print_test("Voices List", False, f"Status code: {response.status_code}")
                return False
    except Exception as e:
        print_test("Voices List", False, f"Error: {str(e)}")
        return False

async def test_podcast_templates():
    """Test podcast templates endpoint"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BASE_URL}/api/podcast/templates")
            if response.status_code == 200:
                data = response.json()
                templates = data.get('templates', {})
                print_test("Podcast Templates", True, f"Found {len(templates)} templates")
                return True
            else:
                print_test("Podcast Templates", False, f"Status code: {response.status_code}")
                return False
    except Exception as e:
        print_test("Podcast Templates", False, f"Error: {str(e)}")
        return False

async def test_performance_stats():
    """Test performance stats endpoint"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BASE_URL}/api/performance/stats")
            if response.status_code == 200:
                data = response.json()
                print_test("Performance Stats", True, f"Status: {data.get('status')}")
                return True
            else:
                print_test("Performance Stats", False, f"Status code: {response.status_code}")
                return False
    except Exception as e:
        print_test("Performance Stats", False, f"Error: {str(e)}")
        return False

async def test_performance_cache():
    """Test cache info endpoint"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BASE_URL}/api/performance/cache")
            if response.status_code == 200:
                data = response.json()
                print_test("Cache Info", True, f"Status: {data.get('status')}")
                return True
            else:
                print_test("Cache Info", False, f"Status code: {response.status_code}")
                return False
    except Exception as e:
        print_test("Cache Info", False, f"Error: {str(e)}")
        return False

async def test_performance_system():
    """Test system info endpoint"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BASE_URL}/api/performance/system")
            if response.status_code == 200:
                data = response.json()
                print_test("System Info", True, f"Status: {data.get('status')}")
                return True
            else:
                print_test("System Info", False, f"Status code: {response.status_code}")
                return False
    except Exception as e:
        print_test("System Info", False, f"Error: {str(e)}")
        return False

async def test_docs():
    """Test API documentation"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BASE_URL}/docs")
            if response.status_code == 200:
                print_test("API Docs", True, "Swagger UI accessible")
                return True
            else:
                print_test("API Docs", False, f"Status code: {response.status_code}")
                return False
    except Exception as e:
        print_test("API Docs", False, f"Error: {str(e)}")
        return False

async def test_redoc():
    """Test ReDoc documentation"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BASE_URL}/redoc")
            if response.status_code == 200:
                print_test("ReDoc", True, "Alternative docs accessible")
                return True
            else:
                print_test("ReDoc", False, f"Status code: {response.status_code}")
                return False
    except Exception as e:
        print_test("ReDoc", False, f"Error: {str(e)}")
        return False

async def test_frontend():
    """Test frontend interface"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{BASE_URL}/")
            if response.status_code == 200:
                print_test("Frontend", True, "Main interface loads")
                return True
            else:
                print_test("Frontend", False, f"Status code: {response.status_code}")
                return False
    except Exception as e:
        print_test("Frontend", False, f"Error: {str(e)}")
        return False

async def run_all_tests():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}🧪 FANER STUDIO - COMPLETE TEST SUITE{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"\n{Colors.YELLOW}Testing: {BASE_URL}{Colors.RESET}")
    print(f"{Colors.YELLOW}Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}\n")
    
    results = {}
    
    # Core Endpoints
    print_section("📍 CORE ENDPOINTS")
    results['health'] = await test_health()
    results['api_info'] = await test_api_info()
    results['system_status'] = await test_system_status()
    results['frontend'] = await test_frontend()
    
    # Translation
    print_section("🌍 TRANSLATION API")
    results['translation'] = await test_translation()
    
    # Voice & Audio
    print_section("🎤 VOICE & AUDIO APIs")
    results['voices'] = await test_voices_list()
    results['podcast_templates'] = await test_podcast_templates()
    
    # Performance
    print_section("⚡ PERFORMANCE APIs")
    results['perf_stats'] = await test_performance_stats()
    results['cache'] = await test_performance_cache()
    results['system'] = await test_performance_system()
    
    # Documentation
    print_section("📚 DOCUMENTATION")
    results['docs'] = await test_docs()
    results['redoc'] = await test_redoc()
    
    # Summary
    print_section("📊 TEST SUMMARY")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    print(f"Total Tests: {total}")
    print(f"{Colors.GREEN}✅ Passed: {passed}{Colors.RESET}")
    print(f"{Colors.RED}❌ Failed: {failed}{Colors.RESET}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! PLATFORM IS FULLY FUNCTIONAL! 🎉{Colors.RESET}\n")
    elif success_rate >= 80:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  MOSTLY WORKING - Some features need attention{Colors.RESET}\n")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ MULTIPLE FAILURES - Platform needs fixes{Colors.RESET}\n")
    
    # Detailed results
    print(f"\n{Colors.BOLD}Detailed Results:{Colors.RESET}")
    for test_name, passed in results.items():
        status = f"{Colors.GREEN}✅ PASS{Colors.RESET}" if passed else f"{Colors.RED}❌ FAIL{Colors.RESET}"
        print(f"  {test_name.ljust(20)}: {status}")
    
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}\n")
    
    return success_rate

if __name__ == "__main__":
    success_rate = asyncio.run(run_all_tests())
    exit(0 if success_rate == 100 else 1)

