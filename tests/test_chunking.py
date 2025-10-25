#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests pou chunking entèlijan / Tests for smart chunking
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import smart_chunk_text


def test_chunking_preserves_content():
    """Verify chunking doesn't lose content"""
    original = "This is a test. " * 100  # Long text
    chunks = smart_chunk_text(original, max_size=100)
    
    # Recombine chunks
    recombined = "".join(chunks)
    
    # Should preserve most content (allowing for some whitespace differences)
    assert len(recombined) >= len(original) * 0.95


def test_chunk_sizes():
    """Verify chunks don't exceed max_size"""
    text = "Word " * 500  # Create long text
    max_size = 200
    chunks = smart_chunk_text(text, max_size=max_size)
    
    for i, chunk in enumerate(chunks):
        # Allow some overflow for the last words
        assert len(chunk) <= max_size + 50, f"Chunk {i} too large: {len(chunk)}"


def test_paragraph_boundaries():
    """Test that paragraphs are kept together when possible"""
    text = """First paragraph is here.

Second paragraph is here.

Third paragraph is here."""
    
    chunks = smart_chunk_text(text, max_size=100)
    
    # Each paragraph should ideally be in its own chunk
    assert len(chunks) >= 3
    
    # First chunk should contain first paragraph
    assert "First paragraph" in chunks[0]


def test_sentence_boundaries():
    """Test that sentences are respected"""
    text = "Sentence one. Sentence two. Sentence three. Sentence four. Sentence five."
    chunks = smart_chunk_text(text, max_size=30)
    
    # Should have multiple chunks
    assert len(chunks) >= 2
    
    # Each chunk should end with punctuation or be the last chunk
    for i, chunk in enumerate(chunks[:-1]):
        assert chunk.strip()[-1] in '.!?', f"Chunk {i} doesn't end with punctuation: '{chunk[-20:]}'"


def test_empty_text():
    """Test handling of empty text"""
    chunks = smart_chunk_text("", max_size=100)
    assert len(chunks) == 1
    assert chunks[0] == ""


def test_single_long_word():
    """Test handling of a single very long 'word'"""
    long_word = "a" * 2000
    chunks = smart_chunk_text(long_word, max_size=500)
    
    # Should be split into multiple chunks
    assert len(chunks) == 4
    
    # Each chunk should be around max_size
    for chunk in chunks:
        assert len(chunk) <= 500


def test_real_world_text():
    """Test with realistic text"""
    text = """
    Kreyòl ayisyen se yon lang kreol ki baze sou franse. Li pale nan Ayiti pa prèske 10 milyon moun.
    
    Lang sa a gen yon istwa rich e li enpòtan anpil pou kiltir ayisyen. Li devlope pandan epòk koloni franse a.
    
    Jodi a, kreyòl ayisyen se youn nan de lang ofisyèl Ayiti, ansanm ak franse. Gen anpil efò k ap fèt pou pwomote lang sa a.
    """
    
    chunks = smart_chunk_text(text, max_size=150)
    
    # Should create multiple chunks
    assert len(chunks) >= 2
    
    # Verify no chunk is too large
    for chunk in chunks:
        assert len(chunk) <= 200  # Some tolerance
    
    # Verify content is preserved
    combined = " ".join(chunks)
    assert "Kreyòl ayisyen" in combined
    assert "lang ofisyèl" in combined


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

