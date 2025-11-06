#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎙️ Faner Studio - TTS Engine
Advanced Text-to-Speech for Haitian Creole
Motè TTS Avanse pou Kreyòl Ayisyen
"""

import os
import tempfile
from typing import Optional, Dict, Any
from datetime import datetime
import hashlib

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("⚠️ gTTS not available. Install: pip install gtts")

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("⚠️ Edge TTS not available. Install: pip install edge-tts")


class TTSEngine:
    """
    Advanced TTS Engine with multiple backends
    Support for Haitian Creole and multiple languages
    """
    
    SUPPORTED_ENGINES = {
        "gtts": "Google Text-to-Speech (Free, 50+ languages)",
        "edge": "Microsoft Edge TTS (Free, 100+ voices)",
        "elevenlabs": "ElevenLabs (Premium, Voice Cloning)",
        "openai": "OpenAI TTS (Premium, HD Quality)"
    }
    
    CREOLE_VOICES = {
        "gtts": "fr",  # French is phonetically closest to Haitian Creole
        "edge": "fr-FR-HenriNeural",  # Male French voice (default)
        "edge_female": "fr-FR-DeniseNeural"  # Female French voice
    }
    
    def __init__(self, engine: str = "gtts", api_key: Optional[str] = None):
        """
        Initialize TTS Engine
        
        Args:
            engine: TTS backend to use (gtts, edge, elevenlabs, openai)
            api_key: API key for premium engines
        """
        self.engine = engine.lower()
        self.api_key = api_key
        
        # Validate engine
        if self.engine not in self.SUPPORTED_ENGINES:
            raise ValueError(f"Unsupported engine: {self.engine}. Choose from: {list(self.SUPPORTED_ENGINES.keys())}")
        
        # Check availability
        if self.engine == "gtts" and not GTTS_AVAILABLE:
            raise ImportError("gTTS not installed. Run: pip install gtts")
        elif self.engine == "edge" and not EDGE_TTS_AVAILABLE:
            raise ImportError("Edge TTS not installed. Run: pip install edge-tts")
    
    async def generate_audio(
        self,
        text: str,
        language: str = "ht",
        voice: Optional[str] = None,
        output_file: Optional[str] = None,
        speed: float = 1.0,
        pitch: int = 0,
        format: str = "mp3"
    ) -> str:
        """
        Generate audio from text
        
        Args:
            text: Text to convert to speech
            language: Language code (ht for Haitian Creole)
            voice: Voice name (optional, uses default for language)
            output_file: Output file path (optional, generates temp file if None)
            speed: Speech speed (0.5 to 2.0)
            pitch: Voice pitch (-12 to +12 semitones)
            format: Audio format (mp3, wav, opus)
            
        Returns:
            Path to generated audio file
        """
        if not text or len(text.strip()) == 0:
            raise ValueError("Text cannot be empty")
        
        # Generate output file if not provided
        if not output_file:
            output_file = tempfile.NamedTemporaryFile(
                delete=False, 
                suffix=f'.{format}'
            ).name
        
        # Convert Haitian Creole to French for TTS
        tts_lang = self._get_tts_language(language)
        
        # Generate based on engine
        if self.engine == "gtts":
            return self._generate_gtts(text, tts_lang, output_file, speed)
        elif self.engine == "edge":
            return await self._generate_edge(text, tts_lang, voice, output_file, speed, pitch)
        else:
            raise NotImplementedError(f"Engine {self.engine} not yet implemented")
    
    def _get_tts_language(self, language: str) -> str:
        """
        Convert language code to TTS-compatible language
        
        Args:
            language: Input language code
            
        Returns:
            TTS-compatible language code
        """
        # Haitian Creole → French (phonetically closest)
        if language.lower() in ["ht", "hat", "kreyòl", "creole", "haitian"]:
            if self.engine == "gtts":
                return "fr"
            elif self.engine == "edge":
                return "fr-FR"
        
        return language
    
    def _generate_gtts(
        self,
        text: str,
        language: str,
        output_file: str,
        speed: float = 1.0
    ) -> str:
        """
        Generate audio using Google TTS
        
        Args:
            text: Text to convert
            language: Language code
            output_file: Output file path
            speed: Speech speed
            
        Returns:
            Path to generated audio file
        """
        try:
            # Adjust speed
            slow = speed < 0.9
            
            # Generate audio
            tts = gTTS(text=text, lang=language, slow=slow)
            tts.save(output_file)
            
            return output_file
        except Exception as e:
            raise Exception(f"gTTS generation failed: {str(e)}")
    
    async def _generate_edge(
        self,
        text: str,
        language: str,
        voice: Optional[str],
        output_file: str,
        speed: float = 1.0,
        pitch: int = 0
    ) -> str:
        """
        Generate audio using Microsoft Edge TTS
        
        Args:
            text: Text to convert
            language: Language code
            voice: Voice name
            output_file: Output file path
            speed: Speech speed
            pitch: Voice pitch
            
        Returns:
            Path to generated audio file
        """
        try:
            import asyncio
            
            # Select voice
            if not voice:
                voice = self.CREOLE_VOICES.get("edge", "fr-FR-HenriNeural")
            
            # Create TTS
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice,
                rate=self._speed_to_rate(speed),
                pitch=self._pitch_to_hz(pitch)
            )
            
            # Generate audio
            await communicate.save(output_file)
            
            return output_file
        except Exception as e:
            raise Exception(f"Edge TTS generation failed: {str(e)}")
    
    @staticmethod
    def _speed_to_rate(speed: float) -> str:
        """
        Convert speed (0.5-2.0) to Edge TTS rate format
        
        Args:
            speed: Speed multiplier
            
        Returns:
            Rate string for Edge TTS
        """
        # Edge TTS uses percentage: +50% for 1.5x, -50% for 0.5x
        percentage = int((speed - 1.0) * 100)
        
        if percentage > 0:
            return f"+{percentage}%"
        elif percentage < 0:
            return f"{percentage}%"
        else:
            return "+0%"
    
    @staticmethod
    def _pitch_to_hz(pitch: int) -> str:
        """
        Convert pitch semitones to Hz string
        
        Args:
            pitch: Pitch in semitones (-12 to +12)
            
        Returns:
            Pitch string for Edge TTS
        """
        if pitch > 0:
            return f"+{pitch}Hz"
        elif pitch < 0:
            return f"{pitch}Hz"
        else:
            return "+0Hz"
    
    @staticmethod
    def get_available_engines() -> Dict[str, str]:
        """
        Get list of available TTS engines
        
        Returns:
            Dict of engine names and descriptions
        """
        available = {}
        
        if GTTS_AVAILABLE:
            available["gtts"] = TTSEngine.SUPPORTED_ENGINES["gtts"]
        
        if EDGE_TTS_AVAILABLE:
            available["edge"] = TTSEngine.SUPPORTED_ENGINES["edge"]
        
        return available
    
    @staticmethod
    def estimate_duration(text: str, speed: float = 1.0) -> float:
        """
        Estimate audio duration from text
        
        Args:
            text: Input text
            speed: Speech speed
            
        Returns:
            Estimated duration in seconds
        """
        # Average speaking rate: ~150 words per minute
        words = len(text.split())
        duration_minutes = words / 150.0
        duration_seconds = duration_minutes * 60.0
        
        # Adjust for speed
        duration_seconds = duration_seconds / speed
        
        return duration_seconds
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """
        Format duration as MM:SS
        
        Args:
            seconds: Duration in seconds
            
        Returns:
            Formatted duration string
        """
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"


# Example usage
async def main():
    """Example usage of TTS Engine"""
    print("🎙️ Faner Studio - TTS Engine Test")
    print("=" * 50)
    
    # Show available engines
    available = TTSEngine.get_available_engines()
    print(f"\n✅ Available engines: {len(available)}")
    for name, desc in available.items():
        print(f"  - {name}: {desc}")
    
    # Test gTTS
    if "gtts" in available:
        print("\n🧪 Testing gTTS...")
        tts = TTSEngine(engine="gtts")
        
        test_text = "Bonjou! Sa se yon tès pou motè TTS Faner Studio. Mwen pale Kreyòl Ayisyen."
        
        try:
            output_file = await tts.generate_audio(
                text=test_text,
                language="ht",
                speed=1.0
            )
            print(f"✅ Audio generated: {output_file}")
            print(f"📊 Estimated duration: {tts.format_duration(tts.estimate_duration(test_text))}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test Edge TTS
    if "edge" in available:
        print("\n🧪 Testing Edge TTS...")
        tts = TTSEngine(engine="edge")
        
        test_text = "Bonjou! Sa se yon tès pou Edge TTS ak vwa Fransè."
        
        try:
            output_file = await tts.generate_audio(
                text=test_text,
                language="ht",
                speed=1.0,
                pitch=0
            )
            print(f"✅ Audio generated: {output_file}")
            print(f"📊 Estimated duration: {tts.format_duration(tts.estimate_duration(test_text))}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Test complete!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

