# 🎙️ VOICE PROFILES - Multi-Voice Support

## Configuration for Voice Variations

This module provides multiple voice profiles using pitch/speed modifications
on the base facebook/mms-tts-hat model to create distinct voices.

"""

import numpy as np
from scipy import signal
from typing import Dict, Any

class VoiceProfile:
    """
    Voice profile with pitch/speed/effect modifications
    """
    
    PROFILES = {
        "creole-male-default": {
            "name": "🇭🇹 Gason Kreyòl (Default)",
            "description": "Natural Haitian Creole male voice",
            "pitch_shift": 0,
            "speed": 1.0,
            "volume": 1.0,
            "gender": "male",
            "age": "adult"
        },
        "creole-male-deep": {
            "name": "🇭🇹 Gason Kreyòl (Grav)",
            "description": "Deep Haitian Creole male voice",
            "pitch_shift": -2,
            "speed": 0.95,
            "volume": 1.1,
            "gender": "male",
            "age": "mature"
        },
        "creole-female-sim": {
            "name": "🇭🇹 Fanm Kreyòl (Simile)",
            "description": "Simulated Haitian Creole female voice",
            "pitch_shift": 3,
            "speed": 1.05,
            "volume": 0.95,
            "gender": "female",
            "age": "adult"
        },
        "creole-narrator": {
            "name": "🇭🇹 Naratè Kreyòl",
            "description": "Professional narrator voice",
            "pitch_shift": -1,
            "speed": 0.90,
            "volume": 1.05,
            "gender": "male",
            "age": "mature"
        }
    }
    
    @classmethod
    def get_profile(cls, profile_id: str) -> Dict[str, Any]:
        """Get voice profile by ID"""
        return cls.PROFILES.get(profile_id, cls.PROFILES["creole-male-default"])
    
    @classmethod
    def list_profiles(cls) -> Dict[str, Dict[str, Any]]:
        """List all available voice profiles"""
        return cls.PROFILES.copy()
    
    @staticmethod
    def apply_profile(audio: np.ndarray, profile: Dict[str, Any], sample_rate: int) -> np.ndarray:
        """
        Apply voice profile transformations to audio
        
        Args:
            audio: Input audio array
            profile: Voice profile dictionary
            sample_rate: Audio sample rate
            
        Returns:
            Modified audio array
        """
        # Apply pitch shift
        pitch_shift = profile.get("pitch_shift", 0)
        if pitch_shift != 0:
            audio = VoiceProfile._pitch_shift(audio, pitch_shift, sample_rate)
        
        # Apply speed change
        speed = profile.get("speed", 1.0)
        if speed != 1.0:
            audio = VoiceProfile._change_speed(audio, speed)
        
        # Apply volume adjustment
        volume = profile.get("volume", 1.0)
        if volume != 1.0:
            audio = audio * volume
        
        # Normalize to prevent clipping
        if np.max(np.abs(audio)) > 0:
            audio = audio / np.max(np.abs(audio))
        
        return audio
    
    @staticmethod
    def _pitch_shift(audio: np.ndarray, semitones: float, sample_rate: int) -> np.ndarray:
        """
        Shift pitch of audio by semitones
        
        Args:
            audio: Input audio
            semitones: Number of semitones to shift (positive = higher, negative = lower)
            sample_rate: Sample rate
            
        Returns:
            Pitch-shifted audio
        """
        # Calculate pitch shift factor
        factor = 2 ** (semitones / 12.0)
        
        # Use resampling to shift pitch
        # This is a simple method; more advanced methods exist
        indices = np.round(np.arange(0, len(audio), factor))
        indices = indices[indices < len(audio)].astype(int)
        
        return audio[indices]
    
    @staticmethod
    def _change_speed(audio: np.ndarray, speed: float) -> np.ndarray:
        """
        Change speed of audio
        
        Args:
            audio: Input audio
            speed: Speed factor (1.0 = normal, 0.5 = half speed, 2.0 = double speed)
            
        Returns:
            Speed-changed audio
        """
        indices = np.round(np.arange(0, len(audio), speed))
        indices = indices[indices < len(audio)].astype(int)
        
        return audio[indices]
    
    @staticmethod
    def add_reverb(audio: np.ndarray, room_size: float = 0.3) -> np.ndarray:
        """
        Add simple reverb effect
        
        Args:
            audio: Input audio
            room_size: Room size factor (0.0 to 1.0)
            
        Returns:
            Audio with reverb
        """
        # Simple delay-based reverb
        delay_samples = int(len(audio) * room_size * 0.05)
        reverb = np.zeros_like(audio)
        
        if delay_samples > 0 and delay_samples < len(audio):
            reverb[delay_samples:] = audio[:-delay_samples] * 0.3
            audio = audio + reverb
        
        # Normalize
        if np.max(np.abs(audio)) > 0:
            audio = audio / np.max(np.abs(audio))
        
        return audio


# Helper functions for easy access

def get_available_voices():
    """Get list of available voice profiles"""
    profiles = VoiceProfile.list_profiles()
    return [
        {
            "id": voice_id,
            "name": profile["name"],
            "description": profile["description"],
            "gender": profile["gender"],
            "age": profile["age"]
        }
        for voice_id, profile in profiles.items()
    ]


def apply_voice_effect(audio: np.ndarray, voice_id: str, sample_rate: int) -> np.ndarray:
    """
    Apply voice effect to audio
    
    Args:
        audio: Input audio array
        voice_id: Voice profile ID
        sample_rate: Audio sample rate
        
    Returns:
        Modified audio
    """
    profile = VoiceProfile.get_profile(voice_id)
    return VoiceProfile.apply_profile(audio, profile, sample_rate)

