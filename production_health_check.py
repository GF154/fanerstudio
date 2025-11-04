#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Production Health Check Script
Test all endpoints on production after deployment
"""

import httpx
import asyncio
from typing import Dict, List
import sys
from datetime import datetime


class ProductionHealthCheck:
    """Comprehensive production health check"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
    
    async def run_all_checks(self) -> Dict:
        """Run all health checks"""
        print("\n" + "="*60)
        print(f"🏥 PRODUCTION HEALTH CHECK")
        print(f"🌐 Base URL: {self.base_url}")
        print(f"⏰ Time: {datetime.now().isoformat()}")
        print("="*60 + "\n")
        
        # Core endpoints
        await self.check_endpoint("GET", "/", "Main page")
        await self.check_endpoint("GET", "/health", "Health check")
        await self.check_endpoint("GET", "/api/info", "API info")
        await self.check_endpoint("GET", "/api/status", "System status")
        await self.check_endpoint("GET", "/docs", "API documentation")
        
        # Translation
        await self.check_translation()
        
        # Voice management
        await self.check_endpoint("GET", "/api/voices", "List voices")
        
        # Podcast templates
        await self.check_endpoint("GET", "/api/podcast/templates", "Podcast templates")
        
        # Admin (should require auth)
        await self.check_endpoint("GET", "/admin", "Admin dashboard", expect_status=200)
        
        # Print summary
        self.print_summary()
        
        return {
            "total": self.total_tests,
            "passed": self.passed_tests,
            "failed": self.failed_tests,
            "success_rate": (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0,
            "results": self.results
        }
    
    async def check_endpoint(
        self, 
        method: str, 
        path: str, 
        description: str,
        expect_status: int = 200,
        timeout: float = 30.0
    ):
        """Check single endpoint"""
        self.total_tests += 1
        url = f"{self.base_url}{path}"
        
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                if method == "GET":
                    response = await client.get(url)
                elif method == "POST":
                    response = await client.post(url)
                else:
                    raise ValueError(f"Unsupported method: {method}")
                
                if response.status_code == expect_status:
                    self.passed_tests += 1
                    print(f"✅ {description}: {response.status_code} OK")
                    self.results.append({
                        "test": description,
                        "status": "PASS",
                        "status_code": response.status_code,
                        "url": url
                    })
                else:
                    self.failed_tests += 1
                    print(f"❌ {description}: Expected {expect_status}, got {response.status_code}")
                    self.results.append({
                        "test": description,
                        "status": "FAIL",
                        "status_code": response.status_code,
                        "expected": expect_status,
                        "url": url
                    })
        
        except Exception as e:
            self.failed_tests += 1
            print(f"❌ {description}: ERROR - {str(e)}")
            self.results.append({
                "test": description,
                "status": "ERROR",
                "error": str(e),
                "url": url
            })
    
    async def check_translation(self):
        """Test translation endpoint"""
        self.total_tests += 1
        url = f"{self.base_url}/api/translate"
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    url,
                    json={
                        "text": "Hello, how are you?",
                        "source": "en",
                        "target": "ht"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        self.passed_tests += 1
                        print(f"✅ Translation: Working ({data.get('translated', 'N/A')})")
                        self.results.append({
                            "test": "Translation",
                            "status": "PASS",
                            "result": data
                        })
                    else:
                        self.failed_tests += 1
                        print(f"❌ Translation: Failed - {data.get('error', 'Unknown error')}")
                        self.results.append({
                            "test": "Translation",
                            "status": "FAIL",
                            "error": data.get("error")
                        })
                else:
                    self.failed_tests += 1
                    print(f"❌ Translation: Status {response.status_code}")
                    self.results.append({
                        "test": "Translation",
                        "status": "FAIL",
                        "status_code": response.status_code
                    })
        
        except Exception as e:
            self.failed_tests += 1
            print(f"❌ Translation: ERROR - {str(e)}")
            self.results.append({
                "test": "Translation",
                "status": "ERROR",
                "error": str(e)
            })
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        
        if self.total_tests > 0:
            success_rate = (self.passed_tests / self.total_tests * 100)
            print(f"📈 Success Rate: {success_rate:.1f}%")
        
        print("="*60 + "\n")
        
        if self.failed_tests == 0:
            print("🎉 ALL TESTS PASSED! Production is healthy!")
        else:
            print("⚠️  SOME TESTS FAILED! Check issues above.")


async def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python production_health_check.py <base_url>")
        print("Example: python production_health_check.py https://fanerstudio.vercel.app")
        sys.exit(1)
    
    base_url = sys.argv[1]
    
    checker = ProductionHealthCheck(base_url)
    results = await checker.run_all_checks()
    
    # Exit with appropriate code
    sys.exit(0 if results["failed"] == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())

