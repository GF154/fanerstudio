#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Test Script - Validate All Platform Features
Skrip Tès - Valide Tout Fonksyonalite Platfòm La
"""

import sys
import os

def test_imports():
    """Test all module imports"""
    print("\n" + "="*60)
    print("🧪 TESTING MODULE IMPORTS")
    print("="*60)
    
    modules = [
        ("pdf_processor", "DocumentProcessor"),
        ("tts_engine", "TTSEngine"),
        ("podcast_generator", "PodcastGenerator"),
        ("video_processor_simple", "VideoProcessor"),
        ("custom_voice_cloner", "CustomVoiceCloner"),
        ("database", "UserDB")
    ]
    
    results = {}
    
    for module_name, class_name in modules:
        try:
            module = __import__(module_name)
            cls = getattr(module, class_name)
            results[module_name] = "✅ PASS"
            print(f"✅ {module_name}.{class_name} - OK")
        except ImportError as e:
            results[module_name] = f"❌ FAIL - {str(e)}"
            print(f"❌ {module_name}.{class_name} - FAIL: {str(e)}")
        except Exception as e:
            results[module_name] = f"⚠️ ERROR - {str(e)}"
            print(f"⚠️ {module_name}.{class_name} - ERROR: {str(e)}")
    
    return results


def test_dependencies():
    """Test required dependencies"""
    print("\n" + "="*60)
    print("📦 TESTING DEPENDENCIES")
    print("="*60)
    
    dependencies = [
        "fastapi",
        "uvicorn",
        "gtts",
        "pydub",
        "PyPDF2",
        "python-docx",
        "ebooklib",
        "beautifulsoup4",
        "pyttsx3",
        "python-multipart",
        "supabase",
        "python-dotenv"
    ]
    
    results = {}
    
    for dep in dependencies:
        # Map package names to import names
        import_name = dep
        if dep == "python-docx":
            import_name = "docx"
        elif dep == "beautifulsoup4":
            import_name = "bs4"
        elif dep == "python-multipart":
            import_name = "multipart"
        elif dep == "python-dotenv":
            import_name = "dotenv"
        
        try:
            __import__(import_name)
            results[dep] = "✅ INSTALLED"
            print(f"✅ {dep} - INSTALLED")
        except ImportError:
            results[dep] = "❌ MISSING"
            print(f"❌ {dep} - MISSING (pip install {dep})")
    
    return results


def test_environment():
    """Test environment variables"""
    print("\n" + "="*60)
    print("🔐 TESTING ENVIRONMENT VARIABLES")
    print("="*60)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        dotenv_available = True
    except:
        dotenv_available = False
        print("⚠️ python-dotenv not available")
    
    env_vars = [
        "SUPABASE_URL",
        "SUPABASE_KEY"
    ]
    
    results = {}
    
    for var in env_vars:
        value = os.getenv(var)
        if value and value != f"your-{var.lower().replace('_', '-')}-here":
            results[var] = "✅ SET"
            print(f"✅ {var} - SET")
        else:
            results[var] = "❌ NOT SET"
            print(f"❌ {var} - NOT SET (check .env file)")
    
    return results


def test_system_tools():
    """Test system tools (FFmpeg, etc.)"""
    print("\n" + "="*60)
    print("🔧 TESTING SYSTEM TOOLS")
    print("="*60)
    
    import subprocess
    
    tools = [
        ("ffmpeg", ["ffmpeg", "-version"]),
        ("ffprobe", ["ffprobe", "-version"])
    ]
    
    results = {}
    
    for tool_name, command in tools:
        try:
            subprocess.run(command, capture_output=True, check=True)
            results[tool_name] = "✅ INSTALLED"
            print(f"✅ {tool_name} - INSTALLED")
        except (subprocess.CalledProcessError, FileNotFoundError):
            results[tool_name] = "❌ NOT INSTALLED"
            print(f"❌ {tool_name} - NOT INSTALLED")
    
    return results


def test_file_structure():
    """Test file structure"""
    print("\n" + "="*60)
    print("📁 TESTING FILE STRUCTURE")
    print("="*60)
    
    required_files = [
        "api/index.py",
        "pdf_processor.py",
        "tts_engine.py",
        "podcast_generator.py",
        "video_processor_simple.py",
        "custom_voice_cloner.py",
        "database.py",
        "requirements.txt",
        "vercel.json",
        ".env.example",
        "public/index.html",
        "public/audiobook.html",
        "public/podcast.html",
        "public/video.html",
        "public/custom-voice.html"
    ]
    
    results = {}
    
    for file_path in required_files:
        if os.path.exists(file_path):
            results[file_path] = "✅ EXISTS"
            print(f"✅ {file_path} - EXISTS")
        else:
            results[file_path] = "❌ MISSING"
            print(f"❌ {file_path} - MISSING")
    
    return results


def generate_report(all_results):
    """Generate final test report"""
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    total_tests = 0
    total_passed = 0
    
    for category, results in all_results.items():
        passed = sum(1 for v in results.values() if "✅" in str(v))
        total = len(results)
        total_tests += total
        total_passed += passed
        
        status = "✅ PASS" if passed == total else "❌ FAIL"
        print(f"\n{category}: {passed}/{total} {status}")
    
    print("\n" + "="*60)
    print(f"OVERALL: {total_passed}/{total_tests} tests passed")
    print("="*60)
    
    if total_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED! Platform is ready!")
        return 0
    else:
        print("\n⚠️ SOME TESTS FAILED! Review errors above.")
        return 1


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print(" 🇭🇹 FANER STUDIO - PLATFORM TEST SUITE")
    print("="*80)
    
    all_results = {
        "Module Imports": test_imports(),
        "Dependencies": test_dependencies(),
        "Environment Variables": test_environment(),
        "System Tools": test_system_tools(),
        "File Structure": test_file_structure()
    }
    
    exit_code = generate_report(all_results)
    
    print("\n💡 Next Steps:")
    print("1. Fix any missing dependencies: pip install -r requirements.txt")
    print("2. Configure environment variables in .env file")
    print("3. Install system tools (FFmpeg) if needed")
    print("4. Deploy to Vercel: vercel --prod")
    print("5. Test live at: https://your-app.vercel.app")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

