#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Podcast Creator - Version avec Hugging Face
Utilise des voix natives créoles et détection automatique
"""

import sys
from pathlib import Path
import torch
from transformers import VitsModel, AutoTokenizer
import numpy as np
from pydub import AudioSegment
import scipy.io.wavfile as wavfile
import re
from tqdm import tqdm

class AdvancedPodcastCreator:
    """Créateur de podcasts avancé avec voix natives"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.voices_config = {
            'host': {
                'name': 'Chris (Host)',
                'model': 'facebook/mms-tts-hat',  # Créole natif
                'pitch_shift': 0,
                'speed': 1.0
            },
            'guest': {
                'name': 'Jessica (Guest)',
                'model': 'facebook/mms-tts-hat',
                'pitch_shift': 2,  # Voix plus aiguë
                'speed': 0.95
            },
            'narrator': {
                'name': 'Narrator',
                'model': 'facebook/mms-tts-hat',
                'pitch_shift': -1,
                'speed': 0.90
            }
        }
        
    def load_model(self, model_name="facebook/mms-tts-hat"):
        """Charger le modèle TTS"""
        if self.model is None:
            print(f"📥 Chargement du modèle {model_name}...")
            try:
                self.model = VitsModel.from_pretrained(model_name)
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                print("✅ Modèle chargé!")
            except Exception as e:
                print(f"⚠️ Erreur de chargement: {e}")
                print("💡 Utilisation du fallback gTTS...")
                return False
        return True
    
    def auto_detect_speakers(self, script_text):
        """
        Détecter automatiquement les speakers dans le script
        """
        lines = script_text.strip().split('\n')
        speakers_found = set()
        
        for line in lines:
            match = re.match(r'^([^:]+):', line)
            if match:
                speaker = match.group(1).strip().lower()
                speakers_found.add(speaker)
        
        # Mapper aux voix disponibles
        speaker_mapping = {}
        available_voices = list(self.voices_config.keys())
        
        for i, speaker in enumerate(sorted(speakers_found)):
            if i < len(available_voices):
                speaker_mapping[speaker] = available_voices[i]
            else:
                # Si plus de speakers que de voix, réutiliser
                speaker_mapping[speaker] = available_voices[i % len(available_voices)]
        
        return speaker_mapping
    
    def parse_script_with_detection(self, script_text):
        """Parser avec détection automatique"""
        lines = script_text.strip().split('\n')
        segments = []
        speaker_mapping = self.auto_detect_speakers(script_text)
        
        print(f"\n🔍 Speakers détectés:")
        for original, mapped in speaker_mapping.items():
            voice_info = self.voices_config[mapped]
            print(f"   - {original.title()} → {voice_info['name']}")
        print()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            match = re.match(r'^([^:]+):\s*(.+)$', line)
            if match:
                original_speaker = match.group(1).strip().lower()
                text = match.group(2).strip()
                
                voice = speaker_mapping.get(original_speaker, 'host')
                
                segments.append({
                    'speaker': voice,
                    'original_name': original_speaker,
                    'text': text
                })
        
        return segments
    
    def generate_segment_hf(self, text, voice_config, output_path):
        """Générer audio avec Hugging Face"""
        try:
            # Tokenizer
            inputs = self.tokenizer(text, return_tensors="pt")
            
            # Générer
            with torch.no_grad():
                output = self.model(**inputs).waveform
            
            # Convertir
            audio_np = output.squeeze().cpu().numpy()
            
            # Normaliser
            audio_np = audio_np / np.max(np.abs(audio_np))
            audio_int16 = (audio_np * 32767).astype(np.int16)
            
            # Sauvegarder WAV temporaire
            wav_path = output_path.with_suffix('.wav')
            wavfile.write(
                str(wav_path),
                rate=self.model.config.sampling_rate,
                data=audio_int16
            )
            
            # Convertir en MP3 avec modification de pitch/speed
            audio = AudioSegment.from_wav(str(wav_path))
            
            # Appliquer pitch shift
            if voice_config['pitch_shift'] != 0:
                # Approximation simple du pitch shift
                new_sample_rate = int(audio.frame_rate * (1.0 + voice_config['pitch_shift'] * 0.05))
                audio = audio._spawn(audio.raw_data, overrides={
                    "frame_rate": new_sample_rate
                })
                audio = audio.set_frame_rate(44100)
            
            # Appliquer speed
            if voice_config['speed'] != 1.0:
                audio = audio.speedup(playback_speed=voice_config['speed'])
            
            # Exporter MP3
            audio.export(str(output_path), format="mp3")
            
            # Nettoyer WAV
            wav_path.unlink()
            
            return True
            
        except Exception as e:
            print(f"⚠️ Erreur HF: {e}")
            return False
    
    def create_advanced_podcast(self, script_text, output_path):
        """Créer un podcast avancé"""
        print("🎙️ CRÉATION DE PODCAST AVANCÉ")
        print("=" * 60)
        
        # Charger le modèle
        use_hf = self.load_model()
        
        # Parser avec détection auto
        segments = self.parse_script_with_detection(script_text)
        print(f"📝 {len(segments)} segments à générer")
        print()
        
        # Générer les segments
        temp_dir = Path("temp_podcast_advanced")
        temp_dir.mkdir(exist_ok=True)
        
        audio_files = []
        
        print("🎤 Génération audio...")
        with tqdm(total=len(segments), desc="Segments", unit="seg") as pbar:
            for i, segment in enumerate(segments):
                temp_file = temp_dir / f"seg_{i:03d}.mp3"
                voice_config = self.voices_config[segment['speaker']]
                
                if use_hf:
                    success = self.generate_segment_hf(
                        segment['text'],
                        voice_config,
                        temp_file
                    )
                else:
                    # Fallback gTTS
                    from gtts import gTTS
                    tts = gTTS(text=segment['text'], lang='fr')
                    tts.save(str(temp_file))
                    success = True
                
                if success:
                    audio_files.append(temp_file)
                
                pbar.update(1)
        
        # Assembler
        print("\n🔗 Assemblage...")
        podcast = AudioSegment.empty()
        
        for audio_file in audio_files:
            segment_audio = AudioSegment.from_mp3(str(audio_file))
            podcast += segment_audio
            podcast += AudioSegment.silent(duration=400)
        
        # Normaliser et exporter
        podcast = podcast.normalize()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        podcast.export(str(output_path), format="mp3", bitrate="192k")
        
        # Nettoyer
        for f in audio_files:
            f.unlink()
        temp_dir.rmdir()
        
        # Stats
        duration = len(podcast) / 1000
        size = output_path.stat().st_size / 1024
        
        print("\n" + "=" * 60)
        print("✅ PODCAST AVANCÉ CRÉÉ!")
        print("=" * 60)
        print(f"📁 Fichier: {output_path}")
        print(f"⏱️ Durée: {duration:.1f}s ({duration/60:.1f} min)")
        print(f"💾 Taille: {size:.1f} Ko")
        print(f"🎙️ Voix utilisées: {use_hf and 'Créole natif (HF)' or 'gTTS (fallback)'}")
        print("=" * 60)


def main():
    """Main"""
    print("🇭🇹 ADVANCED PODCAST CREATOR")
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python podcast_advanced.py <script.txt>")
        return 1
    
    script_file = Path(sys.argv[1])
    if not script_file.exists():
        print(f"❌ Fichier introuvable: {script_file}")
        return 1
    
    script_text = script_file.read_text(encoding='utf-8')
    output_path = Path(f"output/{script_file.stem}/{script_file.stem}_advanced.mp3")
    
    creator = AdvancedPodcastCreator()
    creator.create_advanced_podcast(script_text, output_path)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

