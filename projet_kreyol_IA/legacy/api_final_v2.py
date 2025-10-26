#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇭🇹 Kreyòl IA - API Backend V2 (Production-Ready)
Professional-grade API with security, monitoring, and robustness
"""

import os
import uuid
import logging
import tempfile
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import pypdf

# Import our new modules
from src.app_config import get_config, validate_production_config
from src.file_validator import PDFValidator, validate_file_upload
from src.metrics import (
    PrometheusMiddleware, initialize_app_info, 
    metrics_endpoint, record_pdf_pages
)
from src.health import HealthChecker, health_endpoint, liveness_endpoint, readiness_endpoint
from src.rate_limiter import RateLimiter

# Import existing modules
from traduire_texte import traduire_avec_progress
from generer_audio_huggingface import generer_audio_creole
from podcast_creator import PodcastCreator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('KreyolAI.API')

# Load configuration
config = get_config()

# Validate production configuration
if config.is_production:
    try:
        validate_production_config()
        logger.info("✅ Production configuration validated")
    except ValueError as e:
        logger.error(f"❌ Production configuration invalid: {e}")
        raise


# ============================================================
# APPLICATION LIFECYCLE
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown"""
    # Startup
    logger.info("🚀 Starting Kreyòl IA API v2...")
    
    # Initialize metrics
    if config.prometheus_enabled:
        initialize_app_info(
            app_name=config.app_name,
            version=config.app_version,
            environment=config.app_env
        )
        logger.info("📊 Prometheus metrics initialized")
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    logger.info(f"📁 Output directory: {OUTPUT_DIR}")
    
    logger.info("✅ Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Kreyòl IA API...")
    logger.info("✅ Application shutdown complete")


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title=config.app_name,
    description="Professional AI-powered Haitian Creole content creation platform",
    version=config.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# ============================================================
# MIDDLEWARE
# ============================================================

# CORS (with proper configuration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allowed_origins,  # No more wildcard!
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Prometheus Metrics
if config.prometheus_enabled:
    app.add_middleware(PrometheusMiddleware)
    logger.info("📊 Prometheus middleware enabled")

# Request ID Middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add unique request ID to each request"""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    
    return response

# ============================================================
# GLOBALS
# ============================================================

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Initialize services
podcast_creator = PodcastCreator()
health_checker = HealthChecker(app_version=config.app_version, environment=config.app_env)
pdf_validator = PDFValidator(
    max_size_mb=config.max_upload_size_mb,
    max_pages=config.max_pdf_pages
)

# Rate limiter (if enabled)
rate_limiter = None
if config.rate_limiting_enabled:
    rate_limiter = RateLimiter()
    logger.info("🚦 Rate limiting enabled")


# ============================================================
# MONITORING ENDPOINTS
# ============================================================

@app.get("/metrics")
async def get_metrics():
    """📊 Prometheus metrics endpoint"""
    if not config.prometheus_enabled:
        raise HTTPException(404, "Metrics disabled")
    return await metrics_endpoint()


@app.get("/health")
async def health_check(detailed: bool = False):
    """
    🏥 Health check endpoint
    
    Query params:
    - detailed: Include detailed component checks
    """
    health, status_code = await health_endpoint(health_checker, detailed=detailed)
    return JSONResponse(content=health.dict(), status_code=status_code)


@app.get("/health/live")
async def liveness():
    """🟢 Kubernetes liveness probe"""
    return await liveness_endpoint(health_checker)


@app.get("/health/ready")
async def readiness():
    """🟢 Kubernetes readiness probe"""
    result, status_code = await readiness_endpoint(health_checker)
    return JSONResponse(content=result, status_code=status_code)


# ============================================================
# AUDIO ENDPOINTS
# ============================================================

@app.post("/api/audiobook")
async def create_audiobook(
    request: Request,
    file: UploadFile = File(...),
    voice: str = Form("creole-native")
):
    """
    📚 Create Haitian Creole audiobook from document
    
    Supports: .pdf, .txt
    """
    request_id = request.state.request_id
    logger.info(f"[{request_id}] Audiobook request: {file.filename}")
    
    try:
        # Validate file
        if file.filename.endswith('.pdf'):
            content, file_hash, page_count = await pdf_validator.validate_pdf(file)
            record_pdf_pages(page_count)
            
            # Extract text
            import io
            reader = pypdf.PdfReader(io.BytesIO(content))
            text = "\n".join(page.extract_text() for page in reader.pages)
            
        elif file.filename.endswith('.txt'):
            content, file_hash = await validate_file_upload(
                file,
                allowed_extensions=['.txt'],
                max_size_mb=config.max_upload_size_mb
            )
            text = content.decode('utf-8')
            
        else:
            raise HTTPException(400, "Unsupported file format. Use .pdf or .txt")
        
        # Check text length
        if len(text) > config.max_audio_chars:
            raise HTTPException(
                413,
                f"Text too long: {len(text)} chars (max: {config.max_audio_chars})"
            )
        
        # Translate to Creole
        logger.info(f"[{request_id}] Translating {len(text)} characters...")
        texte_traduit = traduire_avec_progress(text, langue_cible='ht')
        
        # Create output directory
        nom_base = Path(file.filename).stem
        output_base = OUTPUT_DIR / f"{nom_base}_{file_hash[:8]}"
        output_base.mkdir(parents=True, exist_ok=True)
        
        # Save translation
        texte_path = output_base / f"{nom_base}_kreyol.txt"
        texte_path.write_text(texte_traduit, encoding='utf-8')
        
        # Generate audio
        logger.info(f"[{request_id}] Generating audio...")
        audio_path = output_base / f"{nom_base}_audio.mp3"
        generer_audio_creole(texte_traduit, audio_path)
        
        logger.info(f"[{request_id}] ✅ Audiobook created successfully")
        
        return JSONResponse({
            "status": "success",
            "request_id": request_id,
            "files": {
                "translation": f"/output/{output_base.name}/{texte_path.name}",
                "audio": f"/output/{output_base.name}/{audio_path.name}"
            },
            "stats": {
                "original_chars": len(text),
                "translated_chars": len(texte_traduit),
                "original_words": len(text.split()),
                "translated_words": len(texte_traduit.split())
            }
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[{request_id}] ❌ Audiobook error: {e}", exc_info=True)
        raise HTTPException(
            500,
            detail={
                "error": "Audiobook creation failed",
                "message": str(e),
                "request_id": request_id
            }
        )


@app.post("/api/podcast")
async def create_podcast(
    request: Request,
    script: str = Form(...),
    format: str = Form("conversation"),
    voices: str = Form("auto")
):
    """
    🎙️ Create multi-voice podcast
    
    Format: conversation | interview
    """
    request_id = request.state.request_id
    logger.info(f"[{request_id}] Podcast request: format={format}")
    
    try:
        # Create temp script file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as tmp_script:
            tmp_script.write(script)
            tmp_script_path = Path(tmp_script.name)
        
        # Output path
        podcast_id = str(uuid.uuid4())[:8]
        nom_base = f"podcast_{podcast_id}"
        output_base = OUTPUT_DIR / nom_base
        output_base.mkdir(parents=True, exist_ok=True)
        podcast_output_path = output_base / f"{nom_base}.mp3"
        
        # Create podcast
        logger.info(f"[{request_id}] Creating podcast...")
        podcast_creator.create_podcast(str(tmp_script_path), podcast_output_path)
        
        # Cleanup
        tmp_script_path.unlink()
        
        logger.info(f"[{request_id}] ✅ Podcast created successfully")
        
        return JSONResponse({
            "status": "success",
            "request_id": request_id,
            "files": {
                "audio": f"/output/{nom_base}/{podcast_output_path.name}"
            },
            "stats": {
                "segments": podcast_creator.last_stats.get("segments", 0),
                "speakers": podcast_creator.last_stats.get("speakers", 0),
                "duration_estimate": podcast_creator.last_stats.get("duration_sec", 0)
            }
        })
        
    except Exception as e:
        logger.error(f"[{request_id}] ❌ Podcast error: {e}", exc_info=True)
        raise HTTPException(
            500,
            detail={
                "error": "Podcast creation failed",
                "message": str(e),
                "request_id": request_id
            }
        )


# ============================================================
# TRANSLATION ENDPOINTS
# ============================================================

@app.post("/api/translate")
async def translate_text(
    request: Request,
    text: str = Form(...),
    target_lang: str = Form("ht")
):
    """
    🌍 Translate text to Haitian Creole
    
    Uses Google Translate for high-quality translation
    """
    request_id = request.state.request_id
    logger.info(f"[{request_id}] Translation request: {len(text)} chars")
    
    try:
        texte_traduit = traduire_avec_progress(text, langue_cible=target_lang)
        
        return JSONResponse({
            "status": "success",
            "request_id": request_id,
            "translation": texte_traduit,
            "stats": {
                "original_length": len(text),
                "translated_length": len(texte_traduit),
                "original_words": len(text.split()),
                "translated_words": len(texte_traduit.split())
            }
        })
        
    except Exception as e:
        logger.error(f"[{request_id}] ❌ Translation error: {e}", exc_info=True)
        raise HTTPException(
            500,
            detail={
                "error": "Translation failed",
                "message": str(e),
                "request_id": request_id
            }
        )


@app.post("/api/pdf-translate")
async def translate_pdf(
    request: Request,
    file: UploadFile = File(...),
    generate_audio: bool = Form(True)
):
    """
    📄 Translate PDF to Haitian Creole
    
    Optional: Generate audiobook from translation
    """
    request_id = request.state.request_id
    logger.info(f"[{request_id}] PDF translation request: {file.filename}")
    
    try:
        # Validate PDF
        content, file_hash, page_count = await pdf_validator.validate_pdf(file)
        record_pdf_pages(page_count)
        
        # Extract text
        import io
        reader = pypdf.PdfReader(io.BytesIO(content))
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # Translate
        logger.info(f"[{request_id}] Translating {page_count} pages...")
        texte_traduit = traduire_avec_progress(text, langue_cible='ht')
        
        # Create output
        nom_base = Path(file.filename).stem
        output_base = OUTPUT_DIR / f"{nom_base}_{file_hash[:8]}"
        output_base.mkdir(parents=True, exist_ok=True)
        
        # Save translation
        texte_path = output_base / f"{nom_base}_kreyol.txt"
        texte_path.write_text(texte_traduit, encoding='utf-8')
        
        audio_file_url = None
        if generate_audio:
            if len(texte_traduit) > config.max_audio_chars:
                logger.warning(f"[{request_id}] Text too long for audio: {len(texte_traduit)} chars")
            else:
                logger.info(f"[{request_id}] Generating audio...")
                audio_path = output_base / f"{nom_base}_audio.mp3"
                generer_audio_creole(texte_traduit, audio_path)
                audio_file_url = f"/output/{output_base.name}/{audio_path.name}"
        
        logger.info(f"[{request_id}] ✅ PDF translated successfully")
        
        return JSONResponse({
            "status": "success",
            "request_id": request_id,
            "files": {
                "translation": f"/output/{output_base.name}/{texte_path.name}",
                "audio": audio_file_url
            },
            "stats": {
                "pages": page_count,
                "chars": len(text),
                "translated_chars": len(texte_traduit)
            }
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[{request_id}] ❌ PDF translation error: {e}", exc_info=True)
        raise HTTPException(
            500,
            detail={
                "error": "PDF translation failed",
                "message": str(e),
                "request_id": request_id
            }
        )


# ============================================================
# PROJECT MANAGEMENT
# ============================================================

@app.get("/api/projects")
async def list_projects():
    """📂 List all user projects"""
    projects = []
    for project_dir in OUTPUT_DIR.iterdir():
        if project_dir.is_dir():
            files = list(project_dir.glob("*"))
            projects.append({
                "name": project_dir.name,
                "files": [f.name for f in files],
                "created": project_dir.stat().st_ctime,
                "file_count": len(files)
            })
    
    # Sort by creation date
    projects.sort(key=lambda x: x['created'], reverse=True)
    
    return JSONResponse({"projects": projects})


# ============================================================
# STATIC FILES
# ============================================================

# Serve output files
app.mount("/output", StaticFiles(directory="output"), name="output")

@app.get("/")
async def serve_app():
    """Serve main application"""
    return FileResponse("app_studio_dark.html")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print("🇭🇹 KREYÒL IA - PRODUCTION API V2")
    print("=" * 70)
    print()
    print(f"🌍 Environment: {config.app_env}")
    print(f"🏷️  Version: {config.app_version}")
    print(f"🔒 Debug: {'ON' if config.debug else 'OFF'}")
    print(f"🌐 Port: {config.port}")
    print(f"📍 CORS Origins: {', '.join(config.allowed_origins)}")
    print()
    print("✨ Features:")
    print("   ✅ Secure file upload validation")
    print("   ✅ CORS properly configured")
    print(f"   {'✅' if config.rate_limiting_enabled else '❌'} Rate limiting")
    print(f"   {'✅' if config.prometheus_enabled else '❌'} Prometheus metrics")
    print("   ✅ Health checks (live/ready)")
    print("   ✅ Request ID tracking")
    print("   ✅ Professional error handling")
    print()
    print("📚 Endpoints:")
    print(f"   📱 Web App:     http://localhost:{config.port}/")
    print(f"   📖 API Docs:    http://localhost:{config.port}/docs")
    print(f"   🏥 Health:      http://localhost:{config.port}/health")
    print(f"   📊 Metrics:     http://localhost:{config.port}/metrics")
    print("=" * 70)
    print(f"\n🚀 Starting server on {config.host}:{config.port}...\n")
    
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level=config.log_level.lower()
    )

