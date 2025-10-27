"""
🎵 Générateur de Musique IA pour Faner Studio
Génération de musique de style haïtien avec IA
"""

import os
import numpy as np
from typing import Optional, Dict, List
import soundfile as sf
from pydub import AudioSegment
from pydub.generators import Sine, Square, Sawtooth
import random


class HaitianMusicGenerator:
    """Générateur de musique de style haïtien"""
    
    # Styles musicaux haïtiens
    MUSIC_STYLES = {
        'konpa': {
            'tempo': 120,  # BPM
            'rhythm_pattern': [1, 0, 1, 0, 1, 1, 0, 1],
            'key': 'C',
            'instruments': ['bass', 'drums', 'guitar', 'keyboard'],
            'description': 'Style Konpa traditionnel'
        },
        'rara': {
            'tempo': 140,
            'rhythm_pattern': [1, 1, 0, 1, 1, 0, 1, 0],
            'key': 'G',
            'instruments': ['drums', 'trumpet', 'bamboo', 'vocals'],
            'description': 'Style Rara festif'
        },
        'racine': {
            'tempo': 100,
            'rhythm_pattern': [1, 0, 0, 1, 1, 0, 1, 0],
            'key': 'Am',
            'instruments': ['drums', 'bass', 'vocals', 'percussion'],
            'description': 'Racine roots music'
        },
        'twoubadou': {
            'tempo': 90,
            'rhythm_pattern': [1, 0, 1, 0, 0, 1, 0, 1],
            'key': 'D',
            'instruments': ['guitar', 'maracas', 'vocals'],
            'description': 'Twoubadou folk music'
        },
        'zouk': {
            'tempo': 130,
            'rhythm_pattern': [1, 0, 1, 1, 0, 1, 0, 1],
            'key': 'F',
            'instruments': ['bass', 'drums', 'synth', 'guitar'],
            'description': 'Style Zouk moderne'
        },
        'rap_kreyol': {
            'tempo': 95,
            'rhythm_pattern': [1, 0, 0, 1, 0, 1, 0, 1],
            'key': 'Dm',
            'instruments': ['bass', 'drums', 'synth'],
            'description': 'Rap Kreyòl beats'
        }
    }
    
    # Notes musicales (Hz)
    NOTES = {
        'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
        'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
        'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
    }
    
    def __init__(self, sample_rate: int = 44100):
        """
        Initialise le générateur de musique
        
        Args:
            sample_rate: Taux d'échantillonnage (Hz)
        """
        self.sample_rate = sample_rate
        
    def generate_music(
        self,
        style: str = 'konpa',
        duration: int = 30,
        output_path: Optional[str] = None,
        add_melody: bool = True,
        add_bass: bool = True,
        add_drums: bool = True
    ) -> str:
        """
        Génère une piste musicale
        
        Args:
            style: Style musical ('konpa', 'rara', 'racine', etc.)
            duration: Durée en secondes
            output_path: Chemin de sortie (optionnel)
            add_melody: Ajouter une mélodie
            add_bass: Ajouter une ligne de basse
            add_drums: Ajouter des percussions
            
        Returns:
            Chemin du fichier audio généré
        """
        if style not in self.MUSIC_STYLES:
            raise ValueError(f"Style '{style}' non reconnu. Styles disponibles: {list(self.MUSIC_STYLES.keys())}")
        
        style_config = self.MUSIC_STYLES[style]
        
        # Créer une piste audio vide
        audio = AudioSegment.silent(duration=duration * 1000)
        
        # Ajouter les différentes couches
        if add_drums:
            drums = self._generate_drums(style_config, duration)
            audio = audio.overlay(drums)
        
        if add_bass:
            bass = self._generate_bass(style_config, duration)
            audio = audio.overlay(bass)
        
        if add_melody:
            melody = self._generate_melody(style_config, duration)
            audio = audio.overlay(melody)
        
        # Normaliser le volume
        audio = audio.normalize()
        
        # Sauvegarder
        if output_path is None:
            output_dir = "projet_kreyol_IA/output/music"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{style}_music_{duration}s.mp3")
        
        audio.export(output_path, format="mp3", bitrate="192k")
        
        return output_path
    
    def _generate_drums(self, style_config: Dict, duration: int) -> AudioSegment:
        """Génère une piste de percussion"""
        tempo = style_config['tempo']
        pattern = style_config['rhythm_pattern']
        
        # Durée d'un beat en ms
        beat_duration = int((60 / tempo) * 1000)
        
        # Créer les sons de percussion
        kick = self._create_kick()
        snare = self._create_snare()
        hihat = self._create_hihat()
        
        # Piste vide
        drums = AudioSegment.silent(duration=duration * 1000)
        
        # Ajouter les patterns
        position = 0
        pattern_length = len(pattern)
        
        while position < duration * 1000:
            for i, hit in enumerate(pattern):
                if hit and position < duration * 1000:
                    # Varier les instruments selon la position
                    if i % 4 == 0:
                        drums = drums.overlay(kick, position=position)
                    elif i % 2 == 0:
                        drums = drums.overlay(snare, position=position)
                    drums = drums.overlay(hihat, position=position)
                
                position += beat_duration
        
        # Ajuster le volume
        drums = drums - 6  # Réduire de 6dB
        
        return drums
    
    def _generate_bass(self, style_config: Dict, duration: int) -> AudioSegment:
        """Génère une ligne de basse"""
        tempo = style_config['tempo']
        key = style_config['key']
        
        # Notes de basse (fondamentale et quinte)
        root_freq = self.NOTES.get(key, 261.63)
        fifth_freq = root_freq * 1.5  # Quinte parfaite
        
        # Durée d'une note
        note_duration = int((60 / tempo) * 1000 * 2)  # 2 beats par note
        
        bass = AudioSegment.silent(duration=duration * 1000)
        
        position = 0
        alternate = True
        
        while position < duration * 1000:
            freq = root_freq if alternate else fifth_freq
            note = self._create_bass_note(freq, note_duration)
            bass = bass.overlay(note, position=position)
            
            position += note_duration
            alternate = not alternate
        
        # Ajuster le volume
        bass = bass - 3
        
        return bass
    
    def _generate_melody(self, style_config: Dict, duration: int) -> AudioSegment:
        """Génère une mélodie"""
        tempo = style_config['tempo']
        key = style_config['key']
        
        # Gamme pentatonique pour simplicité
        root_freq = self.NOTES.get(key, 261.63)
        scale = [
            root_freq,
            root_freq * 1.125,  # 2nde majeure
            root_freq * 1.25,   # 3ce majeure
            root_freq * 1.5,    # 5te
            root_freq * 1.667   # 6te
        ]
        
        note_duration = int((60 / tempo) * 1000)
        
        melody = AudioSegment.silent(duration=duration * 1000)
        
        position = 0
        
        while position < duration * 1000:
            # Sélectionner une note aléatoire de la gamme
            freq = random.choice(scale)
            note = self._create_melody_note(freq, note_duration)
            melody = melody.overlay(note, position=position)
            
            position += note_duration
        
        # Ajuster le volume
        melody = melody - 9
        
        return melody
    
    def _create_kick(self) -> AudioSegment:
        """Crée un son de grosse caisse"""
        duration = 500  # ms
        # Fréquence décroissante pour simuler un kick
        kick = Sine(60).to_audio_segment(duration=duration)
        kick = kick.fade_out(400)
        return kick
    
    def _create_snare(self) -> AudioSegment:
        """Crée un son de caisse claire"""
        duration = 200
        # Utiliser du bruit blanc (simulé avec une onde carrée haute fréquence)
        snare = Square(200).to_audio_segment(duration=duration)
        snare = snare.fade_out(150)
        return snare
    
    def _create_hihat(self) -> AudioSegment:
        """Crée un son de charleston"""
        duration = 100
        hihat = Square(8000).to_audio_segment(duration=duration)
        hihat = hihat.fade_out(80) - 15  # Plus discret
        return hihat
    
    def _create_bass_note(self, frequency: float, duration: int) -> AudioSegment:
        """Crée une note de basse"""
        note = Sine(frequency / 2).to_audio_segment(duration=duration)
        note = note.fade_in(10).fade_out(100)
        return note
    
    def _create_melody_note(self, frequency: float, duration: int) -> AudioSegment:
        """Crée une note de mélodie"""
        note = Sawtooth(frequency).to_audio_segment(duration=duration)
        note = note.fade_in(20).fade_out(50)
        return note
    
    def mix_music_with_voice(
        self,
        voice_path: str,
        music_path: Optional[str] = None,
        style: str = 'konpa',
        music_volume: int = -20,
        output_path: Optional[str] = None
    ) -> str:
        """
        Mixe une voix avec de la musique de fond
        
        Args:
            voice_path: Chemin du fichier vocal
            music_path: Chemin de la musique (optionnel, sera généré si absent)
            style: Style musical si génération automatique
            music_volume: Volume de la musique en dB (négatif pour réduire)
            output_path: Chemin de sortie
            
        Returns:
            Chemin du fichier mixé
        """
        # Charger la voix
        voice = AudioSegment.from_file(voice_path)
        voice_duration = len(voice) / 1000  # en secondes
        
        # Générer ou charger la musique
        if music_path is None:
            music_path = self.generate_music(
                style=style,
                duration=int(voice_duration) + 5  # 5s de plus que la voix
            )
        
        music = AudioSegment.from_file(music_path)
        
        # Ajuster la durée de la musique
        if len(music) < len(voice):
            # Boucler la musique si elle est plus courte
            loops_needed = int(len(voice) / len(music)) + 1
            music = music * loops_needed
        
        music = music[:len(voice)]
        
        # Ajuster le volume de la musique
        music = music + music_volume
        
        # Mixer
        mixed = voice.overlay(music)
        
        # Normaliser
        mixed = mixed.normalize()
        
        # Sauvegarder
        if output_path is None:
            output_dir = "projet_kreyol_IA/output/mixed"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, "mixed_audio.mp3")
        
        mixed.export(output_path, format="mp3", bitrate="192k")
        
        return output_path
    
    def create_beat(
        self,
        style: str = 'konpa',
        bars: int = 8,
        output_path: Optional[str] = None
    ) -> str:
        """
        Crée un beat instrumental simple
        
        Args:
            style: Style musical
            bars: Nombre de mesures (4 temps par mesure)
            output_path: Chemin de sortie
            
        Returns:
            Chemin du beat généré
        """
        if style not in self.MUSIC_STYLES:
            style = 'konpa'
        
        style_config = self.MUSIC_STYLES[style]
        tempo = style_config['tempo']
        
        # Calculer la durée (4 beats par mesure)
        duration = int((60 / tempo) * 4 * bars)
        
        return self.generate_music(
            style=style,
            duration=duration,
            output_path=output_path,
            add_melody=False,
            add_bass=True,
            add_drums=True
        )
    
    @classmethod
    def get_available_styles(cls) -> Dict[str, str]:
        """Retourne les styles disponibles avec leurs descriptions"""
        return {
            style: config['description']
            for style, config in cls.MUSIC_STYLES.items()
        }


# Fonctions utilitaires
def generate_background_music(
    style: str = 'konpa',
    duration: int = 30,
    output_path: Optional[str] = None
) -> str:
    """
    Fonction rapide pour générer de la musique de fond
    
    Args:
        style: Style musical haïtien
        duration: Durée en secondes
        output_path: Chemin de sortie
        
    Returns:
        Chemin du fichier généré
    """
    generator = HaitianMusicGenerator()
    return generator.generate_music(style, duration, output_path)


def mix_audio_files(
    voice_path: str,
    music_path: Optional[str] = None,
    style: str = 'konpa',
    output_path: Optional[str] = None
) -> str:
    """
    Mixe un fichier vocal avec de la musique
    
    Args:
        voice_path: Chemin du fichier vocal
        music_path: Chemin de la musique (optionnel)
        style: Style musical si génération
        output_path: Chemin de sortie
        
    Returns:
        Chemin du fichier mixé
    """
    generator = HaitianMusicGenerator()
    return generator.mix_music_with_voice(voice_path, music_path, style, output_path=output_path)


if __name__ == "__main__":
    # Test du générateur
    print("🎵 Test du générateur de musique haïtienne")
    print("\nStyles disponibles:")
    for style, desc in HaitianMusicGenerator.get_available_styles().items():
        print(f"  • {style}: {desc}")
    
    # Générer un exemple de chaque style
    generator = HaitianMusicGenerator()
    
    print("\n🎼 Génération d'exemples de musique...")
    for style in ['konpa', 'rara', 'racine']:
        output = generator.generate_music(style=style, duration=15)
        print(f"✅ {style}: {output}")
    
    print("\n✨ Test terminé!")

