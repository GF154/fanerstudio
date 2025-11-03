#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇭🇹 Faner Studio - Unified Platform
Complete creative platform for Haitian Creole content
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
import httpx
import os
import sys
import shutil
import tempfile
from pathlib import Path
from typing import Optional, List
from datetime import datetime
import uuid

# Import database and auth
try:
    from database import get_db, init_db, UserCRUD, ProjectCRUD, VoiceCRUD
    from auth import (
        Token, UserRegister, UserLogin, UserResponse,
        create_access_token, authenticate_user, create_user_account,
        get_current_active_user, get_current_user, optional_auth
    )
    DB_ENABLED = True
except ImportError:
    DB_ENABLED = False
    print("⚠️  Database not available. Running without DB support.")
    # Define dummy models when DB not available
    class UserResponse(BaseModel):
        id: int
        username: str
        email: str
        full_name: Optional[str] = None
        is_active: bool = True
    
    class Token(BaseModel):
        access_token: str
        token_type: str
    
    class UserRegister(BaseModel):
        username: str
        email: str
        password: str
        full_name: Optional[str] = None
    
    class UserLogin(BaseModel):
        username: str
        password: str
    
    # Dummy functions
    def get_db():
        return None
    
    def init_db():
        pass
    
    def get_current_user():
        raise HTTPException(status_code=503, detail="Database not available")
    
    def get_current_active_user():
        raise HTTPException(status_code=503, detail="Database not available")
    
    def optional_auth():
        return None

# Import performance utilities
try:
    from performance import (
        cache, cached, rate_limiter, task_queue, perf_monitor,
        format_bytes, format_duration, get_system_stats
    )
    PERF_ENABLED = True
except ImportError:
    PERF_ENABLED = False
    print("⚠️  Performance utilities not available.")

# ============================================================
# APPLICATION SETUP
# ============================================================

app = FastAPI(
    title="🇭🇹 Faner Studio - Complete Platform", 
    version="3.2.0",
    description="Platfòm konplè pou kreyasyon kontni pwofesyonèl an Kreyòl Ayisyen",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ============================================================
# CORS CONFIGURATION
# ============================================================

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if ALLOWED_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=3600,
)

# ============================================================
# STATIC FILES (Frontend)
# ============================================================

# Mount static files if directory exists
static_path = Path("projet_kreyol_IA/static")
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# ============================================================
# DATA MODELS
# ============================================================

class TranslationRequest(BaseModel):
    text: str
    source: str = "en"
    target: str = "ht"

class TranslationResponse(BaseModel):
    success: bool
    original: str
    translated: Optional[str] = None
    source: str
    target: str
    error: Optional[str] = None

class VoiceCreationRequest(BaseModel):
    voice_name: str = Field(..., description="Nom de la voix personnalisée")
    speaker_name: Optional[str] = Field(None, description="Nom du locuteur")
    text_content: Optional[str] = Field(None, description="Texte prononcé dans l'échantillon")
    language: str = Field("ht", description="Langue de la voix")
    gender: Optional[str] = Field("unknown", description="Genre du locuteur")
    age_range: Optional[str] = Field("adult", description="Tranche d'âge")
    region: Optional[str] = Field("Haiti", description="Région d'origine")
    notes: Optional[str] = Field("", description="Notes additionnelles")
    enhance: bool = Field(True, description="Améliorer la qualité audio")
    denoise: bool = Field(True, description="Réduire le bruit")
    model: str = Field("standard", description="Modèle: standard ou premium")

class VoiceCreationResponse(BaseModel):
    success: bool
    voice_id: Optional[str] = None
    voice_name: str
    status: str
    message: str
    error: Optional[str] = None

class AudiobookRequest(BaseModel):
    voice: str = Field("creole-native", description="Voix à utiliser")
    max_pages: Optional[int] = Field(None, description="Nombre maximum de pages")
    
class PodcastRequest(BaseModel):
    script: str = Field(..., description="Script du podcast")
    voice: str = Field("creole-native", description="Voix à utiliser")
    title: Optional[str] = Field("Mon Podcast", description="Titre du podcast")
    add_intro: bool = Field(True, description="Ajouter une intro")

class AdvancedPodcastRequest(BaseModel):
    script: str = Field(..., description="Advanced script with markers")
    speakers: List[dict] = Field(..., description="List of speakers with configurations")
    title: str = Field("Faner Podcast", description="Podcast title")
    description: Optional[str] = Field("", description="Podcast description")
    add_intro_jingle: bool = Field(True, description="Add intro jingle")
    add_outro_jingle: bool = Field(True, description="Add outro jingle")
    background_music: bool = Field(True, description="Add background music")
    normalize_audio: bool = Field(True, description="Normalize audio levels")
    export_format: str = Field("mp3", description="Export format: mp3, wav, m4a")

# ============================================================
# MAIN ROUTES
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve main interface"""
    
    # Try to serve app_studio_dark.html
    studio_html = Path("projet_kreyol_IA/app_studio_dark.html")
    if studio_html.exists():
        return FileResponse(studio_html)
    
    # Fallback to index.html
    index_html = Path("index.html")
    if index_html.exists():
        return FileResponse(index_html)
    
    # Final fallback: Built-in HTML
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="ht">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🇭🇹 Faner Studio</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                text-align: center;
                max-width: 900px;
            }
            h1 { font-size: 3.5em; margin-bottom: 20px; }
            .tagline { font-size: 1.3em; margin-bottom: 40px; opacity: 0.9; }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 40px 0;
            }
            .feature {
                background: rgba(255,255,255,0.15);
                padding: 30px 20px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                transition: all 0.3s;
            }
            .feature:hover {
                background: rgba(255,255,255,0.25);
                transform: translateY(-5px);
            }
            .feature-icon { font-size: 3em; margin-bottom: 15px; }
            .feature-title { font-size: 1.1em; font-weight: bold; margin-bottom: 8px; }
            .feature-desc { font-size: 0.9em; opacity: 0.8; }
            .links {
                margin-top: 40px;
                display: flex;
                gap: 20px;
                justify-content: center;
                flex-wrap: wrap;
            }
            .link {
                background: rgba(255,255,255,0.2);
                padding: 15px 30px;
                border-radius: 10px;
                text-decoration: none;
                color: white;
                font-weight: bold;
                transition: all 0.3s;
            }
            .link:hover {
                background: rgba(255,255,255,0.3);
                transform: scale(1.05);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🇭🇹 Faner Studio</h1>
            <p class="tagline">Platfòm #1 pou kreyasyon kontni pwofesyonèl an Kreyòl Ayisyen</p>
            
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">🎵</div>
                    <div class="feature-title">Audio Tools</div>
                    <div class="feature-desc">Audiobook, Podcast, TTS, STT</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">🎬</div>
                    <div class="feature-title">Video Tools</div>
                    <div class="feature-desc">Voiceover, Music, Captions</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">🌍</div>
                    <div class="feature-title">Translation</div>
                    <div class="feature-desc">NLLB, PDF, Multi-language</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">🎶</div>
                    <div class="feature-title">Music IA</div>
                    <div class="feature-desc">AI Music Generator</div>
                </div>
            </div>
            
            <div class="links">
                <a href="/docs" class="link">📚 API Documentation</a>
                <a href="/health" class="link">🏥 Health Check</a>
                <a href="/api/status" class="link">📊 System Status</a>
            </div>
        </div>
    </body>
    </html>
    """)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Faner Studio Complete",
        "version": "3.0.0",
        "deployment": "Unified Platform",
        "features": {
            "translation": "active",
            "audio_tools": "active",
            "video_tools": "ready",
            "music_ai": "ready",
            "api": "active",
            "auto_deploy": "active"
        }
    }

@app.get("/api/info")
async def api_info():
    """API information"""
    return {
        "api_name": "Faner Studio Complete API",
        "version": "3.1.0",
        "description": "Complete creative platform for Haitian Creole",
        "features": {
            "audio": ["audiobook", "podcast", "tts", "stt", "url-to-audio", "custom-voice"],
            "video": ["voiceover", "music", "captions", "noise-removal"],
            "translation": ["nllb", "pdf", "batch"],
            "ai": ["music-generator", "script-generator", "voice-cloning"]
        },
        "endpoints": {
            "root": "GET / - Main interface",
            "health": "GET /health - Health check",
            "info": "GET /api/info - API info",
            "status": "GET /api/status - System status",
            "translate": "POST /api/translate - Translation",
            "voice_create": "POST /api/voice/create - Create custom voice",
            "voices": "GET /api/voices - List all voices",
            "audiobook": "POST /api/audiobook - Create audiobook",
            "podcast": "POST /api/podcast - Create podcast",
            "docs": "GET /docs - Interactive docs",
            "redoc": "GET /redoc - Alternative docs"
        },
        "github": "https://github.com/GF154/fanerstudio",
        "live_service": "https://fanerstudio-1.onrender.com"
    }

@app.get("/api/status")
async def status():
    """Detailed system status"""
    import platform
    import sys
    
    return {
        "service": "online",
        "timestamp": "2024-11-02",
        "environment": os.getenv("RENDER", "development"),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "platform": platform.system(),
        "framework": "FastAPI 0.109.0",
        "deployment": {
            "platform": "Render" if os.getenv("RENDER") else "Local",
            "method": "GitHub Actions",
            "auto_deploy": True,
            "branch": "master",
            "unified": True
        },
        "features": {
            "nllb_translation": True,
            "audio_processing": True,
            "video_tools": True,
            "music_ai": True,
            "api_docs": True,
            "health_check": True,
            "cors_configured": True,
            "frontend_served": True
        },
        "resources": {
            "audio_engines": ["mms-tts-hat", "openai", "elevenlabs", "gtts"],
            "stt_engines": ["whisper", "assemblyai"],
            "translation_models": ["nllb-200", "google"],
            "music_models": ["audiocraft", "musicgen"]
        }
    }

# ============================================================
# AUTHENTICATION API
# ============================================================

@app.post("/api/auth/register", response_model=UserResponse)
async def register(user: UserRegister):
    """
    📝 Enskri yon nouvo itilizatè
    
    Register a new user account
    
    - **username**: Unique username
    - **email**: Valid email address
    - **password**: Password (min 8 characters recommended)
    - **full_name**: Full name (optional)
    """
    if not DB_ENABLED:
        raise HTTPException(status_code=503, detail="Database not available")
    
    try:
        new_user = create_user_account(
            username=user.username,
            email=user.email,
            password=user.password,
            full_name=user.full_name
        )
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    🔐 Konekte
    
    Login with username and password
    
    - **username**: Your username
    - **password**: Your password
    
    Returns JWT access token
    """
    if not DB_ENABLED:
        raise HTTPException(status_code=503, detail="Database not available")
    
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_active_user)):
    """
    👤 Jwenn enfòmasyon itilizatè aktyèl
    
    Get current user information
    """
    return current_user

@app.get("/api/auth/projects")
async def get_my_projects(
    limit: int = 50,
    current_user = Depends(get_current_active_user),
    db = Depends(get_db)
):
    """
    📂 Jwenn tout pwojè mwen
    
    Get all user's projects
    """
    projects = ProjectCRUD.get_user_projects(db, user_id=current_user.id, limit=limit)
    return {
        "status": "success",
        "total": len(projects),
        "projects": projects
    }

@app.get("/api/auth/voices")
async def get_my_voices(
    current_user = Depends(get_current_active_user),
    db = Depends(get_db)
):
    """
    🎤 Jwenn tout vwa mwen
    
    Get all user's custom voices
    """
    voices = VoiceCRUD.get_user_voices(db, user_id=current_user.id)
    return {
        "status": "success",
        "total": len(voices),
        "voices": voices
    }

# ============================================================
# PERFORMANCE & MONITORING API
# ============================================================

@app.get("/api/performance/stats")
async def get_performance_stats(endpoint: Optional[str] = None):
    """
    📊 Jwenn estatistik pèfòmans
    
    Get performance statistics
    """
    if not PERF_ENABLED:
        return {"status": "disabled", "message": "Performance monitoring not available"}
    
    return {
        "status": "success",
        "stats": perf_monitor.get_stats(endpoint)
    }

@app.get("/api/performance/cache")
async def get_cache_info():
    """
    💾 Jwenn enfòmasyon cache
    
    Get cache information
    """
    if not PERF_ENABLED:
        return {"status": "disabled", "message": "Cache not available"}
    
    return {
        "status": "success",
        "cache_size": len(cache.cache),
        "items": list(cache.cache.keys())
    }

@app.post("/api/performance/cache/clear")
async def clear_cache():
    """
    🗑️ Efase cache
    
    Clear all cache
    """
    if not PERF_ENABLED:
        return {"status": "disabled", "message": "Cache not available"}
    
    cache.clear()
    return {
        "status": "success",
        "message": "Cache cleared"
    }

@app.get("/api/performance/system")
async def get_system_info():
    """
    🖥️ Jwenn enfòmasyon sistèm
    
    Get system information
    """
    if not PERF_ENABLED:
        return {"status": "disabled", "message": "Performance monitoring not available"}
    
    system_stats = get_system_stats()
    
    return {
        "status": "success",
        "system": system_stats,
        "cache_enabled": PERF_ENABLED,
        "database_enabled": DB_ENABLED
    }

# ============================================================
# TRANSLATION API
# ============================================================

@app.post("/api/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Translate text using NLLB model
    
    - **text**: Text to translate
    - **source**: Source language (en, fr, ht, es)
    - **target**: Target language (en, fr, ht, es)
    """
    try:
        url = "https://api-inference.huggingface.co/models/facebook/nllb-200-distilled-600M"
        headers = {}
        
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        language_codes = {
            "en": "eng_Latn",
            "fr": "fra_Latn",
            "ht": "hat_Latn",
            "es": "spa_Latn",
            "pt": "por_Latn"
        }
        
        src_lang = language_codes.get(request.source, "eng_Latn")
        tgt_lang = language_codes.get(request.target, "hat_Latn")
        
        payload = {
            "inputs": request.text,
            "parameters": {
                "src_lang": src_lang,
                "tgt_lang": tgt_lang
            }
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    translated_text = result[0].get("translation_text", request.text)
                elif isinstance(result, dict):
                    translated_text = result.get("translation_text", request.text)
                else:
                    translated_text = request.text
                
                return TranslationResponse(
                    success=True,
                    original=request.text,
                    translated=translated_text,
                    source=request.source,
                    target=request.target
                )
            
            elif response.status_code == 503:
                return TranslationResponse(
                    success=False,
                    original=request.text,
                    translated=None,
                    source=request.source,
                    target=request.target,
                    error="Model is loading. Please try again in a few seconds."
                )
            
            else:
                return TranslationResponse(
                    success=False,
                    original=request.text,
                    translated=None,
                    source=request.source,
                    target=request.target,
                    error=f"API returned status {response.status_code}"
                )
                
    except httpx.TimeoutException:
        return TranslationResponse(
            success=False,
            original=request.text,
            translated=None,
            source=request.source,
            target=request.target,
            error="Request timeout. Please try again."
        )
    
    except Exception as e:
        return TranslationResponse(
            success=False,
            original=request.text,
            translated=None,
            source=request.source,
            target=request.target,
                    error=str(e)
                )

# ============================================================
# VOICE CREATION API
# ============================================================

@app.post("/api/voice/create", response_model=VoiceCreationResponse)
async def create_custom_voice(
    voice_name: str = Form(...),
    audio_file: UploadFile = File(...),
    speaker_name: Optional[str] = Form(None),
    text_content: Optional[str] = Form(None),
    language: str = Form("ht"),
    gender: str = Form("unknown"),
    age_range: str = Form("adult"),
    region: str = Form("Haiti"),
    notes: str = Form(""),
    enhance: bool = Form(True),
    denoise: bool = Form(True),
    model: str = Form("standard")
):
    """
    🎤 Kreye yon vwa natirèl pèsonalize
    
    Create a custom natural voice from audio sample
    
    - **voice_name**: Nom de la voix (required)
    - **audio_file**: Fichier audio (MP3, WAV, M4A)
    - **speaker_name**: Nom du locuteur (optional)
    - **text_content**: Texte prononcé dans l'audio (optional)
    - **language**: Langue (default: ht)
    - **gender**: Genre du locuteur (male, female, unknown)
    - **age_range**: Tranche d'âge (child, teen, adult, senior)
    - **region**: Région d'origine (default: Haiti)
    - **notes**: Notes additionnelles
    - **enhance**: Améliorer la qualité audio
    - **denoise**: Réduire le bruit de fond
    - **model**: Modèle à utiliser (standard, premium)
    """
    try:
        # Validate file size (max 50MB)
        MAX_SIZE = 50 * 1024 * 1024  # 50MB
        content = await audio_file.read()
        if len(content) > MAX_SIZE:
            return VoiceCreationResponse(
                success=False,
                voice_name=voice_name,
                status="error",
                message="❌ Fichye twò gwo. Maksimòm 50MB.",
                error="File too large"
            )
        
        # Validate file format
        allowed_formats = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']
        file_ext = Path(audio_file.filename).suffix.lower()
        if file_ext not in allowed_formats:
            return VoiceCreationResponse(
                success=False,
                voice_name=voice_name,
                status="error",
                message=f"❌ Fòma fichye pa aksepte. Itilize: {', '.join(allowed_formats)}",
                error="Invalid file format"
            )
        
        # Save audio file temporarily
        temp_dir = Path("temp_uploads")
        temp_dir.mkdir(exist_ok=True)
        
        temp_file = temp_dir / f"{uuid.uuid4()}{file_ext}"
        temp_file.write_bytes(content)
        
        try:
            # Initialize CustomVoiceManager
            sys.path.insert(0, str(Path("projet_kreyol_IA/src")))
            from custom_voice_manager import CustomVoiceManager
            
            voice_manager = CustomVoiceManager(
                voices_dir=Path("projet_kreyol_IA/custom_voices")
            )
            
            # Add voice
            voice_id = voice_manager.add_voice(
                audio_file=temp_file,
                voice_name=voice_name,
                speaker_name=speaker_name or voice_name,
                text_content=text_content or "",
                language=language,
                gender=gender,
                age_range=age_range,
                region=region,
                notes=notes
            )
            
            # Cleanup temp file
            temp_file.unlink()
            
            return VoiceCreationResponse(
                success=True,
                voice_id=voice_id,
                voice_name=voice_name,
                status="created",
                message=f"✅ Vwa '{voice_name}' kreye avèk siksè! ID: {voice_id}"
            )
            
        except Exception as e:
            # Cleanup on error
            if temp_file.exists():
                temp_file.unlink()
            raise e
            
    except Exception as e:
        return VoiceCreationResponse(
            success=False,
            voice_name=voice_name,
            status="error",
            message=f"❌ Erè: {str(e)}",
            error=str(e)
        )

@app.get("/api/voices")
async def get_voices():
    """
    📋 Jwenn lis tout vwa disponib
    
    Get list of all available voices
    """
    try:
        sys.path.insert(0, str(Path("projet_kreyol_IA/src")))
        from custom_voice_manager import CustomVoiceManager
        
        voice_manager = CustomVoiceManager(
            voices_dir=Path("projet_kreyol_IA/custom_voices")
        )
        
        voices = voice_manager.list_voices()
        
        return {
            "status": "success",
            "total": len(voices),
            "voices": voices
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "voices": []
        }

# ============================================================
# AUDIOBOOK API
# ============================================================

@app.post("/api/audiobook")
async def create_audiobook(
    file: UploadFile = File(...),
    voice: str = Form("creole-native"),
    max_pages: Optional[int] = Form(None)
):
    """
    📚 Kreye yon liv odyo (Audiobook)
    
    Create an audiobook from document
    
    - **file**: Document file (PDF, TXT, DOCX, EPUB)
    - **voice**: Voice to use (default: creole-native)
    - **max_pages**: Maximum pages to process (optional)
    """
    try:
        # Validate file format
        allowed_formats = ['.pdf', '.txt', '.docx', '.epub', '.html']
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in allowed_formats:
            raise HTTPException(
                status_code=400,
                detail=f"Format not supported. Use: {', '.join(allowed_formats)}"
            )
        
        # Save uploaded file temporarily
        temp_dir = Path("temp_uploads")
        temp_dir.mkdir(exist_ok=True)
        
        temp_file = temp_dir / f"{uuid.uuid4()}{file_ext}"
        content = await file.read()
        temp_file.write_bytes(content)
        
        try:
            # Import services
            sys.path.insert(0, str(Path("projet_kreyol_IA/app/services")))
            from media_service import MediaService
            
            media_service = MediaService()
            
            # Create audiobook
            result = await media_service.create_audiobook(
                file_path=temp_file,
                voice=voice
            )
            
            # Cleanup
            temp_file.unlink()
            
            return {
                "status": "success",
                "message": "✅ Audiobook kreye avèk siksè!",
                "files": result,
                "voice": voice
            }
            
        except Exception as e:
            # Cleanup on error
            if temp_file.exists():
                temp_file.unlink()
            raise e
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# ============================================================
# PODCAST API
# ============================================================

@app.post("/api/podcast")
async def create_podcast(
    script: str = Form(...),
    voice: str = Form("creole-native"),
    title: str = Form("Mon Podcast"),
    add_intro: bool = Form(True)
):
    """
    🎙️ Kreye yon podcast
    
    Create a podcast from script
    
    - **script**: Podcast script with speaker labels
    - **voice**: Voice to use (default: creole-native)
    - **title**: Podcast title
    - **add_intro**: Add intro music/jingle
    """
    try:
        if not script or len(script.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="Script tro kout. Minimum 10 characters."
            )
        
        # Import services
        sys.path.insert(0, str(Path("projet_kreyol_IA/app/services")))
        from media_service import MediaService
        
        media_service = MediaService()
        
        # Create podcast
        result = await media_service.create_podcast(
            script=script,
            voice=voice,
            title=title,
            add_intro=add_intro
        )
        
        return {
            "status": "success",
            "message": "✅ Podcast kreye avèk siksè!",
            "result": result,
            "title": title,
            "voice": voice
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/podcast/advanced")
async def create_advanced_podcast(request: AdvancedPodcastRequest):
    """
    🎙️ Kreye yon podcast avanse (Veed Fabric style)
    
    Create advanced podcast with multiple speakers, emotions, and effects
    
    - **script**: Advanced script with segment markers [INTRO], [MAIN], [OUTRO]
    - **speakers**: List of speaker configurations (name, voice_id, emotion, etc.)
    - **title**: Podcast title
    - **description**: Podcast description
    - **add_intro_jingle**: Add intro music
    - **add_outro_jingle**: Add outro music
    - **background_music**: Add background music to segments
    - **normalize_audio**: Normalize audio levels
    - **export_format**: Output format (mp3, wav, m4a)
    
    ## Example Script Format:
    ```
    [INTRO - Background: Corporate, Volume: 0.3]
    Host (excited): Welcome to the Faner Podcast!
    [SFX: intro_swoosh]
    
    [MAIN - Background: Calm]
    Host: Today we're discussing AI.
    Guest (professional): That's fascinating!
    [Pause: 2.0]
    
    [OUTRO - Background: Upbeat]
    Host (happy): Thanks for listening!
    [SFX: outro_fade]
    ```
    
    ## Speaker Configuration:
    ```json
    {
      "id": "host",
      "name": "Host",
      "voice_id": "creole-native",
      "gender": "female",
      "emotion": "friendly",
      "pitch": 1.1,
      "speed": 1.0,
      "volume": 1.0
    }
    ```
    """
    try:
        # Import podcast fabric
        import sys
        sys.path.insert(0, str(Path(".")))
        from podcast_fabric import (
            AdvancedPodcastGenerator, Speaker, PodcastConfig,
            SpeakerGender, VoiceEmotion
        )
        
        # Parse speakers
        speakers = []
        for speaker_data in request.speakers:
            speaker = Speaker(
                id=speaker_data.get("id", "speaker1"),
                name=speaker_data.get("name", "Speaker"),
                voice_id=speaker_data.get("voice_id", "creole-native"),
                gender=SpeakerGender(speaker_data.get("gender", "neutral")),
                emotion=VoiceEmotion(speaker_data.get("emotion", "neutral")),
                pitch=speaker_data.get("pitch", 1.0),
                speed=speaker_data.get("speed", 1.0),
                volume=speaker_data.get("volume", 1.0)
            )
            speakers.append(speaker)
        
        # Create config
        config = PodcastConfig(
            title=request.title,
            description=request.description or "Generated with Faner Studio",
            speakers=speakers,
            segments=[],  # Will be parsed from script
            add_intro_jingle=request.add_intro_jingle,
            add_outro_jingle=request.add_outro_jingle,
            normalize_audio=request.normalize_audio,
            export_format=request.export_format
        )
        
        # Generate podcast
        generator = AdvancedPodcastGenerator()
        result = await generator.generate_from_script(
            script=request.script,
            speakers=speakers,
            config=config
        )
        
        return {
            "status": "success",
            "message": "✅ Advanced podcast kreye avèk siksè!",
            "result": result,
            "title": request.title,
            "speakers_count": len(speakers),
            "segments_count": len(result.get("segments", [])),
            "features": {
                "multi_speaker": len(speakers) > 1,
                "emotion_control": True,
                "background_music": request.background_music,
                "sound_effects": True,
                "professional_editing": True
            }
        }
        
    except HTTPException:
        raise
    except ImportError as e:
        raise HTTPException(
            status_code=500, 
            detail=f"podcast_fabric module not available: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/podcast/templates")
async def get_podcast_templates():
    """
    📝 Jwenn modèl podcast
    
    Get podcast script templates
    """
    try:
        from podcast_fabric import PodcastTemplates
        
        return {
            "status": "success",
            "templates": {
                "interview": {
                    "name": "Interview Podcast",
                    "description": "Template for interview-style podcasts",
                    "script": PodcastTemplates.interview_template()
                },
                "news": {
                    "name": "News Podcast",
                    "description": "Template for news podcasts",
                    "script": PodcastTemplates.news_template()
                },
                "storytelling": {
                    "name": "Storytelling Podcast",
                    "description": "Template for storytelling podcasts",
                    "script": PodcastTemplates.storytelling_template()
                }
            }
        }
    except ImportError:
        return {
            "status": "error",
            "message": "Templates not available"
        }

# ============================================================
# ERROR HANDLERS
# ============================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Page not found",
            "message": "The requested endpoint does not exist",
            "available_endpoints": [
                "/",
                "/health",
                "/api/info",
                "/api/status",
                "/api/translate",
                "/docs",
                "/redoc"
            ],
            "tip": "Visit /docs for interactive API documentation"
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "status": "Please try again later or contact support"
        }
    )

# ============================================================
# STARTUP & SHUTDOWN
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Actions on startup"""
    print("="*60)
    print("🇭🇹 Faner Studio - Complete Platform")
    print("="*60)
    print("✅ Service: ONLINE")
    print("✅ Version: 3.2.0")
    print("✅ Mode: Production Ready")
    print("✅ Features: ALL ACTIVE")
    print("✅ APIs: Voice, Audiobook, Podcast, Auth")
    if DB_ENABLED:
        print("✅ Database: SQLite (Enabled)")
        init_db()  # Initialize database tables
    else:
        print("⚠️  Database: Disabled")
    if PERF_ENABLED:
        print("✅ Performance: Monitoring (Enabled)")
    else:
        print("⚠️  Performance: Disabled")
    print("="*60)

@app.on_event("shutdown")
async def shutdown_event():
    """Actions on shutdown"""
    print("🔴 Faner Studio shutting down...")

# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
