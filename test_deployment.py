#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Deployment Validation Script
Tests all deployment requirements and configurations
"""

import sys
import os
from pathlib import Path

def test_files_exist():
    """Test that all required files exist"""
    print("\n🔍 Testing Required Files...")
    
    required_files = [
        "main.py",
        "requirements.txt",
        ".github/workflows/render-deploy.yml",
        "projet_kreyol_IA/render.yaml"
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} NOT FOUND")
            all_exist = False
    
    return all_exist

def test_python_version():
    """Test Python version"""
    print("\n🐍 Testing Python Version...")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"  Current: Python {version_str}")
    
    if version.major == 3 and version.minor >= 11:
        print(f"  ✅ Python version is compatible")
        return True
    else:
        print(f"  ⚠️  Recommended: Python 3.11+")
        return True  # Still pass but warn

def test_imports():
    """Test critical imports"""
    print("\n📦 Testing Critical Imports...")
    
    modules = {
        "fastapi": "FastAPI",
        "uvicorn": "Uvicorn",
        "httpx": "HTTPX",
        "pydantic": "Pydantic"
    }
    
    all_imported = True
    for module, name in modules.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - NOT INSTALLED")
            all_imported = False
    
    return all_imported

def test_main_py():
    """Test main.py can be imported"""
    print("\n🚀 Testing main.py...")
    
    try:
        import main
        print(f"  ✅ main.py imports successfully")
        print(f"  ✅ App title: {main.app.title}")
        print(f"  ✅ App version: {main.app.version}")
        return True
    except Exception as e:
        print(f"  ❌ Error importing main.py: {e}")
        return False

def test_endpoints():
    """Test that endpoints are defined"""
    print("\n🔗 Testing API Endpoints...")
    
    try:
        import main
        
        routes = [route.path for route in main.app.routes]
        
        expected_endpoints = [
            "/",
            "/health",
            "/api/info",
            "/api/status",
            "/api/translate",
            "/docs",
            "/redoc"
        ]
        
        all_present = True
        for endpoint in expected_endpoints:
            if endpoint in routes:
                print(f"  ✅ {endpoint}")
            else:
                print(f"  ❌ {endpoint} - NOT FOUND")
                all_present = False
        
        return all_present
    except Exception as e:
        print(f"  ❌ Error testing endpoints: {e}")
        return False

def test_render_config():
    """Test render.yaml configuration"""
    print("\n☁️  Testing Render Configuration...")
    
    try:
        import yaml
        
        config_path = Path("projet_kreyol_IA/render.yaml")
        if not config_path.exists():
            print(f"  ⚠️  render.yaml not found (optional)")
            return True
        
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        if config and "services" in config:
            service = config["services"][0]
            print(f"  ✅ Service name: {service.get('name')}")
            print(f"  ✅ Start command: {service.get('startCommand')}")
            print(f"  ✅ Health check: {service.get('healthCheckPath')}")
            return True
        else:
            print(f"  ❌ Invalid render.yaml structure")
            return False
            
    except ImportError:
        print(f"  ℹ️  PyYAML not installed (optional)")
        return True
    except Exception as e:
        print(f"  ❌ Error reading render.yaml: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("🔍 DEPLOYMENT VALIDATION")
    print("="*60)
    
    tests = [
        test_files_exist,
        test_python_version,
        test_imports,
        test_main_py,
        test_endpoints,
        test_render_config
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ ALL TESTS PASSED ({passed}/{total})")
        print("="*60)
        print("\n🎉 Ready for deployment!")
        print("\nNext steps:")
        print("  1. Commit changes: git add . && git commit -m 'your message'")
        print("  2. Push to GitHub: git push")
        print("  3. GitHub Actions will auto-deploy to Render")
        return 0
    else:
        print(f"⚠️  SOME TESTS FAILED ({passed}/{total})")
        print("="*60)
        print("\n⚠️  Please fix the issues above before deploying")
        return 1

if __name__ == "__main__":
    sys.exit(main())

