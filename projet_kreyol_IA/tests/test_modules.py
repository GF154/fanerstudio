#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pour modules / Tests for modules
"""

import pytest
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import Config
from src.utils import smart_chunk_text, format_file_size, truncate_text
from src.translator import TranslationCache


class TestUtils:
    """Test utility functions"""
    
    def test_smart_chunk_short_text(self):
        """Test chunking with short text"""
        text = "Short text."
        chunks = smart_chunk_text(text, max_size=100)
        assert len(chunks) == 1
        assert chunks[0] == text
    
    def test_smart_chunk_long_text(self):
        """Test chunking with long text"""
        text = "Word " * 500
        chunks = smart_chunk_text(text, max_size=100)
        assert len(chunks) > 1
        for chunk in chunks:
            # Allow some overflow
            assert len(chunk) <= 150
    
    def test_format_file_size(self):
        """Test file size formatting"""
        assert "1.0KB" in format_file_size(1024)
        assert "1.0MB" in format_file_size(1024 * 1024)
        assert "B" in format_file_size(500)
    
    def test_truncate_text(self):
        """Test text truncation"""
        text = "This is a long text that should be truncated"
        truncated = truncate_text(text, max_length=20)
        assert len(truncated) <= 20
        assert truncated.endswith("...")
    
    def test_truncate_short_text(self):
        """Test truncation of short text"""
        text = "Short"
        truncated = truncate_text(text, max_length=20)
        assert truncated == text


class TestTranslationCache:
    """Test translation cache"""
    
    def test_cache_init(self):
        """Test cache initialization"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = TranslationCache(Path(tmpdir))
            assert cache.cache_dir.exists()
            assert cache.hits == 0
            assert cache.misses == 0
    
    def test_cache_set_and_get(self):
        """Test cache set and get"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = TranslationCache(Path(tmpdir))
            
            # Set cache
            cache.set("Hello", "Bonjou", "en", "ht")
            
            # Get cache
            result = cache.get("Hello", "en", "ht")
            assert result == "Bonjou"
            assert cache.hits == 1
            assert cache.misses == 0
    
    def test_cache_miss(self):
        """Test cache miss"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = TranslationCache(Path(tmpdir))
            
            result = cache.get("NonExistent", "en", "ht")
            assert result is None
            assert cache.misses == 1
    
    def test_cache_stats(self):
        """Test cache statistics"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = TranslationCache(Path(tmpdir))
            
            # Add some entries
            cache.set("Hello", "Bonjou", "en", "ht")
            cache.set("World", "Mond", "en", "ht")
            
            # Get stats
            stats = cache.get_stats()
            assert stats['files'] == 2
            assert stats['size_mb'] >= 0
            assert 'hit_rate' in stats
    
    def test_cache_clear(self):
        """Test cache clearing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = TranslationCache(Path(tmpdir))
            
            # Add entries
            cache.set("Hello", "Bonjou", "en", "ht")
            cache.set("World", "Mond", "en", "ht")
            
            # Clear cache
            count = cache.clear()
            assert count == 2
            
            # Verify cache is empty
            stats = cache.get_stats()
            assert stats['files'] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

