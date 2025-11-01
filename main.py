#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇭🇹 Faner Studio - API Principal
Version optimisée pour Render Free Tier avec déploiement automatique
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from typing import Optional

# Créer l'application FastAPI
app = FastAPI(
    title="🇭🇹 Faner Studio API", 
    version="2.0.0",
    description="Platfòm pwofesyonèl pou kreyasyon kontni an Kreyòl Ayisyen",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS - More restrictive for production
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if ALLOWED_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=3600,
)

# Modèles de données
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
# ROUTES PRINCIPALES
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve l'interface HTML principale"""
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    
    if os.path.exists(html_path):
        return FileResponse(html_path)
    
    # Fallback si index.html n'existe pas
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="ht">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🇭🇹 Faner Studio</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
                padding: 20px;
            }
            .container {
                text-align: center;
                max-width: 800px;
            }
            h1 { font-size: 3em; margin-bottom: 20px; }
            .status { 
                background: rgba(255,255,255,0.1); 
                padding: 20px; 
                border-radius: 15px;
                margin: 20px 0;
            }
            .feature {
                display: inline-block;
                margin: 10px;
                padding: 10px 20px;
                background: rgba(255,255,255,0.2);
                border-radius: 10px;
            }
            a {
                color: #fff;
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🇭🇹 Faner Studio</h1>
            <div class="status">
                <h2>✅ Sistèm la fonksyone!</h2>
                <p>Deplwaman otomatik aktif via GitHub Actions</p>
            </div>
            <div>
                <div class="feature">🎵 Jeneratè Mizik IA</div>
                <div class="feature">🎛️ Editè Odyo</div>
                <div class="feature">🌍 Tradiksyon NLLB</div>
                <div class="feature">🚀 Auto-Deploy</div>
            </div>
            <p style="margin-top: 30px;">
                <a href="/docs">📚 API Documentation</a> | 
                <a href="/health">🏥 Health Check</a>
            </p>
        </div>
    </body>
    </html>
    """)

@app.get("/health")
async def health_check():
    """Vérifie l'état du service"""
    return {
        "status": "healthy",
        "service": "Faner Studio",
        "version": "2.0.0",
        "deployment": "GitHub Actions → Render",
        "features": {
            "translation": "active",
            "api": "active",
            "auto_deploy": "active"
        }
    }

@app.get("/api/info")
async def api_info():
    """Informations sur l'API"""
    return {
        "api_name": "Faner Studio API",
        "version": "2.0.0",
        "description": "API pou kreyasyon kontni an Kreyòl Ayisyen",
        "endpoints": {
            "root": "GET / - Interface HTML",
            "health": "GET /health - Status check",
            "info": "GET /api/info - API information",
            "translate": "POST /api/translate - NLLB Translation",
            "docs": "GET /docs - Interactive API docs",
            "redoc": "GET /redoc - Alternative API docs"
        },
        "github": "https://github.com/GF154/fanerstudio",
        "auto_deploy": True
    }

@app.get("/api/status")
async def status():
    """Status détaillé du système"""
    import platform
    import sys
    
    return {
        "service": "online",
        "timestamp": "2024-11-01",
        "environment": os.getenv("RENDER", "development"),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "platform": platform.system(),
        "framework": "FastAPI 0.109.0",
        "deployment": {
            "platform": "Render" if os.getenv("RENDER") else "Local",
            "method": "GitHub Actions",
            "auto_deploy": True,
            "branch": "master"
        },
        "features": {
            "nllb_translation": True,
            "api_docs": True,
            "health_check": True,
            "cors_configured": True
        }
    }

# ============================================================
# API DE TRADUCTION
# ============================================================

@app.post("/api/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Traduit du texte en utilisant le modèle NLLB de Meta
    
    - **text**: Texte à traduire
    - **source**: Langue source (en, fr, ht, es)
    - **target**: Langue cible (en, fr, ht, es)
    """
    try:
        # Configuration de l'API Hugging Face
        url = "https://api-inference.huggingface.co/models/facebook/nllb-200-distilled-600M"
        headers = {}
        
        # Utiliser la clé API si disponible
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        # Mapping des codes de langue
        language_codes = {
            "en": "eng_Latn",
            "fr": "fra_Latn",
            "ht": "hat_Latn",
            "es": "spa_Latn",
            "pt": "por_Latn"
        }
        
        src_lang = language_codes.get(request.source, "eng_Latn")
        tgt_lang = language_codes.get(request.target, "hat_Latn")
        
        # Préparer le payload
        payload = {
            "inputs": request.text,
            "parameters": {
                "src_lang": src_lang,
                "tgt_lang": tgt_lang
            }
        }
        
        # Appel à l'API
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extraire la traduction
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
                # Modèle en cours de chargement
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
# GESTION DES ERREURS
# ============================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Gestionnaire personnalisé pour les erreurs 404"""
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
            ]
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Gestionnaire personnalisé pour les erreurs 500"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "status": "Please try again later"
        }
    )

# ============================================================
# POINT D'ENTRÉE
# ============================================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
