#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Konfigirasyon / Configuration Module
Centralized configuration for the application
"""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class Config:
    """Klas konfigirasyon prensipal / Main configuration class"""
    
    # Chemen / Paths
    data_dir: Path = field(default_factory=lambda: Path("data"))
    output_dir: Path = field(default_factory=lambda: Path("output"))
    cache_dir: Path = field(default_factory=lambda: Path("cache"))
    logs_dir: Path = field(default_factory=lambda: Path("logs"))
    
    # PDF Settings
    pdf_input_path: Path = field(default_factory=lambda: Path("data/input.pdf"))
    max_pdf_pages: int = 500
    max_pdf_size_mb: int = 50
    
    # Translation Settings
    translation_model: str = "facebook/m2m100_418M"
    source_language: Optional[str] = None  # Auto-detect if None
    target_language: str = "ht"  # Haitian Creole
    chunk_size: int = 1000
    enable_cache: bool = True
    
    # Audio Settings
    tts_language: str = "ht"  # Note: gTTS will use 'fr' for Haitian Creole
    tts_slow: bool = False
    max_audio_chars: int = 100000
    
    # Processing Settings
    enable_parallel: bool = False  # Parallel processing
    max_workers: int = 3
    
    # Logging
    log_level: str = "INFO"
    log_to_console: bool = True
    log_to_file: bool = True
    
    def __post_init__(self):
        """Validate and create directories"""
        # Load from environment if available
        self.source_language = os.getenv("SOURCE_LANGUAGE", self.source_language)
        self.target_language = os.getenv("TARGET_LANGUAGE", self.target_language)
        self.tts_language = os.getenv("TTS_LANGUAGE", self.tts_language)
        
        # Create directories
        for directory in [self.data_dir, self.output_dir, self.cache_dir, self.logs_dir]:
            directory.mkdir(exist_ok=True)
    
    @property
    def output_text_path(self) -> Path:
        """Path to extracted text output"""
        return self.data_dir / "output_text.txt"
    
    @property
    def output_translation_path(self) -> Path:
        """Path to translation output"""
        return self.output_dir / "traduction.txt"
    
    @property
    def output_audio_path(self) -> Path:
        """Path to audiobook output"""
        return self.output_dir / "audiobook.mp3"
    
    def get_cache_enabled(self) -> bool:
        """Check if cache is enabled"""
        return self.enable_cache and self.cache_dir.exists()
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Create config from environment variables"""
        return cls(
            max_pdf_pages=int(os.getenv("MAX_PDF_PAGES", 500)),
            max_pdf_size_mb=int(os.getenv("MAX_PDF_SIZE_MB", 50)),
            translation_model=os.getenv("TRANSLATION_MODEL", "facebook/m2m100_418M"),
            chunk_size=int(os.getenv("CHUNK_SIZE", 1000)),
            enable_cache=os.getenv("ENABLE_CACHE", "true").lower() == "true",
            enable_parallel=os.getenv("ENABLE_PARALLEL", "false").lower() == "true",
            max_workers=int(os.getenv("MAX_WORKERS", 3)),
        )
    
    def to_dict(self) -> dict:
        """Convert config to dictionary"""
        return {
            "data_dir": str(self.data_dir),
            "output_dir": str(self.output_dir),
            "cache_dir": str(self.cache_dir),
            "max_pdf_pages": self.max_pdf_pages,
            "max_pdf_size_mb": self.max_pdf_size_mb,
            "translation_model": self.translation_model,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "chunk_size": self.chunk_size,
            "enable_cache": self.enable_cache,
            "enable_parallel": self.enable_parallel,
        }
    
    def __str__(self) -> str:
        """String representation"""
        return f"Config(model={self.translation_model}, target={self.target_language}, cache={self.enable_cache})"

