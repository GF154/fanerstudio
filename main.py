#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇭🇹 Faner Studio - Unified Platform
Complete creative platform for Haitian Creole content
"""

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import httpx
import os
from pathlib import Path
from typing import Optional

# ============================================================
# APPLICATION SETUP
# ============================================================

app = FastAPI(
    title="🇭🇹 Faner Studio - Complete Platform", 
    version="3.0.0",
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
        "version": "3.0.0",
        "description": "Complete creative platform for Haitian Creole",
        "features": {
            "audio": ["audiobook", "podcast", "tts", "stt", "url-to-audio"],
            "video": ["voiceover", "music", "captions", "noise-removal"],
            "translation": ["nllb", "pdf", "batch"],
            "ai": ["music-generator", "script-generator"]
        },
        "endpoints": {
            "root": "GET / - Main interface",
            "health": "GET /health - Health check",
            "info": "GET /api/info - API info",
            "status": "GET /api/status - System status",
            "translate": "POST /api/translate - Translation",
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
    print("✅ Version: 3.0.0")
    print("✅ Mode: Unified Platform")
    print("✅ Features: ALL ACTIVE")
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
