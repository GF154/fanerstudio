#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pour Config / Tests for Configuration
"""

import pytest
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import Config


class TestConfig:
    """Test configuration module"""
    
    def test_config_defaults(self):
        """Test default configuration values"""
        config = Config()
        
        assert config.data_dir == Path("data")
        assert config.output_dir == Path("output")
        assert config.cache_dir == Path("cache")
        assert config.max_pdf_pages == 500
        assert config.max_pdf_size_mb == 50
        assert config.target_language == "ht"
        assert config.enable_cache == True
    
    def test_config_paths(self):
        """Test configuration path properties"""
        config = Config()
        
        assert config.output_text_path == Path("data/output_text.txt")
        assert config.output_translation_path == Path("output/traduction.txt")
        assert config.output_audio_path == Path("output/audiobook.mp3")
    
    def test_config_from_env(self):
        """Test configuration from environment variables"""
        # Set environment variables
        os.environ["MAX_PDF_PAGES"] = "100"
        os.environ["CHUNK_SIZE"] = "500"
        os.environ["ENABLE_CACHE"] = "false"
        
        config = Config.from_env()
        
        assert config.max_pdf_pages == 100
        assert config.chunk_size == 500
        assert config.enable_cache == False
        
        # Clean up
        del os.environ["MAX_PDF_PAGES"]
        del os.environ["CHUNK_SIZE"]
        del os.environ["ENABLE_CACHE"]
    
    def test_config_to_dict(self):
        """Test configuration to dictionary"""
        config = Config()
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert "translation_model" in config_dict
        assert "target_language" in config_dict
        assert "enable_cache" in config_dict
    
    def test_config_str(self):
        """Test configuration string representation"""
        config = Config()
        config_str = str(config)
        
        assert "Config" in config_str
        assert "ht" in config_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

