#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fonksyon Itil / Utility Functions
Common utilities used across modules
"""

import re
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import List


def setup_logging(log_dir: Path = Path("logs"), log_level: str = "INFO") -> logging.Logger:
    """
    Konfigire sistèm logging / Configure logging system
    
    Args:
        log_dir: Directory for log files
        log_level: Logging level (INFO, WARNING, ERROR, DEBUG)
    
    Returns:
        Logger instance
    """
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"kreyol_ai_{datetime.now():%Y%m%d_%H%M%S}.log"
    
    # Create logger
    logger = logging.getLogger('KreyolAI')
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    logger.info(f"Logging initialized: {log_file}")
    return logger


def smart_chunk_text(text: str, max_size: int = 1000) -> List[str]:
    """
    Divize tèks entèlijan / Smart text chunking
    Respects paragraph and sentence boundaries
    
    Args:
        text: Text to chunk
        max_size: Maximum chunk size in characters
    
    Returns:
        List of text chunks
    """
    if not text or len(text) <= max_size:
        return [text] if text else []
    
    chunks = []
    
    # Split by double newlines (paragraphs)
    paragraphs = re.split(r'\n\s*\n', text)
    current_chunk = ""
    
    for para in paragraphs:
        # If paragraph fits in current chunk
        if len(current_chunk) + len(para) + 2 <= max_size:
            current_chunk += para + "\n\n"
        else:
            # Save current chunk if not empty
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            # If paragraph itself is too long, split by sentences
            if len(para) > max_size:
                sentences = re.split(r'(?<=[.!?])\s+', para)
                temp = ""
                
                for sentence in sentences:
                    if len(temp) + len(sentence) + 1 <= max_size:
                        temp += sentence + " "
                    else:
                        if temp:
                            chunks.append(temp.strip())
                        # If even a single sentence is too long, force split
                        if len(sentence) > max_size:
                            for i in range(0, len(sentence), max_size):
                                chunks.append(sentence[i:i+max_size])
                            temp = ""
                        else:
                            temp = sentence + " "
                
                if temp:
                    current_chunk = temp
                else:
                    current_chunk = ""
            else:
                current_chunk = para + "\n\n"
    
    # Add remaining chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted string (e.g., "1.5MB", "500KB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f}TB"


def estimate_processing_time(pages: int, text_length: int) -> int:
    """
    Estimate processing time in seconds
    
    Args:
        pages: Number of PDF pages
        text_length: Length of text in characters
    
    Returns:
        Estimated time in seconds
    """
    # Rough estimates based on testing
    extraction_time = pages * 0.3  # ~0.3s per page
    translation_time = (text_length // 1000) * 2  # ~2s per 1000 chars
    audio_time = (text_length // 10000) * 5  # ~5s per 10000 chars
    
    return int(extraction_time + translation_time + audio_time)


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Text to clean
    
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove control characters
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    return text.strip()

