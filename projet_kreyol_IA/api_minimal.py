#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇭🇹 Kreyòl IA - Minimal API for Deployment Test
Ultra-simple version - GUARANTEED to work on Render
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import os

# Create FastAPI app
app = FastAPI(
    title="🇭🇹 Kreyòl IA Studio API",
    description="API minimale pou test déploiement",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "status": "live",
        "service": "Kreyòl IA Studio",
        "version": "1.0.0",
        "message": "API fonksyone! ✅"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Kreyòl IA Studio API",
        "version": "1.0.0"
    }

# ============================================================
# NLLB TRANSLATION (Minimal)
# ============================================================

@app.post("/api/translate")
async def translate(text: str, source_lang: str = "en", target_lang: str = "ht"):
    """
    🌍 Tradwi ak NLLB
    
    Minimal translation endpoint for testing
    """
    try:
        # NLLB language codes
        lang_map = {
            "en": "eng_Latn",
            "fr": "fra_Latn", 
            "es": "spa_Latn",
            "ht": "hat_Latn"
        }
        
        src_code = lang_map.get(source_lang, "eng_Latn")
        tgt_code = lang_map.get(target_lang, "hat_Latn")
        
        # Call NLLB API
        api_url = "https://api-inference.huggingface.co/models/facebook/nllb-200-distilled-600M"
        headers = {}
        
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        payload = {
            "inputs": text,
            "parameters": {
                "src_lang": src_code,
                "tgt_lang": tgt_code
            }
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(api_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                translated = result[0].get("translation_text", text) if isinstance(result, list) else text
                
                return {
                    "status": "success",
                    "original": text,
                    "translated": translated,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "model": "NLLB"
                }
            else:
                return {
                    "status": "error",
                    "message": f"API returned {response.status_code}",
                    "original": text
                }
    
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "original": text
        }

# ============================================================
# STARTUP
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

