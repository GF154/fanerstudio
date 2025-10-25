#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration Tests
Test Entegrasyon
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Test that all modules can be imported"""
    print("=" * 60)
    print("🧪 TEST: Import All Modules")
    print("=" * 60)
    
    modules = [
        'utils.cloud_storage',
        'utils.email_notifier',
        'utils.metadata_manager',
        'utils.text_extraction',
        'utils.translate',
        'utils.audio_gen',
        'utils.podcast_mix',
    ]
    
    failed = []
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except Exception as e:
            print(f"❌ {module}: {e}")
            failed.append(module)
    
    if failed:
        print(f"\n❌ {len(failed)} module(s) failed to import")
        return False
    else:
        print(f"\n✅ All {len(modules)} modules imported successfully")
        return True


def test_environment():
    """Test environment configuration"""
    print("\n" + "=" * 60)
    print("🧪 TEST: Environment Configuration")
    print("=" * 60)
    
    bucket = os.getenv("GCS_BUCKET_NAME")
    
    if bucket:
        print(f"✅ GCS_BUCKET_NAME: {bucket}")
    else:
        print("⚠️  GCS_BUCKET_NAME not set (optional for tests)")
    
    sender = os.getenv("SENDER_EMAIL")
    if sender:
        print(f"✅ Email configured: {sender}")
    else:
        print("⚠️  Email not configured (optional)")
    
    return True


def test_directory_structure():
    """Test that required directories exist"""
    print("\n" + "=" * 60)
    print("🧪 TEST: Directory Structure")
    print("=" * 60)
    
    required_dirs = [
        'utils',
        'src',
        'tests',
        'output',
        'input',
    ]
    
    optional_dirs = [
        'cache',
        'logs',
        'output/batch_results',
        'output/metadata',
        'output/web_results',
    ]
    
    all_ok = True
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ (MISSING)")
            all_ok = False
    
    print("\nOptional directories:")
    for dir_path in optional_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"⚠️  {dir_path}/ (will be created when needed)")
    
    return all_ok


def test_required_files():
    """Test that required files exist"""
    print("\n" + "=" * 60)
    print("🧪 TEST: Required Files")
    print("=" * 60)
    
    required_files = [
        'requirements.txt',
        'README.md',
        'main_cloud.py',
        'process_book_enhanced.py',
        'batch_processor.py',
        'web_app.py',
        'utils/__init__.py',
        'utils/cloud_storage.py',
    ]
    
    all_ok = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} (MISSING)")
            all_ok = False
    
    return all_ok


def test_config_files():
    """Test configuration files"""
    print("\n" + "=" * 60)
    print("🧪 TEST: Configuration Files")
    print("=" * 60)
    
    config_files = [
        'cloud_env_template.txt',
        'config.example.env',
        'books_config.json',
    ]
    
    for file_path in config_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"⚠️  {file_path} (recommended)")
    
    return True


def main():
    """Run all integration tests"""
    print("\n" + "=" * 60)
    print("🔗 INTEGRATION TESTS")
    print("=" * 60)
    print()
    
    results = []
    
    try:
        results.append(("Module Imports", test_imports()))
        results.append(("Environment", test_environment()))
        results.append(("Directory Structure", test_directory_structure()))
        results.append(("Required Files", test_required_files()))
        results.append(("Config Files", test_config_files()))
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All integration tests passed!")
        print("\nYour environment is properly configured!")
        print("Anviwònman ou byen konfigure!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("\nSome issues need to be addressed.")
        print("Gen kèk pwoblèm ki bezwen rezoud.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()

