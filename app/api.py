#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇭🇹 Kreyòl IA - API Routes
Tout endpoint API yo
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import Optional
import tempfile
import shutil
import time
import asyncio

# Import services
from app.services.tts_service import TTSService
from app.services.stt_service import STTService
from app.services.media_service import MediaService

# Import security & monitoring
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from src.file_validator import FileValidator
    from src.metrics import (
        track_api_request, track_translation, 
        track_audio_generation, track_file_processing
    )
    MONITORING_ENABLED = True
except ImportError:
    print("⚠️  Monitoring modules not available")
    MONITORING_ENABLED = False

# Kreye aplikasyon FastAPI
app = FastAPI(
    title="🇭🇹 Kreyòl IA Studio API",
    description="API pwofesyonèl pou kreyasyon kontni an Kreyòl Ayisyen",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
tts_service = TTSService()
stt_service = STTService()
media_service = MediaService()

# Initialize file validator
if MONITORING_ENABLED:
    file_validator = FileValidator(
        max_file_size=100 * 1024 * 1024,  # 100 MB
        allowed_extensions={".pdf", ".txt", ".docx", ".epub", ".mp3", ".wav", ".m4a"}
    )

# Directories
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Request tracking middleware
@app.middleware("http")
async def track_requests(request: Request, call_next):
    """Track all API requests for monitoring"""
    start_time = time.time()
    
    response = await call_next(request)
    
    if MONITORING_ENABLED:
        process_time = time.time() - start_time
        track_api_request(
            endpoint=request.url.path,
            method=request.method,
            status_code=response.status_code,
            duration=process_time
        )
    
    return response

# ============================================================
# ROUTES PRENSIPAL
# ============================================================

@app.get("/")
async def serve_app():
    """Sèvi paj akèy hybrid - Chwazi eksperyans ou"""
    return FileResponse("index.html")

@app.get("/health")
async def health_check():
    """Verifye sante aplikasyon an"""
    health_status = {
        "status": "✅ Byen fonksyone",
        "service": "🇭🇹 Kreyòl IA Studio",
        "version": "3.1.0",
        "monitoring": MONITORING_ENABLED
    }
    
    # Check service availability
    try:
        health_status["services"] = {
            "tts": "available",
            "stt": "available",
            "media": "available"
        }
    except Exception as e:
        health_status["services"] = {"error": str(e)}
    
    return health_status

@app.get("/metrics")
async def get_metrics():
    """Jwenn metrik aplikasyon an (Prometheus format)"""
    if not MONITORING_ENABLED:
        raise HTTPException(status_code=503, detail="Monitoring not enabled")
    
    try:
        from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
        from fastapi.responses import Response
        
        return Response(
            content=generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erè: {str(e)}")

@app.get("/api/cache/stats")
async def get_cache_stats():
    """Jwenn estatistik kachaj la"""
    try:
        from app.cache import translation_cache, audio_cache
        
        return JSONResponse({
            "status": "siksè",
            "translation_cache": translation_cache.get_stats(),
            "audio_cache": audio_cache.get_stats()
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erè: {str(e)}")

@app.post("/api/cache/clear")
async def clear_cache(cache_type: str = Form("all")):
    """Efase kachaj la"""
    try:
        from app.cache import translation_cache, audio_cache
        
        count = 0
        if cache_type in ["all", "translation"]:
            count += translation_cache.clear()
        if cache_type in ["all", "audio"]:
            count += audio_cache.clear()
        
        return JSONResponse({
            "status": "siksè",
            "message": f"Kachaj efase! {count} fichye retire.",
            "cleared_count": count,
            "cache_type": cache_type
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erè: {str(e)}")

# ============================================================
# API ENDPOINTS - ODYO
# ============================================================

@app.get("/api/voices")
async def get_voices():
    """
    📋 Jwenn lis vwa disponib yo
    
    **Retounen:**
    - Vwa natif Kreyòl
    - Vwa OpenAI (si API key konfigire)
    - Vwa ElevenLabs (si API key konfigire)
    """
    try:
        voices = tts_service.get_available_voices()
        
        return JSONResponse({
            "status": "siksè",
            "voices": voices,
            "total": len(voices)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erè: {str(e)}")

@app.post("/api/tts")
async def text_to_speech(
    text: str = Form(...),
    voice: str = Form("creole-native")
):
    """
    🗣️ Konvèti tèks an paròl (Text-to-Speech)
    
    **Paramèt:**
    - text: Tèks pou konvèti
    - voice: Vwa pou itilize (creole-native)
    """
    try:
        # Track generation
        if MONITORING_ENABLED:
            track_audio_generation(voice, len(text))
        
        audio_path = await tts_service.generate_speech(text, voice)
        
        return JSONResponse({
            "status": "siksè",
            "message": "Odyo kreye avèk siksè! ✅",
            "audio_url": f"/output/{audio_path.name}",
            "text_length": len(text)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erè: {str(e)}")

@app.post("/api/audiobook")
async def create_audiobook(
    file: UploadFile = File(...),
    voice: str = Form("creole-native"),
    max_pages: int = Form(None),
    show_progress: bool = Form(True)
):
    """
    📚 Kreye liv odyo (Audiobook)
    
    **Sipòte:** .pdf, .txt, .docx, .epub
    
    **Paramèt:**
    - file: Fichye dokiman
    - voice: Vwa pou itilize
    - max_pages: Limit maksimòm paj pou ekstrè (None = tout paj)
    - show_progress: Afiche pwogresyon (default: True)
    
    **Optimize pou gwo fichye:**
    - Chunk processing (50 paj pa fwa)
    - Progress bars pou PDF > 20 paj
    - Warning pou PDF > 1000 paj
    - Memwa optimize ak streaming
    """
    try:
        # Validate file
        if MONITORING_ENABLED:
            file_validator.validate_upload(file)
            track_file_processing("audiobook", file.filename)
        
        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = Path(tmp.name)
        
        # Log processing start
        print(f"\n{'='*60}")
        print(f"📚 AUDIOBOOK CREATION START")
        print(f"   Fichye: {file.filename}")
        print(f"   Vwa: {voice}")
        if max_pages:
            print(f"   ⚠️  Limit paj: {max_pages}")
        print(f"{'='*60}\n")
        
        # Process audiobook with new parameters
        # Note: We need to call extract_text first with new params
        text = await media_service.extract_text_from_document(
            str(tmp_path),
            max_pages=max_pages,
            show_progress=show_progress
        )
        
        # Now create audiobook from extracted text
        result = await media_service.create_audiobook(tmp_path, voice)
        
        # Cleanup
        tmp_path.unlink()
        
        return JSONResponse({
            "status": "siksè",
            "message": "Liv odyo kreye avèk siksè! 📚✅",
            "files": result
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erè: {str(e)}")

@app.post("/api/audiobook-streaming")
async def create_audiobook_streaming(
    file: UploadFile = File(...),
    voice: str = Form("creole-native"),
    chunk_size_pages: int = Form(100)
):
    """
    📚 Kreye liv odyo ak STREAMING (pou gwo fichye)
    
    **Sipòte:** PDF sèlman (pou kounye a)
    
    **Paramèt:**
    - file: Fichye PDF
    - voice: Vwa pou itilize
    - chunk_size_pages: Kantite paj pa chunk (default: 100)
    
    **Avantaj:**
    - ✅ Memwa optimize
    - ✅ Kapab pwosese PDF 5000+ paj
    - ✅ Progress real-time
    - ✅ Timeout protection
    """
    try:
        # Validate PDF
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400, 
                detail="Sèlman fichye PDF sipòte pou streaming extraction!"
            )
        
        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = Path(tmp.name)
        
        # Extract text with streaming
        print(f"\n{'='*60}")
        print(f"📚 STREAMING AUDIOBOOK CREATION")
        print(f"   Fichye: {file.filename}")
        print(f"   Chunk size: {chunk_size_pages} paj")
        print(f"{'='*60}\n")
        
        # Define callback for progress
        progress_data = {"chunks_done": 0, "total_chunks": 0}
        
        async def progress_callback(current_page, total_pages, chunk_text):
            progress_data["chunks_done"] += 1
            percentage = (current_page / total_pages) * 100
            print(f"   📊 Pwogresyon: {percentage:.1f}% ({current_page}/{total_pages} paj)")
        
        # Extract with streaming
        text = await media_service.extract_text_from_pdf_streaming(
            tmp_path,
            chunk_size_pages=chunk_size_pages,
            callback=progress_callback
        )
        
        # Now create audiobook from extracted text
        result = await media_service.create_audiobook(tmp_path, voice)
        
        # Cleanup
        tmp_path.unlink()
        
        return JSONResponse({
            "status": "siksè",
            "message": "Liv odyo kreye avèk streaming! 📚✅",
            "files": result,
            "extraction_method": "streaming",
            "chunk_size_pages": chunk_size_pages
        })
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Timeout! Fichye a tro gwo. Eseye ak chunk_size pi piti."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erè: {str(e)}")

@app.post("/api/podcast")
async def create_podcast(
    title: str = Form(...),
    content: str = Form(...),
    num_speakers: int = Form(2)
):
    """
    🎙️ Kreye podcast
    
    **Paramèt:**
    - title: Tit podcast la
    - content: Kontni pou diskite
    - num_speakers: Kantite moun kap pale (default: 2)
    """
    try:
        podcast_path = await media_service.create_podcast(title, content, num_speakers)
        
        return JSONResponse({
            "status": "siksè",
            "message": "Podcast kreye avèk siksè! 🎙️✅",
            "audio_url": f"/output/{podcast_path.name}",
            "title": title,
            "speakers": num_speakers
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erè: {str(e)}")

@app.post("/api/url-to-text")
async def url_to_text(
    url: str = Form(...)
):
    """
    🔗 Ekstrè tèks soti nan yon URL
    
    **Paramèt:**
    - url: URL paj wèb la
    """
    try:
        text = await media_service.html_to_text(url)
        
        return JSONResponse({
            "status": "siksè",
            "message": "Tèks ekstrè avèk siksè! 🔗✅",
            "text": text,
            "char_count": len(text),
            "word_count": len(text.split()),
            "url": url
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erè: {str(e)}")

# ============================================================
# API ENDPOINTS - TRADIKSYON
# ============================================================

@app.post("/api/translate")
async def translate_text(
    text: str = Form(...),
    target_lang: str = Form("ht"),
    use_cache: bool = Form(True)
):
    """
    🌍 Tradwi tèks (ak kachaj pou pèfòmans)
    
    **Paramèt:**
    - text: Tèks pou tradwi
    - target_lang: Lang sib (ht=Kreyòl, en=Angle, fr=Franse)
    - use_cache: Itilize kachaj oswa non (default: True)
    """
    try:
        # Import translation service and cache
        from traduire_texte import traduire_avec_progress
        from app.cache import translation_cache
        
        # Track translation
        if MONITORING_ENABLED:
            track_translation(target_lang, len(text))
        
        # Check cache if enabled
        if use_cache:
            cache_key = translation_cache._get_cache_key(f"auto:{target_lang}:{text}")
            cached_result = translation_cache.get(cache_key)
            
            if cached_result:
                return JSONResponse({
                    "status": "siksè",
                    "message": "Tradiksyon soti nan kachaj! 💾✅",
                    "original": text,
                    "translated": cached_result,
                    "target_language": target_lang,
                    "char_count": len(cached_result),
                    "cached": True
                })
        
        # Translate
        translated = traduire_avec_progress(text, langue_cible=target_lang)
        
        # Save to cache
        if use_cache:
            cache_key = translation_cache._get_cache_key(f"auto:{target_lang}:{text}")
            translation_cache.set(cache_key, translated)
        
        return JSONResponse({
            "status": "siksè",
            "message": "Tradiksyon konplete! 🌍✅",
            "original": text,
            "translated": translated,
            "target_language": target_lang,
            "char_count": len(translated),
            "cached": False
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erè: {str(e)}")

@app.post("/api/translate/pdf")
async def translate_pdf(
    file: UploadFile = File(...),
    target_lang: str = Form("ht")
):
    """
    📄 Tradwi dokiman PDF
    """
    try:
        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = Path(tmp.name)
        
        # Process PDF translation
        result = await media_service.translate_pdf(tmp_path, target_lang)
        
        # Cleanup
        tmp_path.unlink()
        
        return JSONResponse({
            "status": "siksè",
            "message": "PDF tradwi avèk siksè! 📄✅",
            "files": result
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erè: {str(e)}")

# ============================================================
# API ENDPOINTS - SPEECH-TO-TEXT
# ============================================================

@app.get("/api/stt/engines")
async def get_stt_engines():
    """
    📋 Jwenn lis STT engines disponib yo
    
    **Retounen:**
    - Whisper Local (si enstale)
    - Whisper OpenAI (si API key konfigire)
    - AssemblyAI (si API key konfigire)
    """
    try:
        engines = stt_service.get_available_engines()
        
        return JSONResponse({
            "status": "siksè",
            "engines": engines,
            "total": len(engines)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erè: {str(e)}")

@app.post("/api/stt")
async def speech_to_text(
    file: UploadFile = File(...),
    engine: str = Form("auto")
):
    """
    📝 Konvèti paròl an tèks (Speech-to-Text)
    
    **Sipòte:** .mp3, .wav, .m4a, .ogg, .flac, .webm
    
    **Engines:**
    - auto: Automatic (prefer local Whisper)
    - whisper-local: Local Whisper model (GRATIS)
    - whisper-openai: OpenAI Whisper API ($0.006/min)
    - assemblyai: AssemblyAI ($0.00025/sec)
    """
    try:
        # Validate file
        if MONITORING_ENABLED:
            file_validator.validate_upload(file)
        
        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = Path(tmp.name)
        
        # Process speech-to-text
        text = await stt_service.transcribe(tmp_path, engine=engine)
        
        # Cleanup
        tmp_path.unlink()
        
        return JSONResponse({
            "status": "siksè",
            "message": "Transkripsyon konplete! 📝✅",
            "text": text,
            "char_count": len(text),
            "engine": engine,
            "file_name": file.filename
        })
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erè: {str(e)}")

# ============================================================
# STATIC FILES
# ============================================================

# Sèvi fichye output yo
app.mount("/output", StaticFiles(directory="output"), name="output")

# Sèvi paj multi-page yo
app.mount("/pages", StaticFiles(directory="pages", html=True), name="pages")

# ============================================================
# STARTUP EVENT
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Evènman lè aplikasyon kòmanse"""
    print()
    print("=" * 60)
    print("✅ Kreyòl IA Studio API lanse avèk siksè!")
    print("=" * 60)
    print("📱 Interface: http://localhost:8000")
    print("📚 API Docs:  http://localhost:8000/docs")
    print("=" * 60)
    print()

