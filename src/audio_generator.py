#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audio Generator Module
Generate audiobooks from text using TTS
"""

import logging
from pathlib import Path
from typing import Optional, List
from gtts import gTTS

from .config import Config
from .utils import format_file_size

# Try to import enhanced TTS
try:
    from .tts_enhanced import EnhancedTTS
    ENHANCED_TTS_AVAILABLE = True
except ImportError:
    ENHANCED_TTS_AVAILABLE = False

logger = logging.getLogger('KreyolAI.AudioGenerator')


class AudiobookGenerator:
    """Klas pou kreye liv odyo / Class for audiobook generation"""
    
    def __init__(self, config: Config, use_enhanced: bool = True):
        """
        Initialize audio generator
        
        Args:
            config: Configuration object
            use_enhanced: Use enhanced TTS with better Creole pronunciation
        """
        self.config = config
        self.use_enhanced = use_enhanced and ENHANCED_TTS_AVAILABLE
        
        if self.use_enhanced:
            self.enhanced_tts = EnhancedTTS()
            logger.info("Audio generator initialized with enhanced TTS")
        else:
            self.enhanced_tts = None
            logger.info("Audio generator initialized with standard TTS")
    
    def generate(
        self,
        text: str,
        output_path: Optional[Path] = None,
        language: Optional[str] = None,
        slow: Optional[bool] = None
    ) -> Path:
        """
        Jenere liv odyo / Generate audiobook
        
        Args:
            text: Text to convert to speech
            output_path: Output MP3 file path
            language: Language for TTS (default: config.tts_language)
            slow: Slow speech (default: config.tts_slow)
        
        Returns:
            Path to generated audio file
        
        Raises:
            ValueError: If text is too long or empty
            RuntimeError: If audio generation fails
        """
        if not text or not text.strip():
            raise ValueError("Text is empty")
        
        # Use config defaults if not provided
        if language is None:
            language = self.config.tts_language
        if slow is None:
            slow = self.config.tts_slow
        if output_path is None:
            output_path = self.config.output_audio_path
        
        output_path = Path(output_path)
        
        # Check text length
        if len(text) > self.config.max_audio_chars:
            logger.warning(
                f"Text too long ({len(text)} chars), truncating to {self.config.max_audio_chars}"
            )
            print(f"⚠️  Tèks twò long / Text too long: {len(text)} → {self.config.max_audio_chars} karaktè")
            text = text[:self.config.max_audio_chars]
        
        try:
            logger.info(f"Generating audio: {len(text)} chars, lang={language}, slow={slow}")
            print(f"🎧 Ap kreye odyo / Generating audio...")
            print(f"   Lang / Language: {language}")
            print(f"   Karaktè / Characters: {len(text)}")
            
            # Use enhanced TTS for better Creole pronunciation
            if self.use_enhanced and language == 'ht':
                print(f"   🌟 Using enhanced TTS for better Creole pronunciation")
                try:
                    _, engine_used = self.enhanced_tts.generate_best_available(
                        text, output_path, prefer_quality=True
                    )
                    print(f"   Engine: {engine_used}")
                    
                    # Verify file was created
                    if not output_path.exists():
                        raise RuntimeError("Audio file was not created")
                    
                    # Get file size
                    file_size = format_file_size(output_path.stat().st_size)
                    
                    logger.info(f"Audio generated successfully: {output_path} ({file_size})")
                    print(f"✅ Liv odyo sove nan / Audiobook saved to: {output_path}")
                    print(f"   📊 Gwosè / Size: {file_size}")
                    
                    return output_path
                except Exception as e:
                    logger.warning(f"Enhanced TTS failed, falling back to standard: {e}")
                    print(f"   ⚠️  Enhanced TTS not available, using standard French")
            
            # Standard gTTS fallback
            # gTTS doesn't support Haitian Creole (ht), use French (fr) instead
            actual_language = 'fr' if language == 'ht' else language
            
            if language == 'ht':
                print(f"   Note: Using French (fr) for audio (best available for Creole)")
            
            # Generate audio with gTTS
            tts = gTTS(text=text, lang=actual_language, slow=slow)
            
            # Ensure output directory exists
            output_path.parent.mkdir(exist_ok=True)
            
            # Save audio file
            tts.save(str(output_path))
            
            # Verify file was created
            if not output_path.exists():
                raise RuntimeError("Audio file was not created")
            
            # Get file size
            file_size = format_file_size(output_path.stat().st_size)
            
            logger.info(f"Audio generated successfully: {output_path} ({file_size})")
            print(f"✅ Liv odyo sove nan / Audiobook saved to: {output_path}")
            print(f"   📊 Gwosè / Size: {file_size}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Audio generation error: {e}")
            raise RuntimeError(f"Erè kreyasyon odyo / Audio generation error: {e}")
    
    def generate_from_file(
        self,
        text_file: Path,
        output_path: Optional[Path] = None,
        language: Optional[str] = None
    ) -> Path:
        """
        Generate audiobook from text file
        
        Args:
            text_file: Path to text file
            output_path: Output MP3 file path
            language: Language for TTS
        
        Returns:
            Path to generated audio file
        """
        text_file = Path(text_file)
        
        if not text_file.exists():
            raise FileNotFoundError(f"Text file not found: {text_file}")
        
        logger.info(f"Reading text from: {text_file}")
        
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        return self.generate(text, output_path=output_path, language=language)
    
    def split_and_generate(
        self,
        text: str,
        max_chunk_size: int = 100000,
        output_dir: Optional[Path] = None
    ) -> List[Path]:
        """
        Split long text and generate multiple audio files
        
        Args:
            text: Text to convert
            max_chunk_size: Maximum characters per audio file
            output_dir: Output directory
        
        Returns:
            List of generated audio file paths
        """
        if output_dir is None:
            output_dir = self.config.output_dir
        
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # Split text into chunks
        chunks = []
        current = ""
        
        for paragraph in text.split('\n\n'):
            if len(current) + len(paragraph) < max_chunk_size:
                current += paragraph + "\n\n"
            else:
                if current:
                    chunks.append(current)
                current = paragraph + "\n\n"
        
        if current:
            chunks.append(current)
        
        logger.info(f"Split into {len(chunks)} audio files")
        print(f"  📊 {len(chunks)} fichye odyo / audio files")
        
        # Generate audio for each chunk
        audio_files = []
        for i, chunk in enumerate(chunks, 1):
            output_path = output_dir / f"audiobook_part{i:02d}.mp3"
            logger.info(f"Generating part {i}/{len(chunks)}")
            print(f"\n📀 Pati {i}/{len(chunks)}")
            
            audio_file = self.generate(chunk, output_path=output_path)
            audio_files.append(audio_file)
        
        logger.info(f"Generated {len(audio_files)} audio files")
        return audio_files
    
    def get_audio_info(self, audio_path: Path) -> dict:
        """
        Get audio file information
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            Dictionary with audio info
        """
        audio_path = Path(audio_path)
        
        if not audio_path.exists():
            return {}
        
        try:
            size_bytes = audio_path.stat().st_size
            return {
                'path': str(audio_path),
                'size': format_file_size(size_bytes),
                'size_bytes': size_bytes,
                'exists': True,
            }
        except Exception as e:
            logger.warning(f"Could not get audio info: {e}")
            return {'exists': False}

