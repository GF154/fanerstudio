#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Code Fixes
Verify that all code fixes were applied correctly
"""

def test_fixes():
    print("="*60)
    print("TEST CODE FIXES")
    print("="*60)
    print()
    
    all_passed = True
    
    # Test 1: Check requirements.txt
    print("Test 1: requirements.txt fixes")
    print("-" * 60)
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'torch==2.5.1' in content:
            print("✅ PyTorch version fixed (2.5.1)")
        else:
            print("❌ PyTorch version not fixed")
            all_passed = False
        
        if 'pydub==0.25.1' in content:
            print("✅ Pydub added")
        else:
            print("❌ Pydub not added")
            all_passed = False
        
        if 'google-cloud-storage==2.18.2' in content:
            print("✅ Google Cloud Storage version pinned")
        else:
            print("❌ Google Cloud Storage version not pinned")
            all_passed = False
        
        if 'boto3==1.35.73' in content:
            print("✅ Boto3 version pinned")
        else:
            print("❌ Boto3 version not pinned")
            all_passed = False
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        all_passed = False
    
    # Test 2: Check api.py fixes
    print()
    print("Test 2: api.py fixes")
    print("-" * 60)
    try:
        with open('api.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'config.logs_dir' in content and 'config.LOG_DIR' not in content:
            print("✅ config.logs_dir fixed")
        else:
            print("❌ config.logs_dir not fixed")
            all_passed = False
        
        if 'generator.config.tts_language' in content:
            print("✅ generator.config.tts_language fixed")
        else:
            print("❌ generator.config.tts_language not fixed")
            all_passed = False
        
        if 'generator.config.tts_slow' in content:
            print("✅ generator.config.tts_slow fixed")
        else:
            print("❌ generator.config.tts_slow not fixed")
            all_passed = False
    except Exception as e:
        print(f"❌ Error reading api.py: {e}")
        all_passed = False
    
    # Test 3: Check audio_generator.py fixes
    print()
    print("Test 3: src/audio_generator.py fixes")
    print("-" * 60)
    try:
        with open('src/audio_generator.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'from typing import Optional, List' in content:
            print("✅ List import added")
        else:
            print("❌ List import not added")
            all_passed = False
        
        if '-> List[Path]:' in content:
            print("✅ Type hint fixed (List[Path])")
        else:
            print("❌ Type hint not fixed")
            all_passed = False
    except Exception as e:
        print(f"❌ Error reading src/audio_generator.py: {e}")
        all_passed = False
    
    # Test 4: Check .env file
    print()
    print("Test 4: .env file")
    print("-" * 60)
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
        print("✅ .env file exists")
        
        if 'TARGET_LANGUAGE=ht' in content:
            print("✅ .env configured for Haitian Creole")
    except FileNotFoundError:
        print("⚠️  .env file not found (will be created during installation)")
        # Don't fail for missing .env - it's optional
        # all_passed = False
    except Exception as e:
        print(f"❌ Error reading .env: {e}")
        all_passed = False
    
    # Summary
    print()
    print("="*60)
    if all_passed:
        print("✅ ALL FIXES APPLIED SUCCESSFULLY!")
        print()
        print("Next steps:")
        print("1. Run: pip install -r requirements.txt")
        print("2. Run: python test_quick.py")
        return True
    else:
        print("⚠️  SOME FIXES FAILED")
        print("Please review the errors above")
        return False

if __name__ == "__main__":
    import sys
    success = test_fixes()
    sys.exit(0 if success else 1)

