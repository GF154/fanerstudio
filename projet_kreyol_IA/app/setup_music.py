"""
🎵🎛️ Setup des routes pour les nouvelles fonctionnalités musicales
"""

from fastapi import FastAPI


def setup_music_routes(app: FastAPI):
    """
    Configure toutes les routes musicales et d'édition audio
    
    Args:
        app: Instance FastAPI
    """
    try:
        # Importer les routers
        from app.api_music import router as music_router
        from app.api_audio_editor import router as editor_router
        
        # Inclure les routers
        app.include_router(music_router)
        app.include_router(editor_router)
        
        print("✅ Routes musicales chargées:")
        print("   • Générateur de musique IA (/api/music/*)")
        print("   • Éditeur audio avancé (/api/audio-editor/*)")
        
        return True
        
    except ImportError as e:
        print(f"⚠️  Erreur chargement routes musicales: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Erreur configuration routes: {e}")
        return False


def get_music_info():
    """Retourne les informations sur les fonctionnalités musicales"""
    return {
        "music_generator": {
            "description": "Générateur de musique haïtienne avec IA",
            "styles": ["konpa", "rara", "racine", "rap_kreyol", "zouk", "twoubadou"],
            "endpoints": [
                "GET  /api/music/styles - Liste des styles",
                "POST /api/music/generate - Générer de la musique",
                "POST /api/music/beat - Créer un beat",
                "POST /api/music/mix - Mixer voix et musique",
                "GET  /api/music/templates - Templates prédéfinis",
            ]
        },
        "audio_editor": {
            "description": "Éditeur audio professionnel",
            "features": ["normalize", "compression", "eq", "reverb", "fade"],
            "presets": ["podcast", "music", "voice", "radio"],
            "endpoints": [
                "POST /api/audio-editor/normalize - Normaliser audio",
                "POST /api/audio-editor/compression - Compresser",
                "POST /api/audio-editor/eq - Égalisation",
                "POST /api/audio-editor/reverb - Réverbération",
                "POST /api/audio-editor/fade - Fondus",
                "POST /api/audio-editor/preset/{name} - Appliquer preset",
                "GET  /api/audio-editor/presets - Liste des presets",
            ]
        }
    }

