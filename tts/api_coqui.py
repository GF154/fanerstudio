#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎙️ Faner Studio - Advanced TTS API with Coqui TTS
FastAPI server with multiple TTS engines including Coqui
API FastAPI ak plizyè motè TTS enkli Coqui
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
import uuid

# Import TTS Engines
try:
    from TTS.api import TTS as CoquiTTS
    COQUI_AVAILABLE = True
except ImportError:
    COQUI_AVAILABLE = False
    print("⚠️ Coqui TTS not available. Install: pip install TTS")

try:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from tts.main import TTSEngine
    BASIC_TTS_AVAILABLE = True
except ImportError:
    BASIC_TTS_AVAILABLE = False
    print("⚠️ Basic TTS Engine not available")


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="🎙️ Faner Studio - TTS API",
    description="Advanced Text-to-Speech API for Haitian Creole with Coqui TTS",
    version="2.0.0"
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
# COQUI TTS MODELS
# ============================================================

COQUI_MODELS = {
    "multilingual": "tts_models/multilingual/multi-dataset/your_tts",
    "english": "tts_models/en/ljspeech/tacotron2-DDC",
    "french": "tts_models/fr/mai/tacotron2-DDC",
    "fast_multilingual": "tts_models/multilingual/multi-dataset/xtts_v2"
}

# Initialize Coqui TTS (if available)
coqui_tts = None
if COQUI_AVAILABLE:
    try:
        print("🔄 Loading Coqui TTS model...")
        coqui_tts = CoquiTTS(
            model_name=COQUI_MODELS["multilingual"],
            progress_bar=False,
            gpu=False
        )
        print("✅ Coqui TTS loaded successfully!")
    except Exception as e:
        print(f"⚠️ Failed to load Coqui TTS: {e}")
        COQUI_AVAILABLE = False


# ============================================================
# PYDANTIC MODELS
# ============================================================

class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to convert to speech", min_length=1, max_length=10000)
    language: str = Field(default="ht", description="Language code (ht for Haitian Creole)")
    engine: str = Field(default="coqui", description="TTS engine (coqui, gtts, edge)")
    voice: Optional[str] = None
    speaker: Optional[str] = None
    speed: float = Field(default=1.0, ge=0.5, le=2.0)
    pitch: int = Field(default=0, ge=-12, le=12)
    format: str = Field(default="wav", description="Audio format (wav, mp3)")


class TTSResponse(BaseModel):
    success: bool
    message: str
    audio_url: str
    filename: str
    duration: Optional[str] = None
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
        "version": "2.0.0",
        "status": "running",
        "coqui_available": COQUI_AVAILABLE,
        "basic_tts_available": BASIC_TTS_AVAILABLE,
        "endpoints": {
            "generate": "/api/tts/generate",
            "speak": "/speak",
            "engines": "/api/tts/engines",
            "models": "/api/tts/models",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "coqui_tts": COQUI_AVAILABLE,
        "basic_tts": BASIC_TTS_AVAILABLE,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/tts/engines")
async def get_engines():
    """Get available TTS engines"""
    engine_list = []
    
    if COQUI_AVAILABLE:
        engine_list.append(EngineInfo(
            name="coqui",
            description="Coqui TTS - Advanced Multi-lingual",
            available=True,
            quality="Excellent",
            price="Free (Open Source)"
        ))
    
    if BASIC_TTS_AVAILABLE:
        engines = TTSEngine.get_available_engines()
        
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


@app.get("/api/tts/models")
async def get_models():
    """Get available Coqui TTS models"""
    if not COQUI_AVAILABLE:
        return {
            "success": False,
            "message": "Coqui TTS not available",
            "models": []
        }
    
    return {
        "success": True,
        "models": [
            {
                "id": "multilingual",
                "name": "YourTTS (Multilingual)",
                "description": "Best for Haitian Creole (via French)",
                "languages": ["fr", "en", "pt", "es", "de", "it"],
                "quality": "Excellent"
            },
            {
                "id": "fast_multilingual",
                "name": "XTTS v2 (Fast)",
                "description": "Fast multilingual model",
                "languages": ["Multiple"],
                "quality": "Very Good"
            },
            {
                "id": "french",
                "name": "French Tacotron2",
                "description": "Specialized French model",
                "languages": ["fr"],
                "quality": "Excellent"
            }
        ]
    }


@app.get("/speak")
async def speak_simple(text: str, language: str = "fr"):
    """
    Simple speak endpoint (compatible with original code)
    Quickly generate speech from text
    """
    if not COQUI_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Coqui TTS not available. Install: pip install TTS"
        )
    
    try:
        # Generate unique filename
        file_name = f"audio_{uuid.uuid4().hex}.wav"
        file_path = os.path.join(tempfile.gettempdir(), file_name)
        
        # Use French for Haitian Creole
        lang = "fr" if language in ["ht", "hat", "kreyol", "creole"] else language
        
        # Generate audio
        coqui_tts.tts_to_file(
            text=text,
            file_path=file_path,
            language=lang
        )
        
        return FileResponse(
            file_path,
            media_type="audio/wav",
            filename=file_name
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Speech generation failed: {str(e)}"
        )


@app.post("/api/tts/generate")
async def generate_tts(request: TTSRequest, background_tasks: BackgroundTasks):
    """
    Advanced TTS generation with multiple engines
    Supports Coqui, gTTS, and Edge TTS
    """
    try:
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tts_{timestamp}.{request.format}"
        output_path = os.path.join(tempfile.gettempdir(), filename)
        
        # Generate audio based on engine
        if request.engine == "coqui":
            if not COQUI_AVAILABLE:
                raise HTTPException(
                    status_code=503,
                    detail="Coqui TTS not available. Install: pip install TTS"
                )
            
            # Use French for Haitian Creole
            lang = "fr" if request.language in ["ht", "hat", "kreyol", "creole"] else request.language
            
            # Generate with Coqui
            coqui_tts.tts_to_file(
                text=request.text,
                file_path=output_path,
                language=lang,
                speaker=request.speaker
            )
            
        elif request.engine in ["gtts", "edge"]:
            if not BASIC_TTS_AVAILABLE:
                raise HTTPException(
                    status_code=503,
                    detail="Basic TTS engines not available"
                )
            
            # Use basic TTS engine
            tts = TTSEngine(engine=request.engine)
            await tts.generate_audio(
                text=request.text,
                language=request.language,
                voice=request.voice,
                output_file=output_path,
                speed=request.speed,
                pitch=request.pitch,
                format=request.format
            )
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported engine: {request.engine}"
            )
        
        # Get file info
        file_size = os.path.getsize(output_path)
        file_size_mb = file_size / (1024 * 1024)
        
        # Estimate duration (if available)
        duration = None
        if BASIC_TTS_AVAILABLE and request.engine != "coqui":
            tts = TTSEngine(engine="gtts")
            duration_seconds = tts.estimate_duration(request.text, request.speed)
            duration = tts.format_duration(duration_seconds)
        
        return TTSResponse(
            success=True,
            message="✅ Audio generated successfully! Odyo kreye avèk siksè!",
            audio_url=f"/download/{filename}",
            filename=filename,
            duration=duration,
            estimated_size=f"{file_size_mb:.2f} MB",
            metadata={
                "engine": request.engine,
                "language": request.language,
                "speed": request.speed if request.engine != "coqui" else 1.0,
                "pitch": request.pitch if request.engine != "coqui" else 0,
                "format": request.format,
                "text_length": len(request.text),
                "word_count": len(request.text.split()),
                "generated_at": datetime.now().isoformat()
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"TTS generation failed: {str(e)}"
        )


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated audio file"""
    file_path = os.path.join(tempfile.gettempdir(), filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Determine media type
    media_type = "audio/mpeg" if filename.endswith(".mp3") else "audio/wav"
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=media_type
    )


# ============================================================
# STARTUP / SHUTDOWN
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Run on startup"""
    print("=" * 60)
    print("🎙️ Faner Studio - Advanced TTS API Server")
    print("=" * 60)
    print(f"✅ Coqui TTS: {COQUI_AVAILABLE}")
    print(f"✅ Basic TTS: {BASIC_TTS_AVAILABLE}")
    
    if BASIC_TTS_AVAILABLE:
        engines = TTSEngine.get_available_engines()
        print(f"✅ Available engines: {len(engines)}")
        for name, desc in engines.items():
            print(f"   - {name}: {desc}")
    
    print("=" * 60)
    print("🚀 Server ready!")
    print("📍 API Docs: http://localhost:8000/docs")
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
        "api_coqui:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

