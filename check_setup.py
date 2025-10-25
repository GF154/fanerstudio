#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup Checker - Verifye si tout bagay byen konfigure
Check if everything is properly configured
"""

import os
import sys
from pathlib import Path


def check_python_version():
    """Check Python version"""
    print("=" * 60)
    print("🐍 Python Version")
    print("=" * 60)
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version OK (>= 3.8)")
        return True
    else:
        print("❌ Python version too old (need >= 3.8)")
        return False


def check_required_packages():
    """Check if required packages are installed"""
    print("\n" + "=" * 60)
    print("📦 Required Packages")
    print("=" * 60)
    
    packages = [
        'google.cloud.storage',
        'boto3',
        'pypdf',
        'transformers',
        'torch',
        'gtts',
        'streamlit',
        'fastapi',
    ]
    
    missing = []
    
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (MISSING)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  {len(missing)} package(s) missing")
        print("\nInstall with:")
        print("pip install -r requirements.txt")
        return False
    else:
        print(f"\n✅ All {len(packages)} packages installed")
        return True


def check_environment_variables():
    """Check environment variables"""
    print("\n" + "=" * 60)
    print("⚙️  Environment Variables")
    print("=" * 60)
    
    # Required
    bucket = os.getenv("GCS_BUCKET_NAME")
    if bucket:
        print(f"✅ GCS_BUCKET_NAME: {bucket}")
        required_ok = True
    else:
        print("❌ GCS_BUCKET_NAME: NOT SET (REQUIRED)")
        required_ok = False
    
    # Optional but recommended
    gcs_creds = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if gcs_creds:
        print(f"✅ GOOGLE_APPLICATION_CREDENTIALS: {gcs_creds}")
    else:
        print("⚠️  GOOGLE_APPLICATION_CREDENTIALS: Not set")
        print("   (Using application default credentials)")
    
    # Email (optional)
    sender = os.getenv("SENDER_EMAIL")
    if sender:
        print(f"✅ SENDER_EMAIL: {sender}")
    else:
        print("⚠️  SENDER_EMAIL: Not set (email notifications disabled)")
    
    return required_ok


def check_directory_structure():
    """Check directory structure"""
    print("\n" + "=" * 60)
    print("📁 Directory Structure")
    print("=" * 60)
    
    required_dirs = ['utils', 'src', 'tests']
    auto_create_dirs = ['input', 'output', 'cache', 'logs']
    
    all_ok = True
    
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ (MISSING - CRITICAL)")
            all_ok = False
    
    for dir_name in auto_create_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✅ {dir_name}/")
        else:
            print(f"⚠️  {dir_name}/ (will be created automatically)")
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"   → Created {dir_name}/")
            except Exception as e:
                print(f"   → Failed to create: {e}")
    
    return all_ok


def check_config_files():
    """Check configuration files"""
    print("\n" + "=" * 60)
    print("📄 Configuration Files")
    print("=" * 60)
    
    if Path(".env").exists():
        print("✅ .env (configuration file)")
    else:
        print("⚠️  .env not found")
        if Path("cloud_env_template.txt").exists():
            print("   → Copy cloud_env_template.txt to .env")
            print("   → cp cloud_env_template.txt .env")
        elif Path("config.example.env").exists():
            print("   → Copy config.example.env to .env")
            print("   → cp config.example.env .env")
    
    required_files = [
        'requirements.txt',
        'main_cloud.py',
        'process_book_enhanced.py',
        'batch_processor.py',
        'web_app.py',
    ]
    
    all_ok = True
    
    for file_name in required_files:
        if Path(file_name).exists():
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} (MISSING)")
            all_ok = False
    
    return all_ok


def check_gcs_connection():
    """Check GCS connection"""
    print("\n" + "=" * 60)
    print("☁️  Google Cloud Storage Connection")
    print("=" * 60)
    
    bucket = os.getenv("GCS_BUCKET_NAME")
    
    if not bucket:
        print("⚠️  Cannot test - GCS_BUCKET_NAME not set")
        return False
    
    try:
        from google.cloud import storage
        
        print("Attempting to connect to GCS...")
        client = storage.Client()
        bucket_obj = client.bucket(bucket)
        
        # Try to check if bucket exists
        if bucket_obj.exists():
            print(f"✅ Connected to bucket: {bucket}")
            return True
        else:
            print(f"❌ Bucket not found: {bucket}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nTo authenticate:")
        print("gcloud auth application-default login")
        return False


def print_next_steps(all_checks):
    """Print next steps based on check results"""
    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS / PWOCHEN ETAP")
    print("=" * 60)
    
    if all(all_checks.values()):
        print("\n✅ Everything is configured correctly!")
        print("   Tout bagay byen konfigure!")
        print("\nYou can now:")
        print("1. Run the web interface:")
        print("   streamlit run web_app.py")
        print("\n2. Or use the interactive menu:")
        print("   python start_here.py")
        print("\n3. Or process a book directly:")
        print("   python process_book_enhanced.py")
        
    else:
        print("\n⚠️  Some issues need to be fixed:")
        
        if not all_checks['packages']:
            print("\n1. Install packages:")
            print("   pip install -r requirements.txt")
        
        if not all_checks['environment']:
            print("\n2. Configure environment:")
            print("   cp cloud_env_template.txt .env")
            print("   nano .env  # Edit and set GCS_BUCKET_NAME")
        
        if not all_checks['gcs']:
            print("\n3. Authenticate with GCS:")
            print("   gcloud auth application-default login")
        
        print("\n4. Run this checker again:")
        print("   python check_setup.py")


def main():
    """Run all checks"""
    print("\n" + "=" * 60)
    print("🔍 SETUP CHECKER")
    print("   Verifikasyon Konfigirasyon")
    print("=" * 60)
    
    checks = {}
    
    checks['python'] = check_python_version()
    checks['packages'] = check_required_packages()
    checks['environment'] = check_environment_variables()
    checks['directories'] = check_directory_structure()
    checks['files'] = check_config_files()
    checks['gcs'] = check_gcs_connection()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY / REZIME")
    print("=" * 60)
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    for name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {name.capitalize()}")
    
    print(f"\nScore: {passed}/{total} checks passed")
    
    # Next steps
    print_next_steps(checks)
    
    print("\n" + "=" * 60)
    
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())

