"""
🎛️ Module d'édition audio avancée pour Faner Studio
Fonctionnalités: Normalisation, égalisation, effets, compression, etc.
"""

import os
import numpy as np
from typing import Optional, Tuple, List
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
import soundfile as sf
from scipy import signal


class AudioEditor:
    """Éditeur audio avancé avec effets et traitement"""
    
    def __init__(self):
        """Initialise l'éditeur audio"""
        pass
    
    def normalize_audio(
        self,
        input_path: str,
        target_dbfs: float = -20.0,
        output_path: Optional[str] = None
    ) -> str:
        """
        Normalise le volume audio
        
        Args:
            input_path: Chemin du fichier d'entrée
            target_dbfs: Niveau cible en dBFS
            output_path: Chemin de sortie
            
        Returns:
            Chemin du fichier normalisé
        """
        audio = AudioSegment.from_file(input_path)
        
        # Normaliser
        normalized = normalize(audio, headroom=0.1)
        
        # Ajuster au niveau cible
        change_in_dbfs = target_dbfs - normalized.dBFS
        normalized = normalized.apply_gain(change_in_dbfs)
        
        if output_path is None:
            output_path = self._generate_output_path(input_path, "_normalized")
        
        normalized.export(output_path, format="mp3", bitrate="192k")
        return output_path
    
    def apply_fade(
        self,
        input_path: str,
        fade_in_ms: int = 1000,
        fade_out_ms: int = 1000,
        output_path: Optional[str] = None
    ) -> str:
        """
        Applique des fondus d'entrée et de sortie
        
        Args:
            input_path: Fichier d'entrée
            fade_in_ms: Durée du fondu d'entrée (ms)
            fade_out_ms: Durée du fondu de sortie (ms)
            output_path: Fichier de sortie
            
        Returns:
            Chemin du fichier traité
        """
        audio = AudioSegment.from_file(input_path)
        
        audio = audio.fade_in(fade_in_ms).fade_out(fade_out_ms)
        
        if output_path is None:
            output_path = self._generate_output_path(input_path, "_faded")
        
        audio.export(output_path, format="mp3", bitrate="192k")
        return output_path
    
    def change_speed(
        self,
        input_path: str,
        speed_factor: float = 1.0,
        output_path: Optional[str] = None
    ) -> str:
        """
        Change la vitesse de lecture
        
        Args:
            input_path: Fichier d'entrée
            speed_factor: Facteur de vitesse (1.0 = normal, 2.0 = 2x plus rapide)
            output_path: Fichier de sortie
            
        Returns:
            Chemin du fichier traité
        """
        audio = AudioSegment.from_file(input_path)
        
        # Changer la vitesse en modifiant le frame rate
        new_frame_rate = int(audio.frame_rate * speed_factor)
        audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_frame_rate})
        audio = audio.set_frame_rate(44100)  # Reconvertir au frame rate standard
        
        if output_path is None:
            output_path = self._generate_output_path(input_path, f"_speed{speed_factor}")
        
        audio.export(output_path, format="mp3", bitrate="192k")
        return output_path
    
    def apply_reverb(
        self,
        input_path: str,
        room_size: float = 0.5,
        damping: float = 0.5,
        output_path: Optional[str] = None
    ) -> str:
        """
        Applique un effet de réverbération
        
        Args:
            input_path: Fichier d'entrée
            room_size: Taille de la pièce (0-1)
            damping: Amortissement (0-1)
            output_path: Fichier de sortie
            
        Returns:
            Chemin du fichier traité
        """
        audio = AudioSegment.from_file(input_path)
        
        # Simuler réverbération simple avec délais
        delay_ms = int(room_size * 100)
        reverb = audio - (20 * damping)  # Réduire le volume
        
        # Ajouter plusieurs échos
        result = audio
        for i in range(3):
            delay = delay_ms * (i + 1)
            decay = (1 - damping) ** (i + 1) * 10
            result = result.overlay(reverb - decay, position=delay)
        
        if output_path is None:
            output_path = self._generate_output_path(input_path, "_reverb")
        
        result.export(output_path, format="mp3", bitrate="192k")
        return output_path
    
    def apply_compression(
        self,
        input_path: str,
        threshold: float = -20.0,
        ratio: float = 4.0,
        output_path: Optional[str] = None
    ) -> str:
        """
        Applique une compression dynamique
        
        Args:
            input_path: Fichier d'entrée
            threshold: Seuil de compression (dB)
            ratio: Ratio de compression
            output_path: Fichier de sortie
            
        Returns:
            Chemin du fichier compressé
        """
        audio = AudioSegment.from_file(input_path)
        
        compressed = compress_dynamic_range(
            audio,
            threshold=threshold,
            ratio=ratio
        )
        
        if output_path is None:
            output_path = self._generate_output_path(input_path, "_compressed")
        
        compressed.export(output_path, format="mp3", bitrate="192k")
        return output_path
    
    def apply_eq(
        self,
        input_path: str,
        bass_gain: float = 0.0,
        mid_gain: float = 0.0,
        treble_gain: float = 0.0,
        output_path: Optional[str] = None
    ) -> str:
        """
        Applique une égalisation 3 bandes
        
        Args:
            input_path: Fichier d'entrée
            bass_gain: Gain des basses (dB) -12 à +12
            mid_gain: Gain des médiums (dB) -12 à +12
            treble_gain: Gain des aigus (dB) -12 à +12
            output_path: Fichier de sortie
            
        Returns:
            Chemin du fichier égalisé
        """
        audio = AudioSegment.from_file(input_path)
        
        # Appliquer les gains par bande de fréquence
        # Simplification: appliquer un gain général basé sur la moyenne
        avg_gain = (bass_gain + mid_gain + treble_gain) / 3
        
        audio = audio + avg_gain
        
        if output_path is None:
            output_path = self._generate_output_path(input_path, "_eq")
        
        audio.export(output_path, format="mp3", bitrate="192k")
        return output_path
    
    def trim_audio(
        self,
        input_path: str,
        start_ms: int = 0,
        end_ms: Optional[int] = None,
        output_path: Optional[str] = None
    ) -> str:
        """
        Coupe l'audio
        
        Args:
            input_path: Fichier d'entrée
            start_ms: Début en millisecondes
            end_ms: Fin en millisecondes (None = jusqu'à la fin)
            output_path: Fichier de sortie
            
        Returns:
            Chemin du fichier coupé
        """
        audio = AudioSegment.from_file(input_path)
        
        if end_ms is None:
            end_ms = len(audio)
        
        trimmed = audio[start_ms:end_ms]
        
        if output_path is None:
            output_path = self._generate_output_path(input_path, "_trimmed")
        
        trimmed.export(output_path, format="mp3", bitrate="192k")
        return output_path
    
    def concatenate_audio(
        self,
        audio_paths: List[str],
        crossfade_ms: int = 0,
        output_path: Optional[str] = None
    ) -> str:
        """
        Concatène plusieurs fichiers audio
        
        Args:
            audio_paths: Liste des chemins de fichiers
            crossfade_ms: Durée du fondu enchaîné (ms)
            output_path: Fichier de sortie
            
        Returns:
            Chemin du fichier concaténé
        """
        if not audio_paths:
            raise ValueError("Liste de fichiers vide")
        
        result = AudioSegment.from_file(audio_paths[0])
        
        for path in audio_paths[1:]:
            audio = AudioSegment.from_file(path)
            if crossfade_ms > 0:
                result = result.append(audio, crossfade=crossfade_ms)
            else:
                result = result + audio
        
        if output_path is None:
            output_dir = "projet_kreyol_IA/output/concatenated"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, "concatenated_audio.mp3")
        
        result.export(output_path, format="mp3", bitrate="192k")
        return output_path
    
    def remove_silence(
        self,
        input_path: str,
        silence_thresh: int = -40,
        min_silence_len: int = 1000,
        output_path: Optional[str] = None
    ) -> str:
        """
        Supprime les silences
        
        Args:
            input_path: Fichier d'entrée
            silence_thresh: Seuil de silence (dB)
            min_silence_len: Durée minimale de silence (ms)
            output_path: Fichier de sortie
            
        Returns:
            Chemin du fichier traité
        """
        from pydub.silence import detect_nonsilent
        
        audio = AudioSegment.from_file(input_path)
        
        # Détecter les parties non-silencieuses
        nonsilent_ranges = detect_nonsilent(
            audio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh
        )
        
        # Extraire et concaténer les parties non-silencieuses
        result = AudioSegment.empty()
        for start, end in nonsilent_ranges:
            result += audio[start:end]
        
        if output_path is None:
            output_path = self._generate_output_path(input_path, "_no_silence")
        
        result.export(output_path, format="mp3", bitrate="192k")
        return output_path
    
    def change_pitch(
        self,
        input_path: str,
        semitones: int = 0,
        output_path: Optional[str] = None
    ) -> str:
        """
        Change la hauteur tonale
        
        Args:
            input_path: Fichier d'entrée
            semitones: Nombre de demi-tons (-12 à +12)
            output_path: Fichier de sortie
            
        Returns:
            Chemin du fichier traité
        """
        audio = AudioSegment.from_file(input_path)
        
        # Changer la hauteur en modifiant le frame rate sans changer la vitesse
        octaves = semitones / 12.0
        new_sample_rate = int(audio.frame_rate * (2.0 ** octaves))
        
        audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})
        audio = audio.set_frame_rate(44100)
        
        if output_path is None:
            output_path = self._generate_output_path(input_path, f"_pitch{semitones:+d}")
        
        audio.export(output_path, format="mp3", bitrate="192k")
        return output_path
    
    def apply_multiple_effects(
        self,
        input_path: str,
        effects: List[dict],
        output_path: Optional[str] = None
    ) -> str:
        """
        Applique plusieurs effets en séquence
        
        Args:
            input_path: Fichier d'entrée
            effects: Liste de dictionnaires d'effets
                     Ex: [{'type': 'normalize', 'params': {...}}, ...]
            output_path: Fichier de sortie
            
        Returns:
            Chemin du fichier traité
        """
        current_path = input_path
        temp_files = []
        
        for i, effect in enumerate(effects):
            effect_type = effect.get('type')
            params = effect.get('params', {})
            
            # Créer un fichier temporaire
            temp_output = self._generate_output_path(input_path, f"_temp_{i}")
            temp_files.append(temp_output)
            
            # Appliquer l'effet
            if effect_type == 'normalize':
                current_path = self.normalize_audio(current_path, output_path=temp_output, **params)
            elif effect_type == 'fade':
                current_path = self.apply_fade(current_path, output_path=temp_output, **params)
            elif effect_type == 'compression':
                current_path = self.apply_compression(current_path, output_path=temp_output, **params)
            elif effect_type == 'eq':
                current_path = self.apply_eq(current_path, output_path=temp_output, **params)
            elif effect_type == 'reverb':
                current_path = self.apply_reverb(current_path, output_path=temp_output, **params)
            elif effect_type == 'speed':
                current_path = self.change_speed(current_path, output_path=temp_output, **params)
            elif effect_type == 'pitch':
                current_path = self.change_pitch(current_path, output_path=temp_output, **params)
        
        # Copier le résultat final
        if output_path is None:
            output_path = self._generate_output_path(input_path, "_processed")
        
        audio = AudioSegment.from_file(current_path)
        audio.export(output_path, format="mp3", bitrate="192k")
        
        # Nettoyer les fichiers temporaires
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        return output_path
    
    def get_audio_info(self, input_path: str) -> dict:
        """
        Récupère les informations d'un fichier audio
        
        Args:
            input_path: Chemin du fichier
            
        Returns:
            Dictionnaire avec les informations
        """
        audio = AudioSegment.from_file(input_path)
        
        return {
            'duration_ms': len(audio),
            'duration_seconds': len(audio) / 1000.0,
            'channels': audio.channels,
            'sample_width': audio.sample_width,
            'frame_rate': audio.frame_rate,
            'frame_width': audio.frame_width,
            'db_fs': audio.dBFS,
            'max_db_fs': audio.max_dBFS,
            'file_size_mb': os.path.getsize(input_path) / (1024 * 1024)
        }
    
    def _generate_output_path(self, input_path: str, suffix: str) -> str:
        """Génère un chemin de sortie automatique"""
        output_dir = "projet_kreyol_IA/output/edited"
        os.makedirs(output_dir, exist_ok=True)
        
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        
        return os.path.join(output_dir, f"{name}{suffix}.mp3")


# Présets d'effets
EFFECT_PRESETS = {
    'podcast': [
        {'type': 'normalize', 'params': {'target_dbfs': -16.0}},
        {'type': 'compression', 'params': {'threshold': -20.0, 'ratio': 3.0}},
        {'type': 'eq', 'params': {'bass_gain': 2.0, 'mid_gain': 1.0, 'treble_gain': -1.0}}
    ],
    'music': [
        {'type': 'normalize', 'params': {'target_dbfs': -14.0}},
        {'type': 'eq', 'params': {'bass_gain': 3.0, 'mid_gain': 0.0, 'treble_gain': 2.0}},
        {'type': 'compression', 'params': {'threshold': -18.0, 'ratio': 2.5}}
    ],
    'voice': [
        {'type': 'normalize', 'params': {'target_dbfs': -18.0}},
        {'type': 'eq', 'params': {'bass_gain': -2.0, 'mid_gain': 3.0, 'treble_gain': 1.0}},
        {'type': 'compression', 'params': {'threshold': -22.0, 'ratio': 4.0}}
    ],
    'radio': [
        {'type': 'normalize', 'params': {'target_dbfs': -16.0}},
        {'type': 'compression', 'params': {'threshold': -18.0, 'ratio': 5.0}},
        {'type': 'eq', 'params': {'bass_gain': -3.0, 'mid_gain': 4.0, 'treble_gain': 2.0}}
    ]
}


def apply_preset(input_path: str, preset_name: str, output_path: Optional[str] = None) -> str:
    """
    Applique un preset d'effets
    
    Args:
        input_path: Fichier d'entrée
        preset_name: Nom du preset ('podcast', 'music', 'voice', 'radio')
        output_path: Fichier de sortie
        
    Returns:
        Chemin du fichier traité
    """
    if preset_name not in EFFECT_PRESETS:
        raise ValueError(f"Preset '{preset_name}' non trouvé. Presets disponibles: {list(EFFECT_PRESETS.keys())}")
    
    editor = AudioEditor()
    return editor.apply_multiple_effects(input_path, EFFECT_PRESETS[preset_name], output_path)


if __name__ == "__main__":
    print("🎛️ Test de l'éditeur audio avancé")
    print("\nPresets disponibles:")
    for preset in EFFECT_PRESETS.keys():
        print(f"  • {preset}")

