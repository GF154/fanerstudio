"""
🎵 API Routes pour le générateur de musique IA
Routes FastAPI pour la génération et le mixage de musique
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os
from src.music_generator import HaitianMusicGenerator, generate_background_music, mix_audio_files

router = APIRouter(prefix="/api/music", tags=["music"])

# Modèles de données
class MusicGenerationRequest(BaseModel):
    style: str = "konpa"
    duration: int = 30
    add_melody: bool = True
    add_bass: bool = True
    add_drums: bool = True

class BeatGenerationRequest(BaseModel):
    style: str = "konpa"
    bars: int = 8

class MixRequest(BaseModel):
    style: str = "konpa"
    music_volume: int = -20


@router.get("/styles")
async def get_music_styles():
    """
    Récupère la liste des styles musicaux disponibles
    
    Returns:
        Dict des styles avec leurs descriptions
    """
    try:
        styles = HaitianMusicGenerator.get_available_styles()
        return {
            "success": True,
            "styles": styles,
            "count": len(styles)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate")
async def generate_music(request: MusicGenerationRequest):
    """
    Génère une piste musicale de style haïtien
    
    Args:
        request: Paramètres de génération
        
    Returns:
        Informations sur le fichier généré
    """
    try:
        generator = HaitianMusicGenerator()
        
        output_path = generator.generate_music(
            style=request.style,
            duration=request.duration,
            add_melody=request.add_melody,
            add_bass=request.add_bass,
            add_drums=request.add_drums
        )
        
        return {
            "success": True,
            "message": f"Musique {request.style} générée avec succès",
            "file_path": output_path,
            "style": request.style,
            "duration": request.duration,
            "download_url": f"/api/music/download?path={output_path}"
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération: {str(e)}")


@router.post("/beat")
async def generate_beat(request: BeatGenerationRequest):
    """
    Génère un beat instrumental
    
    Args:
        request: Paramètres du beat
        
    Returns:
        Informations sur le beat généré
    """
    try:
        generator = HaitianMusicGenerator()
        
        output_path = generator.create_beat(
            style=request.style,
            bars=request.bars
        )
        
        return {
            "success": True,
            "message": f"Beat {request.style} généré avec succès",
            "file_path": output_path,
            "style": request.style,
            "bars": request.bars,
            "download_url": f"/api/music/download?path={output_path}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération du beat: {str(e)}")


@router.post("/mix")
async def mix_voice_with_music(
    voice_file: UploadFile = File(...),
    style: str = Form("konpa"),
    music_volume: int = Form(-20),
    use_custom_music: bool = Form(False),
    music_file: Optional[UploadFile] = File(None)
):
    """
    Mixe un fichier vocal avec de la musique de fond
    
    Args:
        voice_file: Fichier audio vocal
        style: Style musical (si génération automatique)
        music_volume: Volume de la musique en dB
        use_custom_music: Utiliser une musique personnalisée
        music_file: Fichier musique personnalisé (optionnel)
        
    Returns:
        Fichier audio mixé
    """
    try:
        # Créer le dossier temporaire
        temp_dir = "projet_kreyol_IA/output/temp"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Sauvegarder le fichier vocal
        voice_path = os.path.join(temp_dir, f"voice_{voice_file.filename}")
        with open(voice_path, "wb") as f:
            content = await voice_file.read()
            f.write(content)
        
        # Gérer la musique
        music_path = None
        if use_custom_music and music_file:
            music_path = os.path.join(temp_dir, f"music_{music_file.filename}")
            with open(music_path, "wb") as f:
                content = await music_file.read()
                f.write(content)
        
        # Mixer
        generator = HaitianMusicGenerator()
        mixed_path = generator.mix_music_with_voice(
            voice_path=voice_path,
            music_path=music_path,
            style=style,
            music_volume=music_volume
        )
        
        # Nettoyer les fichiers temporaires
        if os.path.exists(voice_path):
            os.remove(voice_path)
        if music_path and os.path.exists(music_path):
            os.remove(music_path)
        
        return {
            "success": True,
            "message": "Audio mixé avec succès",
            "file_path": mixed_path,
            "style": style,
            "download_url": f"/api/music/download?path={mixed_path}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du mixage: {str(e)}")


@router.get("/download")
async def download_music(path: str):
    """
    Télécharge un fichier audio généré
    
    Args:
        path: Chemin du fichier
        
    Returns:
        Fichier audio
    """
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    return FileResponse(
        path=path,
        media_type="audio/mpeg",
        filename=os.path.basename(path)
    )


@router.post("/quick-generate/{style}")
async def quick_generate_music(style: str, duration: int = 30):
    """
    Génération rapide de musique avec paramètres par défaut
    
    Args:
        style: Style musical
        duration: Durée en secondes
        
    Returns:
        Fichier audio généré
    """
    try:
        output_path = generate_background_music(style=style, duration=duration)
        
        return {
            "success": True,
            "message": f"Musique {style} générée rapidement",
            "file_path": output_path,
            "download_url": f"/api/music/download?path={output_path}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates")
async def get_music_templates():
    """
    Récupère les templates de musique pré-configurés
    
    Returns:
        Liste des templates disponibles
    """
    templates = [
        {
            "id": "konpa_dance",
            "name": "Konpa Dance",
            "style": "konpa",
            "duration": 180,
            "description": "Konpa énergique pour danser",
            "bpm": 120
        },
        {
            "id": "rara_festival",
            "name": "Rara Festival",
            "style": "rara",
            "duration": 240,
            "description": "Ambiance festive Rara",
            "bpm": 140
        },
        {
            "id": "racine_roots",
            "name": "Racine Roots",
            "style": "racine",
            "duration": 200,
            "description": "Musique roots authentique",
            "bpm": 100
        },
        {
            "id": "rap_beat",
            "name": "Rap Kreyòl Beat",
            "style": "rap_kreyol",
            "duration": 180,
            "description": "Beat pour rap en créole",
            "bpm": 95
        },
        {
            "id": "twoubadou_folk",
            "name": "Twoubadou Folk",
            "style": "twoubadou",
            "duration": 150,
            "description": "Musique folk traditionnelle",
            "bpm": 90
        },
        {
            "id": "zouk_love",
            "name": "Zouk Love",
            "style": "zouk",
            "duration": 210,
            "description": "Zouk romantique",
            "bpm": 130
        }
    ]
    
    return {
        "success": True,
        "templates": templates,
        "count": len(templates)
    }


@router.post("/generate-from-template/{template_id}")
async def generate_from_template(template_id: str):
    """
    Génère de la musique à partir d'un template
    
    Args:
        template_id: ID du template
        
    Returns:
        Fichier audio généré
    """
    templates_response = await get_music_templates()
    templates = {t["id"]: t for t in templates_response["templates"]}
    
    if template_id not in templates:
        raise HTTPException(status_code=404, detail="Template non trouvé")
    
    template = templates[template_id]
    
    try:
        output_path = generate_background_music(
            style=template["style"],
            duration=template["duration"]
        )
        
        return {
            "success": True,
            "message": f"Musique générée depuis le template '{template['name']}'",
            "template": template,
            "file_path": output_path,
            "download_url": f"/api/music/download?path={output_path}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

