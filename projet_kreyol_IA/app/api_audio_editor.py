"""
🎛️ API Routes pour l'éditeur audio avancé
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os
from src.audio_editor import AudioEditor, apply_preset, EFFECT_PRESETS

router = APIRouter(prefix="/api/audio-editor", tags=["audio-editor"])


class EffectRequest(BaseModel):
    effect_type: str
    params: dict = {}


class MultiEffectRequest(BaseModel):
    effects: List[dict]


@router.post("/normalize")
async def normalize_audio(
    file: UploadFile = File(...),
    target_dbfs: float = Form(-20.0)
):
    """Normalise un fichier audio"""
    try:
        temp_dir = "projet_kreyol_IA/output/temp"
        os.makedirs(temp_dir, exist_ok=True)
        
        input_path = os.path.join(temp_dir, file.filename)
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        editor = AudioEditor()
        output_path = editor.normalize_audio(input_path, target_dbfs=target_dbfs)
        
        if os.path.exists(input_path):
            os.remove(input_path)
        
        return {
            "success": True,
            "message": "Audio normalisé avec succès",
            "file_path": output_path,
            "download_url": f"/api/audio-editor/download?path={output_path}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fade")
async def apply_fade(
    file: UploadFile = File(...),
    fade_in_ms: int = Form(1000),
    fade_out_ms: int = Form(1000)
):
    """Applique des fondus"""
    try:
        temp_dir = "projet_kreyol_IA/output/temp"
        os.makedirs(temp_dir, exist_ok=True)
        
        input_path = os.path.join(temp_dir, file.filename)
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        editor = AudioEditor()
        output_path = editor.apply_fade(input_path, fade_in_ms, fade_out_ms)
        
        if os.path.exists(input_path):
            os.remove(input_path)
        
        return {
            "success": True,
            "message": "Fondus appliqués avec succès",
            "file_path": output_path,
            "download_url": f"/api/audio-editor/download?path={output_path}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compression")
async def apply_compression(
    file: UploadFile = File(...),
    threshold: float = Form(-20.0),
    ratio: float = Form(4.0)
):
    """Applique une compression"""
    try:
        temp_dir = "projet_kreyol_IA/output/temp"
        os.makedirs(temp_dir, exist_ok=True)
        
        input_path = os.path.join(temp_dir, file.filename)
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        editor = AudioEditor()
        output_path = editor.apply_compression(input_path, threshold, ratio)
        
        if os.path.exists(input_path):
            os.remove(input_path)
        
        return {
            "success": True,
            "message": "Compression appliquée avec succès",
            "file_path": output_path,
            "download_url": f"/api/audio-editor/download?path={output_path}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/eq")
async def apply_eq(
    file: UploadFile = File(...),
    bass_gain: float = Form(0.0),
    mid_gain: float = Form(0.0),
    treble_gain: float = Form(0.0)
):
    """Applique une égalisation"""
    try:
        temp_dir = "projet_kreyol_IA/output/temp"
        os.makedirs(temp_dir, exist_ok=True)
        
        input_path = os.path.join(temp_dir, file.filename)
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        editor = AudioEditor()
        output_path = editor.apply_eq(input_path, bass_gain, mid_gain, treble_gain)
        
        if os.path.exists(input_path):
            os.remove(input_path)
        
        return {
            "success": True,
            "message": "Égalisation appliquée avec succès",
            "file_path": output_path,
            "download_url": f"/api/audio-editor/download?path={output_path}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reverb")
async def apply_reverb(
    file: UploadFile = File(...),
    room_size: float = Form(0.5),
    damping: float = Form(0.5)
):
    """Applique une réverbération"""
    try:
        temp_dir = "projet_kreyol_IA/output/temp"
        os.makedirs(temp_dir, exist_ok=True)
        
        input_path = os.path.join(temp_dir, file.filename)
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        editor = AudioEditor()
        output_path = editor.apply_reverb(input_path, room_size, damping)
        
        if os.path.exists(input_path):
            os.remove(input_path)
        
        return {
            "success": True,
            "message": "Réverbération appliquée avec succès",
            "file_path": output_path,
            "download_url": f"/api/audio-editor/download?path={output_path}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/preset/{preset_name}")
async def apply_preset_effect(
    preset_name: str,
    file: UploadFile = File(...)
):
    """Applique un preset d'effets"""
    try:
        if preset_name not in EFFECT_PRESETS:
            raise HTTPException(status_code=400, detail=f"Preset '{preset_name}' non trouvé")
        
        temp_dir = "projet_kreyol_IA/output/temp"
        os.makedirs(temp_dir, exist_ok=True)
        
        input_path = os.path.join(temp_dir, file.filename)
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        output_path = apply_preset(input_path, preset_name)
        
        if os.path.exists(input_path):
            os.remove(input_path)
        
        return {
            "success": True,
            "message": f"Preset '{preset_name}' appliqué avec succès",
            "preset": preset_name,
            "file_path": output_path,
            "download_url": f"/api/audio-editor/download?path={output_path}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/presets")
async def get_presets():
    """Récupère les presets disponibles"""
    return {
        "success": True,
        "presets": {
            "podcast": {
                "name": "Podcast",
                "description": "Optimisé pour les podcasts et voix parlées",
                "effects": EFFECT_PRESETS['podcast']
            },
            "music": {
                "name": "Musique",
                "description": "Optimisé pour la musique",
                "effects": EFFECT_PRESETS['music']
            },
            "voice": {
                "name": "Voix",
                "description": "Optimisé pour les enregistrements vocaux",
                "effects": EFFECT_PRESETS['voice']
            },
            "radio": {
                "name": "Radio",
                "description": "Son radio professionnel",
                "effects": EFFECT_PRESETS['radio']
            }
        }
    }


@router.post("/info")
async def get_audio_info(file: UploadFile = File(...)):
    """Récupère les informations d'un fichier audio"""
    try:
        temp_dir = "projet_kreyol_IA/output/temp"
        os.makedirs(temp_dir, exist_ok=True)
        
        input_path = os.path.join(temp_dir, file.filename)
        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        editor = AudioEditor()
        info = editor.get_audio_info(input_path)
        
        if os.path.exists(input_path):
            os.remove(input_path)
        
        return {
            "success": True,
            "info": info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download")
async def download_audio(path: str):
    """Télécharge un fichier audio édité"""
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    return FileResponse(
        path=path,
        media_type="audio/mpeg",
        filename=os.path.basename(path)
    )

