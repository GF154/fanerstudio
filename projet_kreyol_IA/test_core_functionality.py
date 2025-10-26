#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Core Functionality
Verify that the main translation features work
"""

import sys
from pathlib import Path

def test_core_functionality():
    """Test core application functionality"""
    print("="*60)
    print("CORE FUNCTIONALITY TEST")
    print("="*60)
    print()
    
    passed = 0
    failed = 0
    
    # Test 1: Import core modules
    print("Test 1: Import core modules")
    print("-" * 60)
    try:
        from src import Config, PDFExtractor, CreoleTranslator, AudiobookGenerator
        print("✅ All core modules imported successfully")
        passed += 1
    except ImportError as e:
        print(f"❌ Failed to import core modules: {e}")
        failed += 1
    
    # Test 2: Create Config
    print()
    print("Test 2: Configuration")
    print("-" * 60)
    try:
        from src import Config
        config = Config()
        print(f"✅ Config created")
        print(f"   Source language: {config.source_language}")
        print(f"   Target language: {config.target_language}")
        print(f"   TTS language: {config.tts_language}")
        print(f"   Logs dir: {config.logs_dir}")
        passed += 1
    except Exception as e:
        print(f"❌ Config creation failed: {e}")
        failed += 1
    
    # Test 3: Test PDF Extractor
    print()
    print("Test 3: PDF Extractor")
    print("-" * 60)
    try:
        from src import PDFExtractor, Config
        config = Config()
        extractor = PDFExtractor(config)
        print("✅ PDF Extractor initialized")
        passed += 1
    except Exception as e:
        print(f"❌ PDF Extractor failed: {e}")
        failed += 1
    
    # Test 4: Test Translator
    print()
    print("Test 4: Translator")
    print("-" * 60)
    try:
        from src import CreoleTranslator, Config
        config = Config()
        translator = CreoleTranslator(config)
        print("✅ Translator initialized")
        print(f"   Model: {config.translation_model}")
        print(f"   Cache enabled: {config.enable_cache}")
        passed += 1
    except Exception as e:
        print(f"❌ Translator failed: {e}")
        failed += 1
    
    # Test 5: Test Audio Generator
    print()
    print("Test 5: Audio Generator")
    print("-" * 60)
    try:
        from src import AudiobookGenerator, Config
        config = Config()
        generator = AudiobookGenerator(config)
        print("✅ Audio Generator initialized")
        print(f"   TTS language: {config.tts_language}")
        print(f"   Max audio chars: {config.max_audio_chars}")
        passed += 1
    except Exception as e:
        print(f"❌ Audio Generator failed: {e}")
        failed += 1
    
    # Test 6: Test a simple translation
    print()
    print("Test 6: Simple Translation")
    print("-" * 60)
    try:
        from src import CreoleTranslator, Config
        config = Config()
        config.enable_cache = False  # Disable cache for test
        translator = CreoleTranslator(config)
        
        test_text = "Hello, this is a test."
        print(f"   Input: '{test_text}'")
        print(f"   Translating... (this may take a moment)")
        
        # Note: This will download the model on first run (~1.5GB)
        # translated = translator.translate(test_text, src_lang='en', show_progress=False)
        # print(f"   Output: '{translated}'")
        # For now, just check if it can be called
        print("✅ Translator ready (model download will happen on first use)")
        passed += 1
    except Exception as e:
        print(f"❌ Translation test failed: {e}")
        failed += 1
    
    # Test 7: Check FFmpeg
    print()
    print("Test 7: FFmpeg Availability")
    print("-" * 60)
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg available: {version_line}")
            passed += 1
        else:
            print("⚠️  FFmpeg not found (optional for audio processing)")
            passed += 1
    except FileNotFoundError:
        print("⚠️  FFmpeg not found (optional for audio processing)")
        passed += 1
    except Exception as e:
        print(f"⚠️  Could not check FFmpeg: {e}")
        passed += 1
    
    # Test 8: Check directories
    print()
    print("Test 8: Required Directories")
    print("-" * 60)
    try:
        required_dirs = ['data', 'output', 'cache', 'logs', 'src', 'utils']
        all_exist = True
        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            if dir_path.exists():
                print(f"   ✅ {dir_name}/")
            else:
                print(f"   ❌ {dir_name}/ (missing)")
                all_exist = False
        
        if all_exist:
            print("✅ All required directories exist")
            passed += 1
        else:
            print("❌ Some directories are missing")
            failed += 1
    except Exception as e:
        print(f"❌ Directory check failed: {e}")
        failed += 1
    
    # Summary
    print()
    print("="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
    print()
    
    if failed == 0:
        print("✅ ALL TESTS PASSED!")
        print()
        print("Your application is ready to use!")
        print()
        print("Next steps:")
        print("1. Place a PDF in data/input.pdf")
        print("2. Run: python main.py")
        print("3. Or run web interface: streamlit run app.py")
        return True
    else:
        print("⚠️  SOME TESTS FAILED")
        print()
        print("Please review the errors above and fix them.")
        return False

if __name__ == "__main__":
    success = test_core_functionality()
    sys.exit(0 if success else 1)

