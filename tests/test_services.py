#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Tests for Services
Test pou TTS, STT, Media Services
"""

import pytest
import asyncio
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.tts_service import TTSService
from app.services.stt_service import STTService
from app.services.media_service import MediaService


class TestTTSService:
    """Tests pou TTS Service"""
    
    @pytest.fixture
    def tts_service(self):
        """Create TTS service instance"""
        return TTSService()
    
    def test_initialization(self, tts_service):
        """Test TTS service initializes correctly"""
        assert tts_service is not None
        assert tts_service.output_dir.exists()
    
    def test_get_available_voices(self, tts_service):
        """Test getting available voices"""
        voices = tts_service.get_available_voices()
        assert isinstance(voices, list)
        assert len(voices) > 0
        assert any(v['id'] == 'creole-native' for v in voices)
    
    @pytest.mark.asyncio
    async def test_generate_speech_short_text(self, tts_service):
        """Test generating speech from short text"""
        test_text = "Bonjou, sa se yon tès."
        
        try:
            audio_path = await tts_service.generate_speech(test_text, "gtts")
            assert audio_path.exists()
            assert audio_path.suffix == ".mp3"
            
            # Cleanup
            if audio_path.exists():
                audio_path.unlink()
                
        except Exception as e:
            pytest.skip(f"TTS not available: {e}")


class TestSTTService:
    """Tests pou STT Service"""
    
    @pytest.fixture
    def stt_service(self):
        """Create STT service instance"""
        return STTService()
    
    def test_initialization(self, stt_service):
        """Test STT service initializes correctly"""
        assert stt_service is not None
    
    def test_get_available_engines(self, stt_service):
        """Test getting available STT engines"""
        engines = stt_service.get_available_engines()
        assert isinstance(engines, list)
    
    def test_get_supported_formats(self, stt_service):
        """Test getting supported audio formats"""
        formats = stt_service.get_supported_formats()
        assert isinstance(formats, list)
        assert ".mp3" in formats
        assert ".wav" in formats


class TestMediaService:
    """Tests pou Media Service"""
    
    @pytest.fixture
    def media_service(self):
        """Create Media service instance"""
        return MediaService()
    
    def test_initialization(self, media_service):
        """Test Media service initializes correctly"""
        assert media_service is not None
        assert media_service.output_dir.exists()
    
    @pytest.mark.asyncio
    async def test_extract_text_from_txt(self, media_service, tmp_path):
        """Test extracting text from TXT file"""
        # Create a test TXT file
        test_file = tmp_path / "test.txt"
        test_content = "This is a test document.\nWith multiple lines."
        test_file.write_text(test_content, encoding='utf-8')
        
        # Extract text
        extracted = await media_service.extract_text_from_document(str(test_file))
        
        assert extracted == test_content
    
    @pytest.mark.asyncio
    async def test_extract_text_invalid_format(self, media_service, tmp_path):
        """Test extracting text from unsupported format"""
        test_file = tmp_path / "test.xyz"
        test_file.write_text("content")
        
        with pytest.raises(ValueError):
            await media_service.extract_text_from_document(str(test_file))
    
    def test_split_for_speakers(self, media_service):
        """Test splitting text for multiple speakers"""
        text = "First sentence. Second sentence. Third sentence. Fourth sentence."
        segments = media_service._split_for_speakers(text, 2)
        
        assert isinstance(segments, list)
        assert len(segments) >= 2
        assert all('speaker' in seg and 'text' in seg for seg in segments)


class TestCache:
    """Tests pou Cache System"""
    
    def test_cache_import(self):
        """Test cache module can be imported"""
        from app.cache import SimpleCache, translation_cache, audio_cache
        
        assert SimpleCache is not None
        assert translation_cache is not None
        assert audio_cache is not None
    
    def test_cache_set_get(self):
        """Test basic cache set/get operations"""
        from app.cache import SimpleCache
        
        cache = SimpleCache("cache/test", ttl_hours=1)
        
        # Set value
        success = cache.set("test_key", "test_value")
        assert success is True
        
        # Get value
        value = cache.get("test_key")
        assert value == "test_value"
        
        # Cleanup
        cache.clear()
    
    def test_cache_miss(self):
        """Test cache miss returns None"""
        from app.cache import SimpleCache
        
        cache = SimpleCache("cache/test", ttl_hours=1)
        value = cache.get("nonexistent_key")
        assert value is None
    
    def test_cache_stats(self):
        """Test cache statistics"""
        from app.cache import SimpleCache
        
        cache = SimpleCache("cache/test", ttl_hours=1)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        
        stats = cache.get_stats()
        assert isinstance(stats, dict)
        assert "total_entries" in stats
        assert stats["total_entries"] >= 2
        
        # Cleanup
        cache.clear()


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

