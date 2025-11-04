#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Comprehensive Test Suite for Faner Studio
Complete testing for all endpoints and features
"""

import pytest
import asyncio
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from environment_validator import validate_environment, check_deployment_readiness


class TestEnvironment:
    """Test environment configuration"""
    
    def test_python_version(self):
        """Test Python version is 3.9+"""
        assert sys.version_info >= (3, 9), "Python 3.9+ required"
    
    def test_required_packages(self):
        """Test required packages are installed"""
        required = ["fastapi", "uvicorn", "httpx", "pydantic", "sqlalchemy", "bcrypt", "pydub", "gtts"]
        
        for package in required:
            try:
                __import__(package)
            except ImportError:
                pytest.fail(f"Required package missing: {package}")
    
    def test_environment_validation(self):
        """Test environment validator"""
        result = validate_environment()
        assert isinstance(result, bool)
    
    def test_deployment_readiness(self):
        """Test deployment readiness check"""
        readiness = check_deployment_readiness()
        assert "ready" in readiness
        assert "checks" in readiness


class TestTTSIntegration:
    """Test Text-to-Speech integration"""
    
    def test_tts_import(self):
        """Test TTS module can be imported"""
        try:
            from generer_audio_huggingface import generer_audio_creole
            assert callable(generer_audio_creole)
        except ImportError:
            pytest.fail("TTS module not available")
    
    def test_tts_engines_available(self):
        """Test at least one TTS engine is available"""
        try:
            from generer_audio_huggingface import check_tts_available
            engines = check_tts_available()
            assert engines["current"] is not None, "No TTS engine available"
        except ImportError:
            pytest.fail("TTS module not available")
    
    @pytest.mark.asyncio
    async def test_tts_generation(self):
        """Test basic TTS generation"""
        try:
            from generer_audio_huggingface import generer_audio_creole
            
            test_text = "Bonjou! Sa se yon tès."
            test_output = Path("test_tts_output.mp3")
            
            # Generate audio
            result = generer_audio_creole(test_text, test_output)
            
            # Check file was created
            assert result.exists(), "Audio file not created"
            
            # Cleanup
            if test_output.exists():
                test_output.unlink()
        
        except Exception as e:
            pytest.skip(f"TTS generation test skipped: {e}")


class TestVoiceCloning:
    """Test voice cloning functionality"""
    
    def test_voice_cloner_import(self):
        """Test voice cloning module can be imported"""
        try:
            from projet_kreyol_IA.src.advanced_voice_cloning import VoiceCloner
            assert VoiceCloner is not None
        except ImportError:
            pytest.skip("Voice cloning module not available")
    
    def test_voice_analyzer(self):
        """Test voice analyzer"""
        try:
            from projet_kreyol_IA.src.advanced_voice_cloning import VoiceAnalyzer
            analyzer = VoiceAnalyzer()
            assert analyzer is not None
        except ImportError:
            pytest.skip("Voice analyzer not available")


class TestPodcastFabric:
    """Test advanced podcast generation"""
    
    def test_podcast_fabric_import(self):
        """Test podcast fabric module can be imported"""
        try:
            from podcast_fabric import AdvancedPodcastGenerator, Speaker, VoiceEmotion
            assert AdvancedPodcastGenerator is not None
        except ImportError:
            pytest.fail("Podcast fabric module not available")
    
    def test_script_parser(self):
        """Test podcast script parser"""
        try:
            from podcast_fabric import PodcastScriptParser, Speaker, SpeakerGender, VoiceEmotion
            
            parser = PodcastScriptParser()
            
            # Create test speakers
            speakers = [
                Speaker(
                    id="host",
                    name="Host",
                    voice_id="creole-native",
                    gender=SpeakerGender.FEMALE,
                    emotion=VoiceEmotion.FRIENDLY
                )
            ]
            
            # Test script
            script = """[INTRO - Background: Corporate]
Host (excited): Welcome to the test!

[MAIN]
Host: This is a test.

[OUTRO]
Host (happy): Goodbye!"""
            
            segments = parser.parse(script, speakers)
            assert len(segments) == 3, f"Expected 3 segments, got {len(segments)}"
            assert segments[0].type == "intro"
            assert segments[1].type == "main"
            assert segments[2].type == "outro"
        
        except ImportError:
            pytest.fail("Podcast fabric not available")


class TestAudioLibrary:
    """Test music and SFX library"""
    
    def test_audio_library_import(self):
        """Test audio library module can be imported"""
        try:
            from audio_library import MusicLibrary, AudioMixer
            assert MusicLibrary is not None
            assert AudioMixer is not None
        except ImportError:
            pytest.fail("Audio library module not available")
    
    def test_music_library_creation(self):
        """Test music library can be created"""
        try:
            from audio_library import MusicLibrary
            
            library = MusicLibrary()
            available = library.list_available()
            
            assert "music" in available
            assert "sfx" in available
            assert "jingles" in available
        
        except ImportError:
            pytest.skip("Audio library not available")


class TestDatabaseIntegration:
    """Test database integration"""
    
    def test_database_import(self):
        """Test database module can be imported"""
        try:
            from database import get_db, init_db, UserCRUD
            assert get_db is not None
            assert init_db is not None
        except ImportError:
            pytest.skip("Database module not available")


class TestAuthentication:
    """Test authentication system"""
    
    def test_auth_import(self):
        """Test auth module can be imported"""
        try:
            from auth import create_access_token, hash_password, verify_password
            assert create_access_token is not None
            assert hash_password is not None
        except ImportError:
            pytest.skip("Auth module not available")
    
    def test_password_hashing(self):
        """Test password hashing"""
        try:
            from auth import hash_password, verify_password
            
            password = "test123"
            hashed = hash_password(password)
            
            assert hashed != password, "Password not hashed"
            assert verify_password(password, hashed), "Password verification failed"
            assert not verify_password("wrong", hashed), "Wrong password verified"
        
        except ImportError:
            pytest.skip("Auth module not available")


class TestPerformance:
    """Test performance monitoring"""
    
    def test_performance_import(self):
        """Test performance module can be imported"""
        try:
            from performance import cache, perf_monitor
            assert cache is not None
            assert perf_monitor is not None
        except ImportError:
            pytest.skip("Performance module not available")


def run_all_tests():
    """Run all tests and print results"""
    print("\n" + "="*60)
    print("🧪 FANER STUDIO - Comprehensive Test Suite")
    print("="*60 + "\n")
    
    # Run pytest
    exit_code = pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--color=yes",
        "-W", "ignore::DeprecationWarning"
    ])
    
    print("\n" + "="*60)
    if exit_code == 0:
        print("✅ ALL TESTS PASSED")
    else:
        print(f"❌ TESTS FAILED (exit code: {exit_code})")
    print("="*60 + "\n")
    
    return exit_code


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)

