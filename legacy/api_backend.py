#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Backend - Pwojè Kreyòl IA
Connecte l'interface web aux fonctionnalités Python
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import tempfile
import shutil
from typing import Optional
import pypdf
import asyncio

# Import des modules
from traduire_texte import traduire_avec_progress
from generer_audio_huggingface import generer_audio_creole
from podcast_creator import PodcastCreator

app = FastAPI(title="🇭🇹 Kreyòl IA API", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir fichiers statiques
app.mount("/output", StaticFiles(directory="output"), name="output")
app.mount("/static", StaticFiles(directory="."), name="static")

# Dossiers
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


@app.get("/")
async def home():
    """Page d'accueil"""
    return FileResponse("app_complete.html")


@app.post("/api/audiobook")
async def create_audiobook(
    file: UploadFile = File(...),
    voice: str = Form("creole-native")
):
    """Créer un audiobook en créole"""
    
    try:
        # Sauvegarder fichier temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = Path(tmp.name)
        
        # Extraire texte
        if file.filename.endswith('.pdf'):
            reader = pypdf.PdfReader(tmp_path)
            text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        elif file.filename.endswith('.txt'):
            text = tmp_path.read_text(encoding='utf-8')
        else:
            tmp_path.unlink()
            raise HTTPException(400, "Format non supporté. Utilisez .pdf ou .txt")
        
        # Traduire
        texte_traduit = traduire_avec_progress(text, langue_cible='ht')
        
        # Créer dossier sortie
        nom_base = Path(file.filename).stem
        output_base = OUTPUT_DIR / nom_base
        output_base.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarder traduction
        texte_path = output_base / f"{nom_base}_kreyol.txt"
        texte_path.write_text(texte_traduit, encoding='utf-8')
        
        # Générer audio
        audio_path = output_base / f"{nom_base}_audio.mp3"
        generer_audio_creole(texte_traduit, audio_path)
        
        # Nettoyer
        tmp_path.unlink()
        
        return JSONResponse({
            "status": "success",
            "message": "Audiobook créé avec succès!",
            "files": {
                "translation": f"/output/{nom_base}/{nom_base}_kreyol.txt",
                "audio": f"/output/{nom_base}/{nom_base}_audio.mp3"
            },
            "stats": {
                "original_chars": len(text),
                "translated_chars": len(texte_traduit),
                "original_words": len(text.split()),
                "translated_words": len(texte_traduit.split())
            }
        })
        
    except Exception as e:
        raise HTTPException(500, f"Erreur: {str(e)}")


@app.post("/api/podcast")
async def create_podcast(
    script: str = Form(...),
    format: str = Form("conversation"),
    voices: str = Form("auto")
):
    """Créer un podcast avec plusieurs voix"""
    
    try:
        # Créer le podcast
        creator = PodcastCreator()
        
        # Nom unique
        import time
        timestamp = int(time.time())
        nom_base = f"podcast_{timestamp}"
        
        output_path = OUTPUT_DIR / nom_base / f"{nom_base}.mp3"
        
        # Générer
        success = creator.create_podcast(script, output_path, add_music=False)
        
        if not success:
            raise HTTPException(500, "Erreur lors de la création du podcast")
        
        # Parser pour statistiques
        segments = creator.parse_script(script)
        speakers = set(seg['speaker'] for seg in segments)
        
        return JSONResponse({
            "status": "success",
            "message": "Podcast créé avec succès!",
            "files": {
                "audio": f"/output/{nom_base}/{nom_base}.mp3"
            },
            "stats": {
                "segments": len(segments),
                "speakers": len(speakers),
                "duration_estimate": len(script) / 150  # ~150 chars/sec
            }
        })
        
    except Exception as e:
        raise HTTPException(500, f"Erreur: {str(e)}")


@app.post("/api/translate")
async def translate_text(
    text: str = Form(...),
    source_lang: str = Form("auto"),
    target_lang: str = Form("ht")
):
    """Traduire du texte"""
    
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
        raise HTTPException(500, f"Erreur: {str(e)}")


@app.post("/api/pdf-translate")
async def translate_pdf(
    file: UploadFile = File(...),
    generate_audio: bool = Form(False)
):
    """Traduire un PDF"""
    
    try:
        # Sauvegarder temporairement
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = Path(tmp.name)
        
        # Extraire texte
        reader = pypdf.PdfReader(tmp_path)
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        
        # Traduire
        texte_traduit = traduire_avec_progress(text, langue_cible='ht')
        
        # Sauvegarder
        nom_base = Path(file.filename).stem
        output_base = OUTPUT_DIR / nom_base
        output_base.mkdir(parents=True, exist_ok=True)
        
        texte_path = output_base / f"{nom_base}_kreyol.txt"
        texte_path.write_text(texte_traduit, encoding='utf-8')
        
        result = {
            "status": "success",
            "files": {
                "translation": f"/output/{nom_base}/{nom_base}_kreyol.txt"
            },
            "stats": {
                "pages": len(reader.pages),
                "chars": len(texte_traduit)
            }
        }
        
        # Générer audio si demandé
        if generate_audio:
            audio_path = output_base / f"{nom_base}_audio.mp3"
            generer_audio_creole(texte_traduit, audio_path)
            result["files"]["audio"] = f"/output/{nom_base}/{nom_base}_audio.mp3"
        
        # Nettoyer
        tmp_path.unlink()
        
        return JSONResponse(result)
        
    except Exception as e:
        raise HTTPException(500, f"Erreur: {str(e)}")


@app.get("/api/projects")
async def list_projects():
    """Lister tous les projets"""
    
    projects = []
    
    for project_dir in OUTPUT_DIR.iterdir():
        if project_dir.is_dir() and not project_dir.name.startswith('.'):
            files = list(project_dir.glob("*"))
            
            # Déterminer le type
            has_audio = any(f.suffix == '.mp3' for f in files)
            has_translation = any('kreyol' in f.name for f in files)
            
            project_type = "Audiobook" if has_audio else "Translation"
            
            projects.append({
                "name": project_dir.name,
                "type": project_type,
                "files": [f.name for f in files],
                "file_count": len(files),
                "created": project_dir.stat().st_ctime
            })
    
    # Trier par date (plus récent d'abord)
    projects.sort(key=lambda x: x['created'], reverse=True)
    
    return JSONResponse({
        "status": "success",
        "projects": projects,
        "total": len(projects)
    })


@app.get("/api/health")
async def health_check():
    """Vérifier l'état de l'API"""
    return JSONResponse({
        "status": "healthy",
        "version": "1.0",
        "features": [
            "audiobook",
            "podcast",
            "translate",
            "pdf-translate"
        ]
    })


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🇭🇹 KREYÒL IA - API BACKEND")
    print("=" * 60)
    print()
    print("🌐 API Server: http://localhost:8000")
    print("📱 Web App: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print()
    print("✨ Fonctionnalités actives:")
    print("   - 📚 Audiobook Creator")
    print("   - 🎙️ Podcast Creator")
    print("   - 🌍 Text Translator")
    print("   - 📄 PDF Translator")
    print()
    print("🛑 Ctrl+C pour arrêter")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

