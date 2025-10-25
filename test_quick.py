#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Installation Test
Tests all core dependencies
"""

def quick_test():
    print("="*60)
    print("QUICK INSTALLATION TEST")
    print("="*60)
    print()
    
    tests = [
        ('torch', 'PyTorch'),
        ('transformers', 'Transformers'),
        ('streamlit', 'Streamlit'),
        ('fastapi', 'FastAPI'),
        ('gtts', 'gTTS'),
        ('pydub', 'Pydub'),
        ('pypdf', 'PyPDF'),
        ('langdetect', 'LangDetect'),
        ('deep_translator', 'Deep Translator'),
        ('tqdm', 'TQDM'),
        ('dotenv', 'Python-dotenv'),
        ('requests', 'Requests'),
    ]
    
    passed = 0
    failed = 0
    
    for module, name in tests:
        try:
            mod = __import__(module)
            version = getattr(mod, '__version__', 'unknown')
            print(f"✅ {name:20} {version}")
            passed += 1
        except ImportError:
            print(f"❌ {name:20} NOT INSTALLED")
            failed += 1
    
    print()
    print("="*60)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60)
    
    if failed == 0:
        print("✅ All core dependencies installed!")
        print()
        print("Next steps:")
        print("1. Install FFmpeg: choco install ffmpeg")
        print("2. Run: python check_setup.py")
        print("3. Test app: streamlit run app.py")
        return True
    else:
        print("⚠️  Some dependencies missing")
        print()
        print("To install missing dependencies:")
        print("  pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    import sys
    success = quick_test()
    sys.exit(0 if success else 1)

