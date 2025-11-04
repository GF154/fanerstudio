#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎤 Advanced Voice Cloning for Haitian Creole
Klonaj Vwa Avanse pou Kreyòl Ayisyen

Supports 3 methods:
1. Basic: Audio analysis + voice profile (FREE)
2. Medium: RVC voice cloning (OPEN SOURCE)
3. Premium: ElevenLabs API (PAID)
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Tuple
from dataclasses import dataclass, asdict
import hashlib
from datetime import datetime

logger = logging.getLogger('KreyolAI.VoiceCloning')


@dataclass
class VoiceProfile:
    """Voice characteristics profile"""
    voice_id: str
    name: str
    pitch_shift: float = 0.0  # -12 to +12 semitones
    speed_factor: float = 1.0  # 0.5 to 2.0
    volume_boost: float = 0.0  # -20 to +20 dB
    eq_profile: str = "neutral"  # neutral, warm, bright, bass_boost
    gender: str = "neutral"
    age_range: str = "adult"
    region: str = "Haiti"
    sample_audio_path: Optional[str] = None
    cloning_method: str = "basic"  # basic, medium, premium
    created_at: str = ""
    
    def to_dict(self) -> dict:
        return asdict(self)


class VoiceAnalyzer:
    """Analyze audio samples to extract voice characteristics"""
    
    def __init__(self):
        self.has_librosa = self._check_librosa()
        self.has_parselmouth = self._check_parselmouth()
    
    def _check_librosa(self) -> bool:
        try:
            import librosa
            return True
        except ImportError:
            logger.warning("librosa not available - limited voice analysis")
            return False
    
    def _check_parselmouth(self) -> bool:
        try:
            import parselmouth
            return True
        except ImportError:
            logger.warning("parselmouth not available - no pitch detection")
            return False
    
    def analyze(self, audio_path: Path) -> Dict:
        """
        Analyze audio file to extract voice characteristics
        
        Returns:
            Dictionary with voice features
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        features = {
            "pitch_shift": 0.0,
            "speed_factor": 1.0,
            "volume_boost": 0.0,
            "eq_profile": "neutral",
            "gender": "neutral"
        }
        
        if self.has_librosa:
            features.update(self._analyze_with_librosa(audio_path))
        
        if self.has_parselmouth:
            features.update(self._analyze_pitch(audio_path))
        
        return features
    
    def _analyze_with_librosa(self, audio_path: Path) -> Dict:
        """Analyze audio using librosa"""
        import librosa
        import numpy as np
        
        # Load audio
        y, sr = librosa.load(str(audio_path), sr=22050)
        
        # Extract features
        features = {}
        
        # Tempo (for speed factor)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        if tempo < 100:
            features["speed_factor"] = 0.9  # Slower voice
        elif tempo > 140:
            features["speed_factor"] = 1.1  # Faster voice
        else:
            features["speed_factor"] = 1.0
        
        # RMS energy (for volume)
        rms = librosa.feature.rms(y=y)[0]
        mean_rms = np.mean(rms)
        if mean_rms < 0.02:
            features["volume_boost"] = 3.0  # Quiet voice, boost
        elif mean_rms > 0.1:
            features["volume_boost"] = -3.0  # Loud voice, reduce
        
        # Spectral centroid (for EQ profile)
        centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        if centroid < 1500:
            features["eq_profile"] = "warm"  # More bass
        elif centroid > 3000:
            features["eq_profile"] = "bright"  # More treble
        else:
            features["eq_profile"] = "neutral"
        
        return features
    
    def _analyze_pitch(self, audio_path: Path) -> Dict:
        """Analyze pitch using parselmouth (Praat)"""
        import parselmouth
        import numpy as np
        
        sound = parselmouth.Sound(str(audio_path))
        pitch = sound.to_pitch()
        
        pitch_values = pitch.selected_array['frequency']
        pitch_values = pitch_values[pitch_values != 0]  # Remove unvoiced
        
        if len(pitch_values) == 0:
            return {"pitch_shift": 0.0, "gender": "neutral"}
        
        mean_pitch = np.mean(pitch_values)
        
        # Determine pitch shift and gender
        features = {}
        
        if mean_pitch < 165:  # Typical male range
            features["gender"] = "male"
            features["pitch_shift"] = -2.0  # Slightly lower
        elif mean_pitch > 255:  # Typical female range
            features["gender"] = "female"
            features["pitch_shift"] = 2.0  # Slightly higher
        else:
            features["gender"] = "neutral"
            features["pitch_shift"] = 0.0
        
        return features


class VoiceCloner:
    """
    Main voice cloning service
    Supports multiple cloning methods
    """
    
    def __init__(self, voices_dir: Path = None):
        self.voices_dir = voices_dir or Path("custom_voices")
        self.voices_dir.mkdir(exist_ok=True, parents=True)
        
        self.analyzer = VoiceAnalyzer()
        self.profiles_file = self.voices_dir / "voice_profiles.json"
        self.profiles = self._load_profiles()
    
    def _load_profiles(self) -> Dict:
        """Load voice profiles from JSON"""
        if self.profiles_file.exists():
            try:
                with open(self.profiles_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load profiles: {e}")
                return {}
        return {}
    
    def _save_profiles(self):
        """Save voice profiles to JSON"""
        try:
            with open(self.profiles_file, 'w', encoding='utf-8') as f:
                json.dump(self.profiles, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save profiles: {e}")
    
    def clone_voice_basic(
        self,
        audio_sample: Path,
        voice_name: str,
        **kwargs
    ) -> VoiceProfile:
        """
        BASIC voice cloning: Analyze audio and create voice profile
        
        This doesn't create a new voice model, but extracts characteristics
        that can be applied to any TTS engine (pitch, speed, EQ, etc.)
        """
        logger.info(f"Creating basic voice profile for: {voice_name}")
        
        # Analyze audio
        features = self.analyzer.analyze(audio_sample)
        
        # Generate voice ID
        voice_id = hashlib.md5(
            f"{voice_name}_{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]
        
        # Create profile
        profile = VoiceProfile(
            voice_id=voice_id,
            name=voice_name,
            pitch_shift=features.get("pitch_shift", 0.0),
            speed_factor=features.get("speed_factor", 1.0),
            volume_boost=features.get("volume_boost", 0.0),
            eq_profile=features.get("eq_profile", "neutral"),
            gender=features.get("gender", kwargs.get("gender", "neutral")),
            age_range=kwargs.get("age_range", "adult"),
            region=kwargs.get("region", "Haiti"),
            sample_audio_path=str(audio_sample),
            cloning_method="basic",
            created_at=datetime.now().isoformat()
        )
        
        # Save profile
        self.profiles[voice_id] = profile.to_dict()
        self._save_profiles()
        
        logger.info(f"✅ Voice profile created: {voice_id}")
        return profile
    
    def clone_voice_medium(
        self,
        audio_sample: Path,
        voice_name: str,
        **kwargs
    ) -> VoiceProfile:
        """
        MEDIUM voice cloning: Use RVC (Retrieval-based Voice Conversion)
        
        This is a placeholder for future RVC integration
        Requires significant compute resources
        """
        logger.warning("Medium (RVC) cloning not yet implemented")
        logger.info("Falling back to basic cloning")
        return self.clone_voice_basic(audio_sample, voice_name, **kwargs)
    
    def clone_voice_premium(
        self,
        audio_sample: Path,
        voice_name: str,
        **kwargs
    ) -> VoiceProfile:
        """
        PREMIUM voice cloning: Use ElevenLabs API
        
        Requires ELEVENLABS_API_KEY environment variable
        """
        api_key = os.getenv("ELEVENLABS_API_KEY")
        
        if not api_key:
            logger.warning("ELEVENLABS_API_KEY not set, falling back to basic")
            return self.clone_voice_basic(audio_sample, voice_name, **kwargs)
        
        try:
            import httpx
            
            logger.info(f"Creating premium voice with ElevenLabs: {voice_name}")
            
            # Upload audio to ElevenLabs
            with open(audio_sample, 'rb') as f:
                files = {'audio': f}
                data = {
                    'name': voice_name,
                    'description': kwargs.get('notes', 'Custom Haitian Creole voice')
                }
                
                response = httpx.post(
                    "https://api.elevenlabs.io/v1/voices/add",
                    headers={"xi-api-key": api_key},
                    files=files,
                    data=data,
                    timeout=60.0
                )
            
            if response.status_code == 200:
                result = response.json()
                elevenlabs_voice_id = result.get('voice_id')
                
                # Create profile
                voice_id = hashlib.md5(
                    f"{voice_name}_{datetime.now().isoformat()}".encode()
                ).hexdigest()[:12]
                
                profile = VoiceProfile(
                    voice_id=voice_id,
                    name=voice_name,
                    gender=kwargs.get("gender", "neutral"),
                    age_range=kwargs.get("age_range", "adult"),
                    region=kwargs.get("region", "Haiti"),
                    sample_audio_path=str(audio_sample),
                    cloning_method="premium",
                    created_at=datetime.now().isoformat()
                )
                
                # Store ElevenLabs voice ID in profile
                profile_dict = profile.to_dict()
                profile_dict['elevenlabs_voice_id'] = elevenlabs_voice_id
                
                self.profiles[voice_id] = profile_dict
                self._save_profiles()
                
                logger.info(f"✅ Premium voice created: {voice_id} (ElevenLabs: {elevenlabs_voice_id})")
                return profile
            else:
                logger.error(f"ElevenLabs API error: {response.status_code}")
                return self.clone_voice_basic(audio_sample, voice_name, **kwargs)
        
        except Exception as e:
            logger.error(f"Premium cloning failed: {e}")
            return self.clone_voice_basic(audio_sample, voice_name, **kwargs)
    
    def clone_voice(
        self,
        audio_sample: Path,
        voice_name: str,
        method: str = "basic",
        **kwargs
    ) -> VoiceProfile:
        """
        Clone voice using specified method
        
        Args:
            audio_sample: Path to audio file (MP3, WAV, etc.)
            voice_name: Name for the voice
            method: 'basic', 'medium', or 'premium'
            **kwargs: Additional parameters (gender, age_range, region, etc.)
        
        Returns:
            VoiceProfile object
        """
        if method == "basic":
            return self.clone_voice_basic(audio_sample, voice_name, **kwargs)
        elif method == "medium":
            return self.clone_voice_medium(audio_sample, voice_name, **kwargs)
        elif method == "premium":
            return self.clone_voice_premium(audio_sample, voice_name, **kwargs)
        else:
            raise ValueError(f"Unknown cloning method: {method}")
    
    def get_profile(self, voice_id: str) -> Optional[VoiceProfile]:
        """Get voice profile by ID"""
        profile_dict = self.profiles.get(voice_id)
        if profile_dict:
            return VoiceProfile(**profile_dict)
        return None
    
    def list_profiles(self) -> list:
        """List all voice profiles"""
        return [VoiceProfile(**p) for p in self.profiles.values()]
    
    def delete_profile(self, voice_id: str) -> bool:
        """Delete voice profile"""
        if voice_id in self.profiles:
            del self.profiles[voice_id]
            self._save_profiles()
            return True
        return False


# Integration with existing CustomVoiceManager
def upgrade_custom_voice_manager():
    """
    Upgrade existing CustomVoiceManager to use VoiceCloner
    This replaces the placeholder implementation
    """
    from custom_voice_manager import CustomVoiceManager
    
    # Monkey-patch the add_voice method
    original_add_voice = CustomVoiceManager.add_voice
    
    def new_add_voice(self, audio_file: Path, voice_name: str, **kwargs):
        """Enhanced add_voice with real cloning"""
        # Get cloning method from kwargs
        cloning_method = kwargs.pop('model', 'basic')  # 'standard' -> 'basic'
        if cloning_method == 'standard':
            cloning_method = 'basic'
        
        # Use VoiceCloner
        cloner = VoiceCloner(voices_dir=self.voices_dir)
        profile = cloner.clone_voice(
            audio_sample=audio_file,
            voice_name=voice_name,
            method=cloning_method,
            **kwargs
        )
        
        # Call original method to maintain compatibility
        voice_id = original_add_voice(self, audio_file, voice_name, **kwargs)
        
        # Update metadata with cloning info
        if voice_id in self.voices:
            self.voices[voice_id]['cloning_method'] = cloning_method
            self.voices[voice_id]['voice_profile'] = profile.to_dict()
            self._save_metadata()
        
        return voice_id
    
    CustomVoiceManager.add_voice = new_add_voice
    logger.info("✅ CustomVoiceManager upgraded with real voice cloning")


if __name__ == "__main__":
    # Test voice cloning
    print("🧪 Testing Voice Cloning System...")
    
    cloner = VoiceCloner()
    print(f"📊 Available profiles: {len(cloner.list_profiles())}")
    
    # Test with a sample audio file
    test_audio = Path("test_voice_sample.mp3")
    if test_audio.exists():
        print(f"🎤 Cloning voice from: {test_audio}")
        profile = cloner.clone_voice(
            audio_sample=test_audio,
            voice_name="Test Voice",
            method="basic",
            gender="neutral",
            region="Haiti"
        )
        print(f"✅ Voice cloned: {profile.voice_id}")
        print(f"📊 Profile: {profile}")
    else:
        print("⚠️  No test audio file found")

