#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pou fonksyon validasyon / Tests for validation functions
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import validate_text, validate_pdf_file, smart_chunk_text


class TestValidateText:
    """Test text validation"""
    
    def test_valid_text(self):
        """Test valid text passes"""
        text = "This is a valid text with more than 50 characters to pass validation."
        assert validate_text(text) == True
    
    def test_empty_text(self):
        """Test empty text raises ValueError"""
        with pytest.raises(ValueError, match="vid"):
            validate_text("")
    
    def test_short_text(self):
        """Test too short text raises ValueError"""
        with pytest.raises(ValueError, match="kout"):
            validate_text("Short", min_length=50)
    
    def test_whitespace_only(self):
        """Test whitespace-only text raises ValueError"""
        with pytest.raises(ValueError, match="vid"):
            validate_text("   \n\t  ")


class TestSmartChunking:
    """Test smart text chunking"""
    
    def test_short_text_no_chunking(self):
        """Test text shorter than max_size returns single chunk"""
        text = "Short text."
        chunks = smart_chunk_text(text, max_size=100)
        assert len(chunks) == 1
        assert chunks[0] == text
    
    def test_paragraph_chunking(self):
        """Test chunking respects paragraph boundaries"""
        text = "Paragraph 1.\n\nParagraph 2.\n\nParagraph 3."
        chunks = smart_chunk_text(text, max_size=20)
        assert len(chunks) == 3
        assert "Paragraph 1" in chunks[0]
        assert "Paragraph 2" in chunks[1]
        assert "Paragraph 3" in chunks[2]
    
    def test_sentence_chunking(self):
        """Test long paragraphs are chunked by sentences"""
        text = "This is sentence one. This is sentence two. This is sentence three."
        chunks = smart_chunk_text(text, max_size=30)
        assert len(chunks) >= 2
    
    def test_very_long_text(self):
        """Test handles very long text"""
        text = "a" * 5000
        chunks = smart_chunk_text(text, max_size=1000)
        assert len(chunks) == 5
        for chunk in chunks:
            assert len(chunk) <= 1000
    
    def test_mixed_content(self):
        """Test handles mixed paragraphs and sentences"""
        text = """This is paragraph one with multiple sentences. It has more text. And even more.

This is paragraph two. It's shorter.

Paragraph three is here."""
        chunks = smart_chunk_text(text, max_size=50)
        assert len(chunks) >= 3
        # Verify no text is lost
        combined = "".join(chunks)
        assert len(combined.replace("\n\n", "").replace(" ", "")) >= len(text.replace("\n\n", "").replace(" ", "")) - 10


class TestPDFValidation:
    """Test PDF file validation"""
    
    def test_nonexistent_file(self):
        """Test non-existent file raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            validate_pdf_file("nonexistent.pdf")
    
    def test_non_pdf_file(self):
        """Test non-PDF file raises ValueError"""
        # Create a temporary non-PDF file
        temp_file = Path("test_file.txt")
        temp_file.write_text("test")
        try:
            with pytest.raises(ValueError, match="PDF"):
                validate_pdf_file(temp_file)
        finally:
            temp_file.unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

