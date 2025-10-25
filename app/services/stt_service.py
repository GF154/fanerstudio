#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📝 Speech-to-Text Service
Sèvis pou konvèti paròl an tèks
Sipòte: Whisper (Local/OpenAI), AssemblyAI
"""

from pathlib import Path
import asyncio
import os
import httpx
import json

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

class STTService:
    """Sèvis Speech-to-Text"""
    
    def __init__(self):
        """Inisyalize sèvis STT"""
        print("✅ STT Service initialized")
    
    async def transcribe(self, audio_path: Path, engine: str = "auto") -> str:
        """
        Transkripsyon fichye odyo
        
        Args:
            audio_path: Chemen fichye odyo a
            engine: Engine pou itilize:
                   - "auto": Automatic (prefer local Whisper if available)
                   - "whisper-local": Local Whisper model
                   - "whisper-openai": OpenAI Whisper API
                   - "assemblyai": AssemblyAI API
            
        Returns:
            str: Tèks ki soti nan odyo a
        """
        try:
            if engine == "auto":
                # Try local Whisper first, then OpenAI, then AssemblyAI
                try:
                    return await self._transcribe_whisper_local(audio_path)
                except:
                    if OPENAI_API_KEY:
                        return await self._transcribe_whisper_openai(audio_path)
                    elif ASSEMBLYAI_API_KEY:
                        return await self._transcribe_assemblyai(audio_path)
                    else:
                        raise ValueError("Pa gen STT engine disponib. Konfigire API key oswa enstale Whisper.")
            
            elif engine == "whisper-local":
                return await self._transcribe_whisper_local(audio_path)
            
            elif engine == "whisper-openai":
                return await self._transcribe_whisper_openai(audio_path)
            
            elif engine == "assemblyai":
                return await self._transcribe_assemblyai(audio_path)
            
            else:
                raise ValueError(f"Engine STT pa valid: {engine}")
            
        except Exception as e:
            print(f"❌ Error transcribing audio: {e}")
            raise
    
    async def _transcribe_whisper_local(self, audio_path: Path) -> str:
        """
        Transkripsyon ak Whisper local
        Bezwen: pip install openai-whisper
        """
        try:
            import whisper
            
            # Load model (base is good balance of speed/accuracy)
            model = whisper.load_model("base")
            
            # Transcribe
            result = model.transcribe(str(audio_path), language="ht")  # Haitian Creole
            
            print(f"✅ Transcribed with local Whisper: {len(result['text'])} characters")
            return result["text"]
            
        except ImportError:
            raise ImportError("Whisper pa enstale! Run: pip install openai-whisper")
        except Exception as e:
            print(f"❌ Whisper local error: {e}")
            raise
    
    async def _transcribe_whisper_openai(self, audio_path: Path) -> str:
        """
        Transkripsyon ak OpenAI Whisper API
        """
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY pa konfigire! Set li nan .env")
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                # Read audio file
                with open(audio_path, "rb") as audio_file:
                    files = {
                        "file": (audio_path.name, audio_file, "audio/mpeg"),
                        "model": (None, "whisper-1"),
                        "language": (None, "ht")  # Haitian Creole
                    }
                    
                    response = await client.post(
                        "https://api.openai.com/v1/audio/transcriptions",
                        headers={
                            "Authorization": f"Bearer {OPENAI_API_KEY}"
                        },
                        files=files
                    )
                
                response.raise_for_status()
                result = response.json()
                
                print(f"✅ Transcribed with OpenAI Whisper: {len(result['text'])} characters")
                return result["text"]
                
        except Exception as e:
            print(f"❌ OpenAI Whisper error: {e}")
            raise
    
    async def _transcribe_assemblyai(self, audio_path: Path) -> str:
        """
        Transkripsyon ak AssemblyAI
        """
        if not ASSEMBLYAI_API_KEY:
            raise ValueError("ASSEMBLYAI_API_KEY pa konfigire! Set li nan .env")
        
        try:
            headers = {
                "authorization": ASSEMBLYAI_API_KEY,
                "content-type": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=300.0) as client:
                # Step 1: Upload audio file
                print("📤 Upload audio to AssemblyAI...")
                with open(audio_path, "rb") as audio_file:
                    upload_response = await client.post(
                        "https://api.assemblyai.com/v2/upload",
                        headers={"authorization": ASSEMBLYAI_API_KEY},
                        content=audio_file.read()
                    )
                
                upload_response.raise_for_status()
                audio_url = upload_response.json()["upload_url"]
                
                # Step 2: Request transcription
                print("🎤 Request transcription...")
                transcription_response = await client.post(
                    "https://api.assemblyai.com/v2/transcript",
                    headers=headers,
                    json={
                        "audio_url": audio_url,
                        "language_code": "ht"  # Haitian Creole
                    }
                )
                
                transcription_response.raise_for_status()
                transcript_id = transcription_response.json()["id"]
                
                # Step 3: Poll for completion
                print("⏳ Wait for transcription...")
                while True:
                    status_response = await client.get(
                        f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
                        headers=headers
                    )
                    
                    status_response.raise_for_status()
                    status_data = status_response.json()
                    
                    if status_data["status"] == "completed":
                        print(f"✅ Transcribed with AssemblyAI: {len(status_data['text'])} characters")
                        return status_data["text"]
                    
                    elif status_data["status"] == "error":
                        raise Exception(f"AssemblyAI error: {status_data.get('error')}")
                    
                    # Wait before polling again
                    await asyncio.sleep(3)
                    
        except Exception as e:
            print(f"❌ AssemblyAI error: {e}")
            raise
    
    async def transcribe_audio(self, audio_path: str, engine: str = "auto") -> str:
        """
        Transkripsyon fichye odyo (alias pou transcribe)
        
        Args:
            audio_path: Chemen fichye odyo a kòm string
            engine: Engine pou itilize (auto, whisper-local, whisper-openai, assemblyai)
            
        Returns:
            str: Tèks ki soti nan odyo a
        """
        return await self.transcribe(Path(audio_path), engine)
    
    def get_supported_formats(self) -> list:
        """Jwenn lis fòma sipòte yo"""
        return [".mp3", ".wav", ".m4a", ".ogg", ".flac", ".webm"]
    
    def get_available_engines(self) -> list:
        """Jwenn lis STT engines disponib yo"""
        engines = []
        
        # Check if local Whisper is available
        try:
            import whisper
            engines.append({
                "id": "whisper-local",
                "name": "Whisper Local",
                "provider": "OpenAI",
                "cost": "free",
                "speed": "medium",
                "accuracy": "high"
            })
        except ImportError:
            pass
        
        # Check if OpenAI API key is available
        if OPENAI_API_KEY:
            engines.append({
                "id": "whisper-openai",
                "name": "Whisper API",
                "provider": "OpenAI",
                "cost": "$0.006/minute",
                "speed": "fast",
                "accuracy": "high"
            })
        
        # Check if AssemblyAI key is available
        if ASSEMBLYAI_API_KEY:
            engines.append({
                "id": "assemblyai",
                "name": "AssemblyAI",
                "provider": "AssemblyAI",
                "cost": "$0.00025/second",
                "speed": "fast",
                "accuracy": "very high"
            })
        
        return engines


# Standalone function pou import fasil
async def transcribe_audio(audio_path: str, engine: str = "auto") -> str:
    """
    Fonksyon global pou transkripsyon odyo
    Rele sèvis speech-to-text (Whisper/AssemblyAI) epi retounen tèks
    
    Args:
        audio_path: Chemen fichye odyo a
        engine: Engine pou itilize (auto, whisper-local, whisper-openai, assemblyai)
        
    Returns:
        str: Tèks ki soti nan odyo a (transkripsyon)
    """
    service = STTService()
    return await service.transcribe_audio(audio_path, engine)

