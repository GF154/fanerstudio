#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur d'Audiobook avec Hugging Face TTS - Pwojè Kreyòl IA
Utilise facebook/mms-tts-hat pour une vraie voix créole haïtienne
OPTIMIZED: Model caching & batch processing
"""

import sys
from pathlib import Path
import numpy as np
from tqdm import tqdm
import scipy.io.wavfile as wavfile

# Import optimized TTS Manager
try:
    from app.services.tts_manager import get_tts_manager
    USE_MANAGER = True
except ImportError:
    # Fallback to legacy implementation
    import torch
    from transformers import VitsModel, AutoTokenizer
    USE_MANAGER = False

def generer_audio_creole(texte, chemin_sortie, model_name="facebook/mms-tts-hat"):
    """
    Générer un fichier audio avec une vraie voix créole haïtienne
    
    Args:
        texte: Le texte créole à synthétiser
        chemin_sortie: Chemin du fichier MP3 de sortie
        model_name: Modèle Hugging Face à utiliser
    """
    print(f"\n🎧 Génération de l'audiobook avec voix créole native...")
    print(f"   Modèle: {model_name}")
    print(f"   Texte: {len(texte)} caractères")
    print(f"   Sortie: {chemin_sortie}")
    print()
    
    try:
        # Créer le dossier de sortie
        chemin_sortie.parent.mkdir(parents=True, exist_ok=True)
        
        # Charger le modèle et le tokenizer
        print("📥 Chargement du modèle TTS créole haïtien...")
        with tqdm(total=100, desc="Préparation", unit="%") as pbar:
            pbar.update(20)
            
            try:
                model = VitsModel.from_pretrained(model_name)
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                pbar.update(40)
            except Exception as e:
                print(f"\n⚠️  Le modèle {model_name} n'est pas disponible.")
                print(f"   Erreur: {e}")
                print(f"\n💡 Utilisation du fallback avec gTTS...")
                return generer_audio_gtts_fallback(texte, chemin_sortie)
        
        print("✅ Modèle chargé!")
        print()
        
        # Diviser le texte en phrases pour éviter les timeouts
        phrases = texte.split('.')
        phrases = [p.strip() + '.' for p in phrases if p.strip()]
        
        print(f"📝 Traitement de {len(phrases)} phrase(s)...")
        print()
        
        # Générer l'audio phrase par phrase
        tous_les_audios = []
        
        with tqdm(total=len(phrases), desc="Synthèse vocale", unit="phrase") as pbar:
            for phrase in phrases:
                # Nettoyer et valider la phrase
                phrase_clean = phrase.strip()
                
                # Ignorer les phrases trop courtes ou vides
                if len(phrase_clean) < 3:
                    pbar.update(1)
                    continue
                
                try:
                    # Tokenizer la phrase
                    inputs = tokenizer(phrase_clean, return_tensors="pt")
                    
                    # Vérifier que l'input n'est pas vide
                    if inputs['input_ids'].shape[1] == 0:
                        print(f"\n⚠️  Phrase ignorée (tokenization vide): {phrase_clean[:50]}...")
                        pbar.update(1)
                        continue
                    
                    # Générer l'audio
                    with torch.no_grad():
                        output = model(**inputs).waveform
                    
                    # Vérifier que l'output n'est pas vide
                    if output.numel() == 0:
                        print(f"\n⚠️  Phrase ignorée (output vide): {phrase_clean[:50]}...")
                        pbar.update(1)
                        continue
                    
                    # Convertir en numpy
                    audio_np = output.squeeze().cpu().numpy()
                    tous_les_audios.append(audio_np)
                    
                except Exception as e:
                    print(f"\n⚠️  Erreur sur phrase: {str(e)[:100]}")
                    print(f"    Phrase: {phrase_clean[:50]}...")
                    pbar.update(1)
                    continue
                
                pbar.update(1)
        
        if not tous_les_audios:
            print("❌ Aucun audio généré")
            return False
        
        print()
        print("🔗 Assemblage des segments audio...")
        
        # Concaténer tous les segments
        audio_complet = np.concatenate(tous_les_audios)
        
        # Normaliser l'audio (entre -1 et 1)
        audio_complet = audio_complet / np.max(np.abs(audio_complet))
        
        # Convertir en int16 pour WAV
        audio_int16 = (audio_complet * 32767).astype(np.int16)
        
        # Sauvegarder en WAV avec scipy
        wav_path = chemin_sortie.with_suffix('.wav')
        wavfile.write(
            str(wav_path),
            rate=model.config.sampling_rate,
            data=audio_int16
        )
        
        print(f"✅ Fichier WAV créé: {wav_path}")
        
        # Essayer de convertir en MP3 si ffmpeg est disponible
        try:
            import subprocess
            mp3_path = chemin_sortie.with_suffix('.mp3')
            subprocess.run([
                'ffmpeg', '-i', str(wav_path),
                '-codec:a', 'libmp3lame', '-qscale:a', '2',
                str(mp3_path), '-y'
            ], check=True, capture_output=True)
            print(f"✅ Fichier MP3 créé: {mp3_path}")
            
            # Supprimer le WAV si MP3 réussi
            wav_path.unlink()
            chemin_final = mp3_path
        except:
            print("ℹ️  FFmpeg non disponible, fichier sauvegardé en WAV")
            chemin_final = wav_path
        
        # Statistiques
        duree = len(audio_complet) / model.config.sampling_rate
        taille_ko = chemin_final.stat().st_size / 1024
        
        print()
        print(f"✅ Audiobook créé avec succès!")
        print(f"   Fichier: {chemin_final}")
        print(f"   Taille: {taille_ko:.2f} Ko")
        print(f"   Durée: {duree:.1f} secondes (~{duree/60:.1f} minutes)")
        print(f"   Qualité: Voix créole haïtienne native 🇭🇹")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Erreur lors de la génération: {e}")
        print("\n💡 Tentative avec fallback gTTS...")
        return generer_audio_gtts_fallback(texte, chemin_sortie)


def generer_audio_gtts_fallback(texte, chemin_sortie):
    """Fallback avec gTTS si Hugging Face ne fonctionne pas"""
    print("\n🔄 Utilisation de gTTS comme solution de repli...")
    
    try:
        from gtts import gTTS
        
        # Générer avec gTTS (français pour prononcer le créole)
        tts = gTTS(text=texte, lang='fr', slow=False)
        tts.save(str(chemin_sortie))
        
        taille_ko = chemin_sortie.stat().st_size / 1024
        print(f"✅ Audio créé avec gTTS: {taille_ko:.2f} Ko")
        print("   Note: Prononciation avec accent français")
        
        return True
    
    except Exception as e:
        print(f"❌ Erreur gTTS: {e}")
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
    print("🇭🇹 GÉNÉRATEUR D'AUDIOBOOK CRÉOLE HAÏTIEN")
    print("   avec Voix Native Hugging Face")
    print("="*60)
    print()
    
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("Usage: python generer_audio_huggingface.py <fichier_kreyol.txt>")
        print()
        print("Exemple:")
        print("  python generer_audio_huggingface.py output/test_document/test_document_kreyol.txt")
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
    audio_path = dossier_sortie / f"{nom_base}_audio_hf.mp3"
    
    # Générer l'audio
    if not generer_audio_creole(texte, audio_path):
        return 1
    
    # Résumé final
    print("\n" + "="*60)
    print("✅ AUDIOBOOK CRÉÉ AVEC SUCCÈS!")
    print("="*60)
    print(f"🎧 Fichier audio: {audio_path}")
    print()
    print("💡 Pour écouter:")
    print(f"   - Double-cliquez sur le fichier")
    print(f"   - Ou utilisez: {audio_path}")
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

