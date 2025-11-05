#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗣️ Text-to-Speech (TTS) Engine for Audiobook Generation
Motè TTS pou jenere audiobook
"""

import io
import os
import tempfile
from typing import Optional, Literal
from pathlib import Path

# gTTS - Google Text-to-Speech (Simple & Free)
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("⚠️ gTTS not available - install with: pip install gtts")

# pyttsx3 - Offline TTS
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    print("⚠️ pyttsx3 not available - install with: pip install pyttsx3")


class TTSEngine:
    """Text-to-Speech engine for audiobook generation"""
    
    def __init__(self, engine: str = "gtts"):
        """
        Initialize TTS engine
        
        Args:
            engine: TTS engine to use ('gtts' or 'pyttsx3')
        """
        self.engine = engine
        
        if engine == "gtts" and not GTTS_AVAILABLE:
            raise ImportError("gTTS not installed. Install with: pip install gtts")
        
        if engine == "pyttsx3" and not PYTTSX3_AVAILABLE:
            raise ImportError("pyttsx3 not installed. Install with: pip install pyttsx3")
    
    def generate_audio_gtts(
        self,
        text: str,
        output_file: str,
        lang: str = "en",
        slow: bool = False
    ) -> str:
        """
        Generate audio using gTTS
        
        Args:
            text: Text to convert
            output_file: Output file path
            lang: Language code (en, fr, ht, etc.)
            slow: Slow speed
            
        Returns:
            Path to generated audio file
        """
        try:
            tts = gTTS(text=text, lang=lang, slow=slow)
            tts.save(output_file)
            return output_file
        
        except Exception as e:
            raise Exception(f"gTTS error: {str(e)}")
    
    def generate_audio_pyttsx3(
        self,
        text: str,
        output_file: str,
        rate: int = 150,
        volume: float = 1.0,
        voice_gender: Optional[str] = None
    ) -> str:
        """
        Generate audio using pyttsx3 (offline)
        
        Args:
            text: Text to convert
            output_file: Output file path
            rate: Speech rate (words per minute)
            volume: Volume (0.0 to 1.0)
            voice_gender: 'male' or 'female' (optional)
            
        Returns:
            Path to generated audio file
        """
        try:
            engine = pyttsx3.init()
            
            # Set properties
            engine.setProperty('rate', rate)
            engine.setProperty('volume', volume)
            
            # Set voice if specified
            if voice_gender:
                voices = engine.getProperty('voices')
                for voice in voices:
                    if voice_gender.lower() in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
            
            # Save to file
            engine.save_to_file(text, output_file)
            engine.runAndWait()
            
            return output_file
        
        except Exception as e:
            raise Exception(f"pyttsx3 error: {str(e)}")
    
    def generate_audio(
        self,
        text: str,
        output_file: Optional[str] = None,
        voice: str = "natural",
        speed: float = 1.0,
        pitch: int = 0,
        format: str = "mp3",
        lang: str = "en"
    ) -> str:
        """
        Generate audio from text
        
        Args:
            text: Text to convert
            output_file: Output file path (auto-generated if None)
            voice: Voice type ('natural', 'male', 'female')
            speed: Speech speed (0.5 to 2.0)
            pitch: Pitch adjustment (-2 to +2)
            format: Output format ('mp3', 'wav')
            lang: Language code
            
        Returns:
            Path to generated audio file
        """
        # Generate output file if not provided
        if not output_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{format}') as tmp:
                output_file = tmp.name
        
        # Use gTTS by default (simple and reliable)
        if self.engine == "gtts" or GTTS_AVAILABLE:
            # Map speed to slow parameter
            slow = speed < 1.0
            
            # Generate audio
            return self.generate_audio_gtts(
                text=text,
                output_file=output_file,
                lang=lang,
                slow=slow
            )
        
        # Fallback to pyttsx3
        elif self.engine == "pyttsx3" or PYTTSX3_AVAILABLE:
            # Map speed to rate
            rate = int(150 * speed)
            
            # Map voice to gender
            voice_gender = None
            if voice == "male":
                voice_gender = "male"
            elif voice == "female":
                voice_gender = "female"
            
            return self.generate_audio_pyttsx3(
                text=text,
                output_file=output_file,
                rate=rate,
                voice_gender=voice_gender
            )
        
        else:
            raise ImportError("No TTS engine available. Install gTTS or pyttsx3")
    
    @staticmethod
    def get_available_engines():
        """Return list of available TTS engines"""
        engines = {
            "gtts": GTTS_AVAILABLE,
            "pyttsx3": PYTTSX3_AVAILABLE
        }
        return engines
    
    @staticmethod
    def chunk_text(text: str, max_length: int = 5000) -> list:
        """
        Split text into chunks for processing
        
        Args:
            text: Full text
            max_length: Maximum characters per chunk
            
        Returns:
            List of text chunks
        """
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            # If adding this paragraph exceeds limit, save current and start new
            if len(current_chunk) + len(para) > max_length and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = para
            else:
                current_chunk += "\n\n" + para if current_chunk else para
        
        # Add final chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks


# Quick test function
if __name__ == "__main__":
    tts = TTSEngine()
    
    print("🗣️ Text-to-Speech Engine")
    print("=" * 50)
    print("\n✅ Available engines:")
    for engine, available in tts.get_available_engines().items():
        status = "✅" if available else "❌"
        print(f"  {status} {engine}")
    
    print("\n💡 Usage:")
    print("  from tts_engine import TTSEngine")
    print('  tts = TTSEngine()')
    print('  audio_file = tts.generate_audio("Your text here", output_file="output.mp3")')
    
    # Test if available
    if GTTS_AVAILABLE:
        print("\n🧪 Running quick test...")
        try:
            test_file = "test_audio.mp3"
            tts.generate_audio("Hello, this is a test.", output_file=test_file)
            print(f"✅ Test successful! Audio saved to: {test_file}")
        except Exception as e:
            print(f"❌ Test failed: {e}")

