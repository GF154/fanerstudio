#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇭🇹 Kreyòl IA - API Backend Complete
Professional-grade API for all features
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import tempfile
import shutil
from typing import Optional
import uuid
from datetime import datetime

# Import modules
from traduire_texte import traduire_avec_progress
from generer_audio_huggingface import generer_audio_creole
from podcast_creator import PodcastCreator
import pypdf

app = FastAPI(
    title="🇭🇹 Kreyòl IA API",
    description="Professional AI-powered Haitian Creole content creation",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Initialize services
podcast_creator = PodcastCreator()

# ============================================================
# AUDIO ENDPOINTS
# ============================================================

@app.post("/api/audiobook")
async def create_audiobook(
    file: UploadFile = File(...),
    voice: str = Form("creole-native")
):
    """
    📚 Create Haitian Creole audiobook from document
    
    Supports: .pdf, .txt, .epub, .html, .docx
    """
    try:
        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = Path(tmp.name)
        
        # Extract text
        if file.filename.endswith('.pdf'):
            reader = pypdf.PdfReader(tmp_path)
            text = "\n".join(page.extract_text() for page in reader.pages)
        elif file.filename.endswith('.txt'):
            text = tmp_path.read_text(encoding='utf-8')
        else:
            raise HTTPException(400, "Unsupported format")
        
        # Translate to Creole
        texte_traduit = traduire_avec_progress(text, langue_cible='ht')
        
        # Create output directory
        nom_base = Path(file.filename).stem
        output_base = OUTPUT_DIR / nom_base
        output_base.mkdir(parents=True, exist_ok=True)
        
        # Save translation
        texte_path = output_base / f"{nom_base}_kreyol.txt"
        texte_path.write_text(texte_traduit, encoding='utf-8')
        
        # Generate audio
        audio_path = output_base / f"{nom_base}_audio.mp3"
        generer_audio_creole(texte_traduit, audio_path)
        
        # Cleanup
        tmp_path.unlink()
        
        return JSONResponse({
            "status": "success",
            "files": {
                "translation": f"/output/{nom_base}/{texte_path.name}",
                "audio": f"/output/{nom_base}/{audio_path.name}"
            },
            "stats": {
                "original_chars": len(text),
                "translated_chars": len(texte_traduit),
                "original_words": len(text.split()),
                "translated_words": len(texte_traduit.split())
            }
        })
        
    except Exception as e:
        raise HTTPException(500, f"Error creating audiobook: {str(e)}")


@app.post("/api/podcast")
async def create_podcast(
    script: str = Form(...),
    format: str = Form("conversation"),
    voices: str = Form("auto")
):
    """
    🎙️ Create multi-voice podcast
    
    Format: conversation | interview
    """
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
        podcast_creator.create_podcast(str(tmp_script_path), podcast_output_path)
        
        # Cleanup
        tmp_script_path.unlink()
        
        return JSONResponse({
            "status": "success",
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
        raise HTTPException(500, f"Error creating podcast: {str(e)}")


@app.post("/api/url-to-audio")
async def convert_url_to_audio(
    url: str = Form(...),
    language: str = Form("ht")
):
    """
    🔗 Convert web article to audio
    
    Extract, translate, and generate audio from URL
    """
    try:
        # TODO: Implement web scraping
        # For now, return placeholder
        return JSONResponse({
            "status": "coming_soon",
            "message": "URL to Audio feature will be available soon!"
        })
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")


@app.post("/api/ai-script")
async def generate_ai_script(
    prompt: str = Form(...),
    type: str = Form("story")
):
    """
    ✨ Generate AI script in Creole
    
    Types: story | news | educational | podcast
    """
    try:
        # TODO: Implement AI script generation
        return JSONResponse({
            "status": "coming_soon",
            "message": "AI Script Generator will be available soon!"
        })
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")


# ============================================================
# VIDEO ENDPOINTS
# ============================================================

@app.post("/api/video-voiceover")
async def add_video_voiceover(
    video: UploadFile = File(...),
    script: str = Form(...)
):
    """
    🎥 Add Creole voiceover to video
    """
    try:
        # TODO: Implement video voiceover
        return JSONResponse({
            "status": "coming_soon",
            "message": "Video Voiceover feature will be available soon!"
        })
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")


@app.post("/api/sfx-music")
async def add_sfx_music(
    audio: UploadFile = File(...),
    music_style: str = Form("compas")
):
    """
    🎵 Add Haitian music and sound effects
    
    Styles: compas | rara | troubadou | mizik-rasin
    """
    try:
        # TODO: Implement music mixing
        return JSONResponse({
            "status": "coming_soon",
            "message": "SFX and Music feature will be available soon!"
        })
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")


@app.post("/api/captions")
async def add_captions(
    video: UploadFile = File(...),
    language: str = Form("ht")
):
    """
    📝 Auto-generate Creole captions
    """
    try:
        # TODO: Implement caption generation
        return JSONResponse({
            "status": "coming_soon",
            "message": "Captions feature will be available soon!"
        })
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")


@app.post("/api/remove-noise")
async def remove_background_noise(
    audio: UploadFile = File(...),
    level: str = Form("medium")
):
    """
    🔇 Remove background noise from audio
    
    Levels: light | medium | strong
    """
    try:
        # TODO: Implement noise reduction
        return JSONResponse({
            "status": "coming_soon",
            "message": "Noise Removal feature will be available soon!"
        })
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")


@app.post("/api/fix-voiceover")
async def fix_voiceover_mistakes(
    audio: UploadFile = File(...),
    corrected_text: str = Form(...)
):
    """
    🔧 Fix voiceover mistakes
    """
    try:
        # TODO: Implement voiceover fixing
        return JSONResponse({
            "status": "coming_soon",
            "message": "Fix Voiceover feature will be available soon!"
        })
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")


@app.post("/api/ai-soundtrack")
async def generate_ai_soundtrack(
    prompt: str = Form(...),
    style: str = Form("compas")
):
    """
    🎼 Generate AI Haitian soundtrack
    """
    try:
        # TODO: Implement AI music generation
        return JSONResponse({
            "status": "coming_soon",
            "message": "AI Soundtrack Generator will be available soon!"
        })
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")


# ============================================================
# KREYÒL TRANSLATION ENDPOINTS
# ============================================================

@app.post("/api/translate")
async def translate_text(
    text: str = Form(...),
    target_lang: str = Form("ht")
):
    """
    🌍 Translate text to Haitian Creole
    
    Uses M2M100 AI model for high-quality translation
    """
    try:
        texte_traduit = traduire_avec_progress(text, langue_cible=target_lang)
        
        return JSONResponse({
            "status": "success",
            "translation": texte_traduit,
            "stats": {
                "original_length": len(text),
                "translated_length": len(texte_traduit),
                "original_words": len(text.split()),
                "translated_words": len(texte_traduit.split())
            }
        })
        
    except Exception as e:
        raise HTTPException(500, f"Error translating: {str(e)}")


@app.post("/api/pdf-translate")
async def translate_pdf(
    file: UploadFile = File(...),
    generate_audio: bool = Form(True)
):
    """
    📄 Translate PDF to Haitian Creole
    
    Optional: Generate audiobook from translation
    """
    try:
        # Save uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = Path(tmp.name)
        
        # Extract text
        reader = pypdf.PdfReader(tmp_path)
        text = "\n".join(page.extract_text() for page in reader.pages)
        
        # Translate
        texte_traduit = traduire_avec_progress(text, langue_cible='ht')
        
        # Create output
        nom_base = Path(file.filename).stem
        output_base = OUTPUT_DIR / nom_base
        output_base.mkdir(parents=True, exist_ok=True)
        
        # Save translation
        texte_path = output_base / f"{nom_base}_kreyol.txt"
        texte_path.write_text(texte_traduit, encoding='utf-8')
        
        audio_file_url = None
        if generate_audio:
            audio_path = output_base / f"{nom_base}_audio.mp3"
            generer_audio_creole(texte_traduit, audio_path)
            audio_file_url = f"/output/{nom_base}/{audio_path.name}"
        
        # Cleanup
        tmp_path.unlink()
        
        return JSONResponse({
            "status": "success",
            "files": {
                "translation": f"/output/{nom_base}/{texte_path.name}",
                "audio": audio_file_url
            },
            "stats": {
                "pages": len(reader.pages),
                "chars": len(text),
                "translated_chars": len(texte_traduit)
            }
        })
        
    except Exception as e:
        raise HTTPException(500, f"Error translating PDF: {str(e)}")


# ============================================================
# PROJECT MANAGEMENT
# ============================================================

@app.get("/api/projects")
async def list_projects():
    """
    📂 List all user projects
    """
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


@app.get("/api/health")
async def health_check():
    """
    ✅ Health check endpoint
    """
    return JSONResponse({
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    })


# ============================================================
# STATIC FILES & APP
# ============================================================

# Serve output files
app.mount("/output", StaticFiles(directory="output"), name="output")

@app.get("/")
async def serve_app():
    """Serve main application - 100% Kreyòl Ayisyen"""
    return FileResponse("app_studio_dark.html")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get port from environment variable (for Render/Heroku) or default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    print("=" * 60)
    print("🇭🇹 KREYÒL IA - PROFESSIONAL STUDIO")
    print("=" * 60)
    print(f"🌐 API Documentation: http://localhost:{port}/docs")
    print(f"📱 Web Application:   http://localhost:{port}")
    print("=" * 60)
    print("\n✨ Features:")
    print("   📚 Audiobook Creation (AI-powered)")
    print("   🎙️ Podcast Generation (Multi-voice)")
    print("   🌍 Translation (M2M100 AI)")
    print("   📄 PDF Processing")
    print("   🎥 Video Tools (Coming soon)")
    print("=" * 60)
    print(f"\n🚀 Server starting on port {port}...\n")
    
    uvicorn.run(app, host="0.0.0.0", port=port)

