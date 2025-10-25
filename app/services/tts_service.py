#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗣️ Text-to-Speech Service
Sèvis pou konvèti tèks an paròl
Sipòte: Kreyòl natif, OpenAI TTS, ElevenLabs
"""

from pathlib import Path
from datetime import datetime
import uuid
import sys
import os
import httpx

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

class TTSService:
    """Sèvis Text-to-Speech"""
    
    def __init__(self):
        """Inisyalize sèvis TTS"""
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        print("✅ TTS Service initialized")
    
    async def generate_speech(self, text: str, voice: str = "creole-native") -> Path:
        """
        Jenere paròl soti nan tèks
        
        Args:
            text: Tèks pou konvèti
            voice: Vwa pou itilize
            
        Returns:
            Path: Chemen fichye odyo a
        """
        try:
            # Import here to avoid circular dependencies
            sys.path.insert(0, str(Path(__file__).parent.parent.parent))
            from generer_audio_huggingface import generer_audio_creole
            
            # Generate unique filename
            filename = f"tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.mp3"
            output_path = self.output_dir / filename
            
            # Generate audio
            generer_audio_creole(text, output_path)
            
            print(f"✅ Audio generated: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error generating audio: {e}")
            raise
    
    async def text_to_speech_file(self, text: str, output_path: str, voice: str = "creole-native") -> Path:
        """
        Konvèti tèks an paròl epi sove nan yon fichye espesifik
        Sipòte plizyè TTS engines: Kreyòl natif, OpenAI, ElevenLabs
        
        Args:
            text: Tèks pou konvèti
            output_path: Chemen fichye pou sove
            voice: Vwa pou itilize
                  - "creole-native": Kreyòl natif (default)
                  - "openai-alloy", "openai-echo", "openai-fable", etc.
                  - "elevenlabs-<voice_id>": ElevenLabs voice
            
        Returns:
            Path: Chemen fichye odyo a
        """
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Chwazi TTS engine selon vwa
            if voice.startswith("openai-"):
                return await self._tts_openai(text, output_file, voice)
            elif voice.startswith("elevenlabs-"):
                return await self._tts_elevenlabs(text, output_file, voice)
            else:
                # Use native Creole TTS
                return await self._tts_creole_native(text, output_file)
            
        except Exception as e:
            print(f"❌ Error generating audio file: {e}")
            raise
    
    async def _tts_creole_native(self, text: str, output_file: Path) -> Path:
        """TTS ak engine Kreyòl natif"""
        # Validate text
        if not text or len(text.strip()) < 3:
            raise ValueError("Text tro kout oswa vid! Minimoum 3 karaktè.")
        
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from generer_audio_huggingface import generer_audio_creole
        
        generer_audio_creole(text, output_file)
        print(f"✅ Audio saved (Creole native): {output_file}")
        return output_file
    
    async def _tts_openai(self, text: str, output_file: Path, voice: str) -> Path:
        """
        TTS ak OpenAI
        Vwa disponib: alloy, echo, fable, onyx, nova, shimmer
        """
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY pa konfigire! Set li nan .env")
        
        # Extract voice name (openai-alloy -> alloy)
        voice_name = voice.replace("openai-", "")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/audio/speech",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "tts-1",  # or "tts-1-hd" for higher quality
                    "input": text,
                    "voice": voice_name,
                    "response_format": "mp3"
                }
            )
            
            response.raise_for_status()
            
            # Save audio
            output_file.write_bytes(response.content)
            print(f"✅ Audio saved (OpenAI {voice_name}): {output_file}")
            return output_file
    
    async def _tts_elevenlabs(self, text: str, output_file: Path, voice: str) -> Path:
        """
        TTS ak ElevenLabs
        voice format: elevenlabs-<voice_id>
        """
        if not ELEVENLABS_API_KEY:
            raise ValueError("ELEVENLABS_API_KEY pa konfigire! Set li nan .env")
        
        # Extract voice ID (elevenlabs-21m00Tcm4TlvDq8ikWAM -> 21m00Tcm4TlvDq8ikWAM)
        voice_id = voice.replace("elevenlabs-", "")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                headers={
                    "xi-api-key": ELEVENLABS_API_KEY,
                    "Content-Type": "application/json"
                },
                json={
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.75
                    }
                }
            )
            
            response.raise_for_status()
            
            # Save audio
            output_file.write_bytes(response.content)
            print(f"✅ Audio saved (ElevenLabs {voice_id}): {output_file}")
            return output_file
    
    def get_available_voices(self) -> list:
        """Jwenn lis vwa disponib yo"""
        voices = [
            {
                "id": "creole-native",
                "name": "🇭🇹 Kreyòl Ayisyen (Natif)",
                "language": "ht",
                "gender": "neutral",
                "engine": "native"
            }
        ]
        
        # Add OpenAI voices if API key is available
        if OPENAI_API_KEY:
            openai_voices = [
                {"id": "openai-alloy", "name": "OpenAI Alloy", "language": "multilingual", "gender": "neutral", "engine": "openai"},
                {"id": "openai-echo", "name": "OpenAI Echo", "language": "multilingual", "gender": "male", "engine": "openai"},
                {"id": "openai-fable", "name": "OpenAI Fable", "language": "multilingual", "gender": "neutral", "engine": "openai"},
                {"id": "openai-onyx", "name": "OpenAI Onyx", "language": "multilingual", "gender": "male", "engine": "openai"},
                {"id": "openai-nova", "name": "OpenAI Nova", "language": "multilingual", "gender": "female", "engine": "openai"},
                {"id": "openai-shimmer", "name": "OpenAI Shimmer", "language": "multilingual", "gender": "female", "engine": "openai"},
            ]
            voices.extend(openai_voices)
        
        # Add ElevenLabs info if API key is available
        if ELEVENLABS_API_KEY:
            voices.append({
                "id": "elevenlabs-custom",
                "name": "ElevenLabs (Custom Voice ID)",
                "language": "multilingual",
                "gender": "custom",
                "engine": "elevenlabs",
                "note": "Use format: elevenlabs-<voice_id>"
            })
        
        return voices


# Standalone function pou import fasil
async def text_to_speech_file(text: str, output_path: str, voice: str = "creole-native") -> Path:
    """
    Fonksyon global pou konvèti tèks an paròl
    
    Args:
        text: Tèks pou konvèti
        output_path: Chemen fichye pou sove
        voice: Vwa pou itilize
        
    Returns:
        Path: Chemen fichye odyo a
    """
    service = TTSService()
    return await service.text_to_speech_file(text, output_path, voice)

