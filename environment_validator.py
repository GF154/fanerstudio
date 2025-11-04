#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Environment Validator for Faner Studio
Validate all required configurations and dependencies
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import importlib


class EnvironmentValidator:
    """Validate environment configuration"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
    
    def validate_all(self) -> Dict:
        """Run all validations"""
        self.check_python_version()
        self.check_required_packages()
        self.check_optional_packages()
        self.check_environment_variables()
        self.check_directories()
        self.check_tts_engines()
        
        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info
        }
    
    def check_python_version(self):
        """Check Python version"""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 9):
            self.errors.append(f"Python 3.9+ required, found {version.major}.{version.minor}")
        else:
            self.info.append(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    
    def check_required_packages(self):
        """Check required Python packages"""
        required = {
            "fastapi": "FastAPI web framework",
            "uvicorn": "ASGI server",
            "httpx": "HTTP client for API calls",
            "pydantic": "Data validation",
            "sqlalchemy": "Database ORM",
            "bcrypt": "Password hashing",
            "pydub": "Audio processing",
            "gtts": "Text-to-speech"
        }
        
        for package, description in required.items():
            try:
                importlib.import_module(package)
                self.info.append(f"✅ {package} ({description})")
            except ImportError:
                self.errors.append(f"❌ Missing required package: {package} - {description}")
    
    def check_optional_packages(self):
        """Check optional Python packages"""
        optional = {
            "librosa": "Advanced audio analysis",
            "parselmouth": "Pitch detection",
            "TTS": "Coqui TTS (high quality)",
            "elevenlabs": "ElevenLabs API",
            "redis": "Redis caching"
        }
        
        for package, description in optional.items():
            try:
                importlib.import_module(package)
                self.info.append(f"✅ {package} ({description}) - OPTIONAL")
            except ImportError:
                self.warnings.append(f"⚠️  Optional package not installed: {package} - {description}")
    
    def check_environment_variables(self):
        """Check environment variables"""
        # Required
        required_vars = {
            "DATABASE_URL": "Database connection string (default: SQLite)",
            "SECRET_KEY": "JWT secret key (default: generated)"
        }
        
        for var, description in required_vars.items():
            value = os.getenv(var)
            if value:
                masked = value[:10] + "..." if len(value) > 10 else value
                self.info.append(f"✅ {var} = {masked}")
            else:
                self.warnings.append(f"⚠️  {var} not set - {description}")
        
        # Optional API keys
        optional_vars = {
            "HUGGINGFACE_API_KEY": "Hugging Face API for translation",
            "OPENAI_API_KEY": "OpenAI TTS API",
            "ELEVENLABS_API_KEY": "ElevenLabs voice cloning",
            "SUPABASE_URL": "Supabase database URL",
            "SUPABASE_KEY": "Supabase API key"
        }
        
        for var, description in optional_vars.items():
            value = os.getenv(var)
            if value:
                masked = value[:10] + "..."
                self.info.append(f"✅ {var} = {masked} (OPTIONAL)")
            else:
                self.warnings.append(f"⚠️  {var} not set - {description} (optional)")
    
    def check_directories(self):
        """Check required directories"""
        dirs = [
            ("output", "Output directory for generated files"),
            ("custom_voices", "Custom voice storage"),
            ("audio_library", "Music and SFX library"),
            ("temp_uploads", "Temporary upload directory")
        ]
        
        for dir_name, description in dirs:
            dir_path = Path(dir_name)
            if dir_path.exists():
                self.info.append(f"✅ {dir_name}/ exists ({description})")
            else:
                self.warnings.append(f"⚠️  {dir_name}/ not found - {description} (will be created)")
    
    def check_tts_engines(self):
        """Check available TTS engines"""
        engines = []
        
        try:
            import gtts
            engines.append("gTTS (Google)")
        except ImportError:
            pass
        
        try:
            from TTS.api import TTS
            engines.append("Coqui TTS")
        except ImportError:
            pass
        
        try:
            import pyttsx3
            engines.append("pyttsx3 (Offline)")
        except ImportError:
            pass
        
        if engines:
            self.info.append(f"✅ TTS Engines: {', '.join(engines)}")
        else:
            self.errors.append("❌ No TTS engines available! Install gtts: pip install gtts")
    
    def print_report(self):
        """Print validation report"""
        print("\n" + "="*60)
        print("🔍 FANER STUDIO - Environment Validation Report")
        print("="*60 + "\n")
        
        if self.errors:
            print("❌ ERRORS (Must Fix):")
            for error in self.errors:
                print(f"   {error}")
            print()
        
        if self.warnings:
            print("⚠️  WARNINGS (Optional):")
            for warning in self.warnings:
                print(f"   {warning}")
            print()
        
        if self.info:
            print("ℹ️  INFO:")
            for info in self.info:
                print(f"   {info}")
            print()
        
        print("="*60)
        if len(self.errors) == 0:
            print("✅ Environment is VALID - Ready to deploy!")
        else:
            print(f"❌ Environment has {len(self.errors)} error(s) - Fix before deploying")
        print("="*60 + "\n")


def validate_environment() -> bool:
    """
    Validate environment and return True if valid
    
    Returns:
        True if environment is valid, False otherwise
    """
    validator = EnvironmentValidator()
    result = validator.validate_all()
    validator.print_report()
    
    return result["valid"]


def check_deployment_readiness() -> Dict:
    """
    Check if platform is ready for deployment
    
    Returns:
        Dictionary with readiness status
    """
    validator = EnvironmentValidator()
    result = validator.validate_all()
    
    # Additional deployment checks
    deployment_checks = {
        "environment_valid": len(result["errors"]) == 0,
        "tts_available": any("TTS" in info for info in result["info"]),
        "database_configured": any("DATABASE_URL" in info for info in result["info"]),
        "audio_processing": any("pydub" in info for info in result["info"]),
        "has_warnings": len(result["warnings"]) > 0
    }
    
    deployment_checks["ready"] = all([
        deployment_checks["environment_valid"],
        deployment_checks["tts_available"],
        deployment_checks["audio_processing"]
    ])
    
    return {
        "ready": deployment_checks["ready"],
        "checks": deployment_checks,
        "errors": result["errors"],
        "warnings": result["warnings"]
    }


if __name__ == "__main__":
    # Run validation
    is_valid = validate_environment()
    
    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)

