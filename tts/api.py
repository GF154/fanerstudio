#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎙️ Faner Studio - TTS API Server
FastAPI server for Text-to-Speech
Sèvè API FastAPI pou TTS
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import os
import tempfile
from datetime import datetime
import asyncio

# Import TTS Engine
try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from tts.main import TTSEngine
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️ TTS Engine not available")


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="🎙️ Faner Studio - TTS API",
    description="Advanced Text-to-Speech API for Haitian Creole",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PYDANTIC MODELS
# ============================================================

class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to convert to speech", min_length=1, max_length=10000)
    language: str = Field(default="ht", description="Language code (ht for Haitian Creole)")
    engine: str = Field(default="gtts", description="TTS engine (gtts, edge)")
    voice: Optional[str] = Field(None, description="Voice name (optional)")
    speed: float = Field(default=1.0, ge=0.5, le=2.0, description="Speech speed (0.5 to 2.0)")
    pitch: int = Field(default=0, ge=-12, le=12, description="Voice pitch (-12 to +12)")
    format: str = Field(default="mp3", description="Audio format (mp3, wav, opus)")


class TTSResponse(BaseModel):
    success: bool
    message: str
    audio_url: str
    filename: str
    duration: str
    estimated_size: str
    metadata: dict


class EngineInfo(BaseModel):
    name: str
    description: str
    available: bool
    quality: str
    price: str


# ============================================================
# ROUTES
# ============================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "🎙️ Faner Studio TTS API",
        "version": "1.0.0",
        "status": "running",
        "tts_available": TTS_AVAILABLE,
        "endpoints": {
            "generate": "/api/tts/generate",
            "engines": "/api/tts/engines",
            "voices": "/api/tts/voices",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "tts_available": TTS_AVAILABLE,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/tts/engines")
async def get_engines():
    """Get available TTS engines"""
    if not TTS_AVAILABLE:
        raise HTTPException(status_code=503, detail="TTS Engine not available")
    
    engines = TTSEngine.get_available_engines()
    
    engine_list = []
    
    if "gtts" in engines:
        engine_list.append(EngineInfo(
            name="gtts",
            description="Google Text-to-Speech",
            available=True,
            quality="Good",
            price="Free"
        ))
    
    if "edge" in engines:
        engine_list.append(EngineInfo(
            name="edge",
            description="Microsoft Edge TTS",
            available=True,
            quality="Excellent",
            price="Free"
        ))
    
    return {
        "success": True,
        "engines": engine_list,
        "count": len(engine_list)
    }


@app.get("/api/tts/voices")
async def get_voices(language: str = "ht"):
    """Get available voices for a language"""
    voices = []
    
    if language in ["ht", "hat", "creole", "kreyol"]:
        voices = [
            {
                "id": "fr-FR-DeniseNeural",
                "name": "Denise (Female)",
                "language": "French (Haitian Creole)",
                "gender": "Female",
                "engine": "edge"
            },
            {
                "id": "fr-FR-HenriNeural",
                "name": "Henri (Male)",
                "language": "French (Haitian Creole)",
                "gender": "Male",
                "engine": "edge"
            },
            {
                "id": "fr",
                "name": "French (gTTS)",
                "language": "French (Haitian Creole)",
                "gender": "Neutral",
                "engine": "gtts"
            }
        ]
    
    return {
        "success": True,
        "language": language,
        "voices": voices,
        "count": len(voices)
    }


@app.post("/api/tts/generate")
async def generate_tts(request: TTSRequest, background_tasks: BackgroundTasks):
    """
    Generate audio from text using TTS
    """
    if not TTS_AVAILABLE:
        raise HTTPException(status_code=503, detail="TTS Engine not available")
    
    try:
        # Create TTS engine
        tts = TTSEngine(engine=request.engine)
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tts_{timestamp}.{request.format}"
        output_path = os.path.join(tempfile.gettempdir(), filename)
        
        # Generate audio
        audio_file = await tts.generate_audio(
            text=request.text,
            language=request.language,
            voice=request.voice,
            output_file=output_path,
            speed=request.speed,
            pitch=request.pitch,
            format=request.format
        )
        
        # Get file info
        file_size = os.path.getsize(audio_file)
        file_size_mb = file_size / (1024 * 1024)
        
        # Estimate duration
        duration_seconds = tts.estimate_duration(request.text, request.speed)
        duration_formatted = tts.format_duration(duration_seconds)
        
        # Schedule file cleanup after 1 hour
        # background_tasks.add_task(cleanup_file, audio_file, delay=3600)
        
        return TTSResponse(
            success=True,
            message="✅ Audio generated successfully!",
            audio_url=f"/download/{filename}",
            filename=filename,
            duration=duration_formatted,
            estimated_size=f"{file_size_mb:.2f} MB",
            metadata={
                "engine": request.engine,
                "language": request.language,
                "speed": request.speed,
                "pitch": request.pitch,
                "format": request.format,
                "text_length": len(request.text),
                "word_count": len(request.text.split()),
                "generated_at": datetime.now().isoformat()
            }
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated audio file"""
    file_path = os.path.join(tempfile.gettempdir(), filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="audio/mpeg"
    )


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

async def cleanup_file(file_path: str, delay: int = 3600):
    """
    Delete file after delay (default 1 hour)
    
    Args:
        file_path: Path to file to delete
        delay: Delay in seconds before deletion
    """
    await asyncio.sleep(delay)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"🗑️ Cleaned up: {file_path}")
    except Exception as e:
        print(f"⚠️ Failed to cleanup {file_path}: {e}")


# ============================================================
# STARTUP / SHUTDOWN
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Run on startup"""
    print("=" * 60)
    print("🎙️ Faner Studio - TTS API Server")
    print("=" * 60)
    print(f"✅ TTS Available: {TTS_AVAILABLE}")
    
    if TTS_AVAILABLE:
        engines = TTSEngine.get_available_engines()
        print(f"✅ Available engines: {len(engines)}")
        for name, desc in engines.items():
            print(f"   - {name}: {desc}")
    
    print("=" * 60)
    print("🚀 Server ready!")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Run on shutdown"""
    print("👋 Shutting down TTS API Server...")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

