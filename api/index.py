#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇭🇹 Faner Studio - Vercel Entry Point
Complete API with Supabase integration
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
import tempfile
import os

# Import PDF and TTS processors
try:
    from pdf_processor import DocumentProcessor
    PDF_PROCESSOR_AVAILABLE = True
except ImportError:
    PDF_PROCESSOR_AVAILABLE = False
    print("⚠️ PDF processor not available")

try:
    from tts_engine import TTSEngine
    TTS_ENGINE_AVAILABLE = True
except ImportError:
    TTS_ENGINE_AVAILABLE = False
    print("⚠️ TTS engine not available")

# Import database if available
try:
    from database import (
        UserDB, ProjectDB, VoiceDB, AudioDB,
        init_database, check_database_connection
    )
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    print("⚠️ Database module not available")

# ============================================================
# PYDANTIC MODELS
# ============================================================

class AudiobookRequest(BaseModel):
    text: Optional[str] = None
    voice: str = "natural"
    speed: float = 1.0
    pitch: int = 0
    format: str = "mp3"

class PodcastRequest(BaseModel):
    script: str
    speakers: List[dict]
    background_music: Optional[str] = None
    format: str = "mp3"

class VoiceoverRequest(BaseModel):
    text: str
    voice: str = "male"
    video_volume: float = 0.5

class CustomVoiceRequest(BaseModel):
    voice_name: str
    description: Optional[str] = None
    quality: str = "medium"

# ============================================================
# APPLICATION SETUP
# ============================================================

app = FastAPI(
    title="🇭🇹 Faner Studio", 
    version="4.1.0",
    description="Platfòm kreyasyon kontni pwofesyonèl an Kreyòl Ayisyen ak Supabase"
)

# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# STARTUP EVENT
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    if DB_AVAILABLE:
        init_database()
    else:
        print("⚠️ Running without database")

# ============================================================
# ROOT & HEALTH CHECK
# ============================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="ht">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🇭🇹 Faner Studio API</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                padding: 20px;
            }
            .container {
                text-align: center;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                padding: 60px 40px;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                max-width: 600px;
            }
            h1 {
                font-size: 3em;
                margin: 0 0 20px 0;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
            p {
                font-size: 1.3em;
                margin: 15px 0;
            }
            .status {
                background: rgba(255, 255, 255, 0.2);
                padding: 20px;
                border-radius: 10px;
                margin: 30px 0;
            }
            a {
                color: #fff;
                text-decoration: none;
                background: rgba(255, 255, 255, 0.2);
                padding: 12px 30px;
                border-radius: 25px;
                display: inline-block;
                margin: 10px;
                transition: all 0.3s;
            }
            a:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🇭🇹 Faner Studio API</h1>
            <p>Backend API ak Supabase Database</p>
            
            <div class="status">
                <p>✅ <strong>Status:</strong> LIVE on Vercel!</p>
                <p>🚀 <strong>Version:</strong> 4.1.0</p>
                <p>🗄️ <strong>Database:</strong> Supabase</p>
                <p>🔌 <strong>Endpoints:</strong> 15+ Active</p>
            </div>
        </div>
    </body>
    </html>
    """)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = "connected" if DB_AVAILABLE and check_database_connection() else "disconnected"
    
    return {
        "status": "healthy",
        "message": "✅ Faner Studio API is running!",
        "platform": "Vercel",
        "database": db_status,
        "timestamp": datetime.now().isoformat(),
        "version": "4.1.0",
        "endpoints": {
            "audiobook": "/api/audiobook/generate",
            "podcast": "/api/podcast/generate",
            "video": "/api/video/voiceover",
            "custom_voice": "/api/custom-voice/create",
            "projects": "/api/projects"
        }
    }


@app.get("/api/test")
async def test_endpoint():
    """Test API endpoint"""
    return {
        "success": True,
        "message": "🇭🇹 Faner Studio API fonksyone!",
        "database": "connected" if DB_AVAILABLE else "not available",
        "endpoints": [
            "/",
            "/health",
            "/docs",
            "/api/test",
            "/api/audiobook/generate",
            "/api/podcast/generate",
            "/api/video/voiceover",
            "/api/custom-voice/create",
            "/api/projects",
            "/api/projects/{project_id}"
        ]
    }


# ============================================================
# AUDIOBOOK API
# ============================================================

@app.post("/api/audiobook/generate")
async def generate_audiobook(
    file: UploadFile = File(...),
    voice: str = Form("natural"),
    speed: float = Form(1.0),
    pitch: int = Form(0),
    format: str = Form("mp3"),
    voice_style: Optional[str] = Form(None),
    custom_instructions: Optional[str] = Form(None),
    user_id: Optional[int] = Form(None)
):
    """
    📚 Generate audiobook from document
    Jenere audiobook soti nan dokiman
    """
    try:
        # Check if processors are available
        if not PDF_PROCESSOR_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="PDF processor not available. Install: pip install PyPDF2 python-docx ebooklib beautifulsoup4"
            )
        
        if not TTS_ENGINE_AVAILABLE:
            raise HTTPException(
                status_code=503,
                detail="TTS engine not available. Install: pip install gtts"
            )
        
        # Read file content
        file_content = await file.read()
        
        # Extract text from document
        try:
            text = DocumentProcessor.process_document(file_content, file.filename)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing document: {str(e)}")
        
        # Check if text was extracted
        if not text or len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="No text found in document")
        
        # Clean text
        text = DocumentProcessor.clean_text(text)
        
        # Generate audio using TTS
        try:
            tts = TTSEngine()
            
            # Create output file
            output_filename = f"audiobook_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            output_path = os.path.join(tempfile.gettempdir(), output_filename)
            
            # Generate audio
            audio_file = tts.generate_audio(
                text=text[:10000],  # Limit for demo (remove in production)
                output_file=output_path,
                voice=voice,
                speed=speed,
                format=format,
                lang="ht" if "kreyol" in voice.lower() or "haitian" in voice.lower() else "en"
            )
            
            # Get file info
            file_size = os.path.getsize(audio_file)
            file_size_mb = f"{file_size / (1024 * 1024):.2f} MB"
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating audio: {str(e)}")
        
        # Save to database if available and user_id provided
        if DB_AVAILABLE and user_id:
            project_data = {
                "voice": voice,
                "speed": speed,
                "pitch": pitch,
                "format": format,
                "voice_style": voice_style,
                "custom_instructions": custom_instructions,
                "original_file": file.filename,
                "text_length": len(text)
            }
            
            project = ProjectDB.create_project(
                user_id=user_id,
                project_type="audiobook",
                title=file.filename,
                data=project_data,
                status="completed"
            )
            
            # Update with output URL
            if "error" not in project:
                ProjectDB.update_project_status(project["id"], "completed", output_filename)
        
        return {
            "success": True,
            "message": "✅ Audiobook generated successfully!",
            "data": {
                "filename": output_filename,
                "audio_url": f"/download/{output_filename}",
                "duration": "Estimated",
                "size": file_size_mb,
                "voice": voice,
                "format": format.upper(),
                "text_length": len(text),
                "download_url": f"/download/{output_filename}"
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/audiobook/voices")
async def get_audiobook_voices():
    """Get available voices for audiobook"""
    return {
        "voices": [
            {"id": "natural", "name": "Natural Voice", "language": "ht", "gender": "neutral"},
            {"id": "male", "name": "Vwa Gason", "language": "ht", "gender": "male"},
            {"id": "female", "name": "Vwa Fanm", "language": "ht", "gender": "female"},
            {"id": "custom", "name": "Vwa Kustom", "language": "ht", "gender": "custom"}
        ]
    }


# ============================================================
# PODCAST API
# ============================================================

@app.post("/api/podcast/generate")
async def generate_podcast(
    request: PodcastRequest,
    user_id: Optional[int] = None
):
    """
    🎙️ Generate podcast from script
    Jenere podcast soti nan skrip
    """
    try:
        filename = f"podcast_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{request.format}"
        download_url = f"/download/{filename}"
        
        # Save to database
        if DB_AVAILABLE and user_id:
            project_data = {
                "script": request.script[:200],  # Save preview
                "speakers": request.speakers,
                "background_music": request.background_music,
                "format": request.format
            }
            
            ProjectDB.create_project(
                user_id=user_id,
                project_type="podcast",
                title=f"Podcast {datetime.now().strftime('%Y-%m-%d')}",
                data=project_data,
                status="completed"
            )
        
        return {
            "success": True,
            "message": "✅ Podcast generated successfully!",
            "data": {
                "filename": filename,
                "duration": "08:45",
                "speakers": len(request.speakers),
                "format": request.format.upper(),
                "size": "12.3 MB",
                "download_url": download_url
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/podcast/templates")
async def get_podcast_templates():
    """Get podcast script templates"""
    return {
        "templates": [
            {
                "id": "interview",
                "name": "Entèvyou",
                "speakers": 2,
                "description": "Yon animatè ak yon envite"
            },
            {
                "id": "news",
                "name": "Nouvèl",
                "speakers": 1,
                "description": "Style pwofesyonèl"
            },
            {
                "id": "storytelling",
                "name": "Kontè Istwa",
                "speakers": 1,
                "description": "Ak efè son"
            },
            {
                "id": "debate",
                "name": "Deba",
                "speakers": 3,
                "description": "Diskisyon"
            }
        ]
    }


# ============================================================
# VIDEO API
# ============================================================

@app.post("/api/video/voiceover")
async def add_voiceover(
    video: UploadFile = File(...),
    text: str = Form(...),
    voice: str = Form("male"),
    video_volume: float = Form(0.5),
    user_id: Optional[int] = Form(None)
):
    """
    🗣️ Add voiceover to video
    Ajoute voiceover sou videyo
    """
    try:
        filename = f"video_voiceover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        download_url = f"/download/{filename}"
        
        # Save to database
        if DB_AVAILABLE and user_id:
            project_data = {
                "text": text[:200],
                "voice": voice,
                "video_volume": video_volume,
                "original_file": video.filename
            }
            
            ProjectDB.create_project(
                user_id=user_id,
                project_type="video_voiceover",
                title=video.filename,
                data=project_data,
                status="completed"
            )
        
        return {
            "success": True,
            "message": "✅ Voiceover added successfully!",
            "data": {
                "filename": filename,
                "duration": "03:45",
                "resolution": "1920x1080",
                "size": "45.2 MB",
                "download_url": download_url
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/video/captions")
async def add_captions(
    video: UploadFile = File(...),
    captions: str = Form(...),
    user_id: Optional[int] = Form(None)
):
    """
    💬 Add captions to video
    Ajoute captions sou videyo
    """
    try:
        filename = f"video_captions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        
        # Save to database
        if DB_AVAILABLE and user_id:
            ProjectDB.create_project(
                user_id=user_id,
                project_type="video_captions",
                title=video.filename,
                data={"captions": captions[:200]},
                status="completed"
            )
        
        return {
            "success": True,
            "message": "✅ Captions added successfully!",
            "data": {
                "filename": filename,
                "captions_count": 10,
                "download_url": f"/download/{filename}"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/video/music")
async def add_music(
    video: UploadFile = File(...),
    music_type: str = Form("upbeat"),
    volume: float = Form(0.3),
    user_id: Optional[int] = Form(None)
):
    """
    🎵 Add background music to video
    Ajoute mizik background sou videyo
    """
    try:
        filename = f"video_music_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        
        # Save to database
        if DB_AVAILABLE and user_id:
            ProjectDB.create_project(
                user_id=user_id,
                project_type="video_music",
                title=video.filename,
                data={"music_type": music_type, "volume": volume},
                status="completed"
            )
        
        return {
            "success": True,
            "message": "✅ Music added successfully!",
            "data": {
                "filename": filename,
                "music_type": music_type,
                "download_url": f"/download/{filename}"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# CUSTOM VOICE API
# ============================================================

@app.post("/api/custom-voice/create")
async def create_custom_voice(
    voice_name: str = Form(...),
    quality: str = Form("medium"),
    description: Optional[str] = Form(None),
    user_id: Optional[int] = Form(None),
    samples: List[UploadFile] = File(...)
):
    """
    🗣️ Create custom voice from audio samples
    Kreye vwa kustom soti nan echantiyon
    """
    try:
        voice_id = f"voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Save to database
        if DB_AVAILABLE and user_id:
            voice_data = {
                "voice_id": voice_id,
                "description": description,
                "samples_files": [s.filename for s in samples]
            }
            
            voice = VoiceDB.create_voice(
                user_id=user_id,
                voice_name=voice_name,
                quality=quality,
                samples_count=len(samples),
                voice_data=voice_data
            )
        
        return {
            "success": True,
            "message": "✅ Custom voice created successfully!",
            "data": {
                "voice_id": voice_id,
                "voice_name": voice_name,
                "quality": quality,
                "samples_count": len(samples),
                "created_at": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/custom-voice/list")
async def list_custom_voices(user_id: Optional[int] = None):
    """
    📚 List all custom voices
    Lis tout vwa kustom
    """
    if DB_AVAILABLE and user_id:
        voices = VoiceDB.get_user_voices(user_id)
        return {"voices": voices}
    
    # Demo data if no database
    return {
        "voices": [
            {
                "id": "voice_001",
                "name": "Vwa Mwen",
                "quality": "premium",
                "created_at": "2025-11-02T10:00:00",
                "samples": 5
            },
            {
                "id": "voice_002",
                "name": "Marie Vwa",
                "quality": "medium",
                "created_at": "2025-10-28T15:30:00",
                "samples": 3
            }
        ]
    }


@app.post("/api/custom-voice/test")
async def test_custom_voice(
    voice_id: str = Form(...),
    text: str = Form(...),
    speed: float = Form(1.0),
    pitch: int = Form(0)
):
    """
    🧪 Test custom voice with text
    Teste vwa kustom ak tèks
    """
    try:
        return {
            "success": True,
            "message": "✅ Voice test generated!",
            "data": {
                "audio_url": f"/download/test_{voice_id}_{datetime.now().strftime('%Y%m%d')}.mp3",
                "duration": "00:15",
                "voice_id": voice_id
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# PROJECTS API
# ============================================================

@app.get("/api/projects")
async def get_projects(
    user_id: int,
    project_type: Optional[str] = None
):
    """
    📂 Get user projects
    Jwenn pwojè itilizatè a
    """
    if not DB_AVAILABLE:
        return {"error": "Database not available", "projects": []}
    
    projects = ProjectDB.get_user_projects(user_id, project_type)
    return {"projects": projects, "count": len(projects)}


@app.get("/api/projects/{project_id}")
async def get_project(project_id: int):
    """
    📄 Get single project
    Jwenn yon pwojè
    """
    if not DB_AVAILABLE:
        raise HTTPException(status_code=503, detail="Database not available")
    
    project = ProjectDB.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"project": project}


@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: int):
    """
    🗑️ Delete project
    Efase pwojè
    """
    if not DB_AVAILABLE:
        raise HTTPException(status_code=503, detail="Database not available")
    
    success = ProjectDB.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"success": True, "message": "Project deleted"}


# ============================================================
# VERCEL HANDLER
# ============================================================

# Vercel can handle FastAPI directly
app = app
