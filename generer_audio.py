#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur d'Audiobook - Pwojè Kreyòl IA
"""

import sys
from pathlib import Path
from gtts import gTTS
from tqdm import tqdm

def generer_audio(texte, chemin_sortie, langue='fr'):
    """Générer un fichier audio MP3 à partir du texte"""
    print(f"\n🎧 Génération de l'audiobook...")
    print(f"   Texte: {len(texte)} caractères")
    print(f"   Langue: Français (pour texte créole)")
    print(f"   Note: Le créole haïtien sera prononcé avec accent français")
    print(f"   Sortie: {chemin_sortie}")
    print()
    
    try:
        # Créer le dossier de sortie
        chemin_sortie.parent.mkdir(parents=True, exist_ok=True)
        
        # Générer l'audio avec gTTS
        print("📢 Synthèse vocale en cours...")
        
        # Utiliser une barre de progression factice
        with tqdm(total=100, desc="Génération audio", unit="%") as pbar:
            pbar.update(20)
            
            # Créer l'objet TTS avec accent français pour le créole
            tts = gTTS(text=texte, lang=langue, slow=False, tld='com')
            pbar.update(40)
            
            # Sauvegarder le fichier
            tts.save(str(chemin_sortie))
            pbar.update(40)
        
        # Vérifier la taille du fichier
        taille_ko = chemin_sortie.stat().st_size / 1024
        duree_estimee = len(texte) / 200  # Estimation: ~200 chars/minute
        
        print()
        print(f"✅ Audiobook créé avec succès!")
        print(f"   Fichier: {chemin_sortie}")
        print(f"   Taille: {taille_ko:.2f} Ko")
        print(f"   Durée estimée: ~{duree_estimee:.1f} minutes")
        
        return True
    
    except Exception as e:
        print(f"❌ Erreur lors de la génération audio: {e}")
        return False


def lire_fichier_texte(chemin):
    """Lire un fichier texte"""
    try:
        with open(chemin, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Erreur de lecture: {e}")
        return None


def main():
    """Fonction principale"""
    print("="*60)
    print("🎧 GÉNÉRATEUR D'AUDIOBOOK EN CRÉOLE HAÏTIEN")
    print("="*60)
    print()
    
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("Usage: python generer_audio.py <fichier_texte_kreyol.txt>")
        print()
        print("Exemple:")
        print("  python generer_audio.py output/test_document/test_document_kreyol.txt")
        return 1
    
    fichier_texte = Path(sys.argv[1])
    
    # Vérifier que le fichier existe
    if not fichier_texte.exists():
        print(f"❌ Fichier introuvable: {fichier_texte}")
        return 1
    
    print(f"📖 Fichier source: {fichier_texte.name}")
    
    # Lire le texte
    print(f"📄 Lecture du texte créole...")
    texte = lire_fichier_texte(fichier_texte)
    
    if not texte:
        return 1
    
    print(f"✅ Texte chargé: {len(texte)} caractères")
    
    # Générer le chemin de sortie
    nom_base = fichier_texte.stem.replace('_kreyol', '')
    dossier_sortie = fichier_texte.parent
    audio_path = dossier_sortie / f"{nom_base}_audio.mp3"
    
    # Générer l'audio (utiliser 'fr' car gTTS ne supporte pas 'ht')
    if not generer_audio(texte, audio_path, langue='fr'):
        return 1
    
    # Résumé final
    print("\n" + "="*60)
    print("✅ AUDIOBOOK CRÉÉ AVEC SUCCÈS!")
    print("="*60)
    print(f"🎧 Fichier audio: {audio_path}")
    print()
    print("💡 Pour écouter:")
    print(f"   - Double-cliquez sur le fichier")
    print(f"   - Ou utilisez votre lecteur audio préféré")
    print("="*60)
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Génération interrompue")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

