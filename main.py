#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Faner Studio - Ultra-Minimal API
GUARANTEED to work on Render free tier
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os

app = FastAPI(title="Faner Studio API", version="1.0")

# Mount static files (for tools.html and other HTML files)
@app.get("/tools.html")
def tools():
    """Serve the tools page"""
    html_path = os.path.join(os.path.dirname(__file__), "tools.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    else:
        return {"error": "Tools page not found"}

@app.get("/")
def root():
    """Serve the HTML interface if available, otherwise return JSON"""
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    else:
        return {"status": "live", "message": "Faner Studio fonksyone!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/translate")
async def translate(text: str, target: str = "ht"):
    """NLLB Translation"""
    try:
        url = "https://api-inference.huggingface.co/models/facebook/nllb-200-distilled-600M"
        headers = {}
        key = os.getenv("HUGGINGFACE_API_KEY")
        if key:
            headers["Authorization"] = f"Bearer {key}"
        
        langs = {"en": "eng_Latn", "fr": "fra_Latn", "ht": "hat_Latn"}
        payload = {
            "inputs": text,
            "parameters": {
                "src_lang": "eng_Latn",
                "tgt_lang": langs.get(target, "hat_Latn")
            }
        }
        
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(url, json=payload, headers=headers)
            if r.status_code == 200:
                result = r.json()
                translated = result[0]["translation_text"] if isinstance(result, list) else text
                return {"success": True, "original": text, "translated": translated}
            else:
                return {"success": False, "error": "API error", "original": text}
    except Exception as e:
        return {"success": False, "error": str(e), "original": text}
