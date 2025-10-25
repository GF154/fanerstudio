#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Podcast Creator - Pwojè Kreyòl IA
Créer des podcasts professionnels avec plusieurs voix en créole
"""

import sys
from pathlib import Path
from gtts import gTTS
import re
from tqdm import tqdm
import json
import subprocess
import wave
import struct

class PodcastCreator:
    """Créateur de podcasts multi-voix"""
    
    def __init__(self):
        self.voices = {
            'chris': {'lang': 'fr', 'tld': 'com', 'gender': 'male'},
            'jessica': {'lang': 'fr', 'tld': 'ca', 'gender': 'female'},
            'pierre': {'lang': 'fr', 'tld': 'fr', 'gender': 'male'},
            'marie': {'lang': 'fr', 'tld': 'com', 'gender': 'female'},
        }
        
    def parse_script(self, script_text):
        """
        Parser le script pour identifier les speakers et leur texte
        Format: "Speaker: Texte"
        """
        lines = script_text.strip().split('\n')
        segments = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Chercher le pattern "Speaker: Texte"
            match = re.match(r'^([^:]+):\s*(.+)$', line)
            if match:
                speaker = match.group(1).strip().lower()
                text = match.group(2).strip()
                
                # Mapper au speaker par défaut si non reconnu
                if speaker not in self.voices:
                    # Essayer de détecter le genre par les noms communs
                    if any(name in speaker.lower() for name in ['host', 'animateur', 'présentateur']):
                        speaker = 'chris'
                    elif any(name in speaker.lower() for name in ['guest', 'invité', 'expert']):
                        speaker = 'jessica'
                    else:
                        speaker = 'chris'  # Par défaut
                
                segments.append({
                    'speaker': speaker,
                    'text': text
                })
            else:
                # Ligne sans speaker, attribuer au dernier speaker ou chris
                speaker = segments[-1]['speaker'] if segments else 'chris'
                segments.append({
                    'speaker': speaker,
                    'text': line
                })
        
        return segments
    
    def generate_audio_segment(self, text, speaker, output_path):
        """Générer un segment audio pour un speaker"""
        voice_config = self.voices[speaker]
        
        tts = gTTS(
            text=text,
            lang=voice_config['lang'],
            tld=voice_config['tld'],
            slow=False
        )
        
        tts.save(str(output_path))
        return output_path
    
    def create_silence_mp3(self, output_path, duration_ms=500):
        """Créer un fichier MP3 de silence"""
        # Créer un WAV de silence
        wav_path = output_path.with_suffix('.wav')
        sample_rate = 22050
        num_samples = int(sample_rate * duration_ms / 1000)
        
        with wave.open(str(wav_path), 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            
            # Écrire des zéros (silence)
            for _ in range(num_samples):
                wav_file.writeframes(struct.pack('<h', 0))
        
        # Convertir en MP3 si ffmpeg est disponible
        try:
            subprocess.run([
                'ffmpeg', '-i', str(wav_path),
                '-codec:a', 'libmp3lame', '-qscale:a', '2',
                str(output_path), '-y'
            ], check=True, capture_output=True)
            wav_path.unlink()
        except:
            # Si ffmpeg n'est pas disponible, garder le WAV
            output_path.unlink(missing_ok=True)
            wav_path.rename(output_path)
        
        return output_path
    
    def create_podcast(self, script_text, output_path, add_music=False):
        """
        Créer le podcast complet
        
        Args:
            script_text: Le script du podcast
            output_path: Chemin de sortie du MP3
            add_music: Ajouter une intro/outro musicale
        """
        print("🎙️ Création du podcast...")
        print()
        
        # 1. Parser le script
        print("📝 Analyse du script...")
        segments = self.parse_script(script_text)
        print(f"✅ {len(segments)} segments détectés")
        
        # Compter les speakers
        speakers = set(seg['speaker'] for seg in segments)
        print(f"🗣️ {len(speakers)} speaker(s): {', '.join(speakers)}")
        print()
        
        # 2. Générer les segments audio
        print("🎤 Génération des segments audio...")
        temp_dir = Path("temp_podcast")
        temp_dir.mkdir(exist_ok=True)
        
        audio_files = []
        
        with tqdm(total=len(segments), desc="Segments", unit="seg") as pbar:
            for i, segment in enumerate(segments):
                temp_file = temp_dir / f"segment_{i:03d}.mp3"
                
                try:
                    self.generate_audio_segment(
                        segment['text'],
                        segment['speaker'],
                        temp_file
                    )
                    audio_files.append(temp_file)
                except Exception as e:
                    print(f"\n⚠️ Erreur segment {i}: {e}")
                    continue
                
                pbar.update(1)
        
        print()
        print("🔗 Assemblage du podcast...")
        
        # 3. Assembler tous les segments avec ffmpeg
        try:
            # Créer un fichier de liste pour ffmpeg
            concat_file = temp_dir / "concat_list.txt"
            
            with open(concat_file, 'w', encoding='utf-8') as f:
                for i, audio_file in enumerate(audio_files):
                    f.write(f"file '{audio_file.absolute()}'\n")
                    
                    # Ajouter silence entre segments
                    if i < len(audio_files) - 1:
                        silence_file = temp_dir / f"silence_{i}.mp3"
                        self.create_silence_mp3(silence_file, 300)
                        f.write(f"file '{silence_file.absolute()}'\n")
            
            # Assembler avec ffmpeg
            print("🔗 Assemblage avec ffmpeg...")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                subprocess.run([
                    'ffmpeg', '-f', 'concat', '-safe', '0',
                    '-i', str(concat_file),
                    '-c', 'copy',
                    str(output_path), '-y'
                ], check=True, capture_output=True)
                
            except FileNotFoundError:
                print("⚠️ ffmpeg non trouvé, assemblage simple...")
                # Fallback: copier juste le premier fichier
                import shutil
                shutil.copy(audio_files[0], output_path)
            
            # Nettoyer les fichiers temporaires
            print("🧹 Nettoyage...")
            for temp_file in temp_dir.glob("*"):
                temp_file.unlink()
            concat_file.unlink(missing_ok=True)
            temp_dir.rmdir()
            
            # Statistiques
            size_kb = output_path.stat().st_size / 1024
            
            # Estimer la durée (approximativement 150 chars = 1 seconde de parole)
            total_chars = sum(len(seg['text']) for seg in segments)
            duration_sec = total_chars / 150
            
            print()
            print("=" * 60)
            print("✅ PODCAST CRÉÉ AVEC SUCCÈS!")
            print("=" * 60)
            print(f"📁 Fichier: {output_path}")
            print(f"⏱️ Durée: {duration_sec:.1f} secondes ({duration_sec/60:.1f} minutes)")
            print(f"💾 Taille: {size_kb:.1f} Ko")
            print(f"🗣️ Speakers: {len(speakers)}")
            print(f"📝 Segments: {len(segments)}")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'assemblage: {e}")
            return False


def create_sample_script():
    """Créer un script de démonstration"""
    return """Host: Bonjou! Welcome to Kreyòl Podcast, the show where we explore Haitian culture and language.

Guest: Mèsi pou envitasyon an! Thank you for having me today.

Host: Today we're discussing the importance of preserving the Haitian Creole language. Can you tell us why this matters?

Guest: Well, Kreyòl is more than just a language - it's the heart of Haitian identity. When we speak Kreyòl, we connect with our ancestors and our culture.

Host: That's beautifully said. And technology can help preserve it, right?

Guest: Absolutely! Tools like this podcast creator make it easier to create content in Kreyòl. More content means more people engaging with the language.

Host: What would you say to someone who wants to learn Kreyòl?

Guest: I'd say: Don't be afraid! Kreyòl is a beautiful, expressive language. Start with simple phrases, listen to Haitian music, and most importantly - practice speaking!

Host: Excellent advice! Thank you so much for joining us today.

Guest: It was my pleasure. Mèsi anpil, and keep speaking Kreyòl!

Host: That's all for today's episode. Remember to subscribe and share with your friends. Kenbe fòm!"""


def main():
    """Fonction principale"""
    print("=" * 60)
    print("🎙️ PODCAST CREATOR - PWOJÈ KREYÒL IA")
    print("=" * 60)
    print()
    
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("Usage: python podcast_creator.py <script_file.txt>")
        print()
        print("Ou lancez sans argument pour créer un podcast de démonstration")
        print()
        
        # Créer un podcast de demo
        response = input("Créer un podcast de démo? (o/n): ")
        if response.lower() != 'o':
            return 1
        
        # Créer le script de démo
        demo_script = create_sample_script()
        
        # Sauvegarder le script
        script_path = Path("data/demo_podcast_script.txt")
        script_path.parent.mkdir(exist_ok=True)
        script_path.write_text(demo_script, encoding='utf-8')
        
        print(f"📝 Script de démo créé: {script_path}")
        print()
        
        script_text = demo_script
        output_path = Path("output/demo_podcast/demo_podcast.mp3")
        
    else:
        script_file = Path(sys.argv[1])
        
        if not script_file.exists():
            print(f"❌ Fichier introuvable: {script_file}")
            return 1
        
        print(f"📖 Lecture du script: {script_file.name}")
        script_text = script_file.read_text(encoding='utf-8')
        
        output_path = Path(f"output/{script_file.stem}/{script_file.stem}_podcast.mp3")
    
    # Créer le podcast
    creator = PodcastCreator()
    success = creator.create_podcast(script_text, output_path, add_music=False)
    
    if success:
        print()
        print("💡 Pour écouter:")
        print(f"   - Double-cliquez sur: {output_path}")
        print(f"   - Ou ouvrez avec votre lecteur audio")
        print()
        return 0
    else:
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️ Création interrompue")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

