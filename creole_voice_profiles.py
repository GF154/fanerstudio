#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇭🇹 Creole-Specific Voice Profiles
Pwofil vwa espesyal pou Kreyòl Ayisyen

Optimized voice settings for natural Haitian Creole pronunciation
"""

from dataclasses import dataclass
from typing import Dict, List
from enum import Enum


class CreoleRegion(str, Enum):
    """Haitian regions with distinct accents"""
    PORT_AU_PRINCE = "port-au-prince"
    CAP_HAITIEN = "cap-haitien"
    LES_CAYES = "les-cayes"
    GONAIVES = "gonaives"
    JACMEL = "jacmel"
    JEREMIE = "jeremie"
    SAINT_MARC = "saint-marc"
    STANDARD = "standard"  # Neutral/standard Creole


class CreoleSpeakerType(str, Enum):
    """Common Creole speaker types"""
    STORYTELLER = "storyteller"  # Raconteur
    NEWS_ANCHOR = "news-anchor"  # Journalist
    TEACHER = "teacher"  # Professor
    CASUAL = "casual"  # Everyday conversation
    FORMAL = "formal"  # Official/formal speech
    ELDERLY = "elderly"  # Older generation
    YOUTH = "youth"  # Younger generation


@dataclass
class CreoleVoiceProfile:
    """
    Voice profile optimized for Haitian Creole
    Pwofil vwa optimize pou Kreyòl Ayisyen
    """
    name: str
    region: CreoleRegion
    speaker_type: CreoleSpeakerType
    gender: str  # male, female, neutral
    
    # Voice characteristics
    pitch_shift: float = 0.0  # -12 to +12 semitones
    speed_factor: float = 1.0  # 0.5 to 2.0
    volume_boost: float = 0.0  # -20 to +20 dB
    
    # Creole-specific settings
    nasalization_strength: float = 1.0  # 0.0 to 2.0
    rhythm_emphasis: float = 1.0  # 0.5 to 1.5
    consonant_clarity: float = 1.0  # 0.5 to 1.5
    
    # TTS engine preferences
    preferred_tts: str = "gtts-fr"  # gtts-fr, edge-fr-ca, coqui
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "region": self.region.value,
            "speaker_type": self.speaker_type.value,
            "gender": self.gender,
            "pitch_shift": self.pitch_shift,
            "speed_factor": self.speed_factor,
            "volume_boost": self.volume_boost,
            "nasalization_strength": self.nasalization_strength,
            "rhythm_emphasis": self.rhythm_emphasis,
            "consonant_clarity": self.consonant_clarity,
            "preferred_tts": self.preferred_tts
        }


class CreoleVoiceLibrary:
    """
    Library of pre-configured Creole voice profiles
    Bibliyotèk pwofil vwa Kreyòl ki deja konfigure
    """
    
    def __init__(self):
        self.profiles = self._load_default_profiles()
    
    def _load_default_profiles(self) -> Dict[str, CreoleVoiceProfile]:
        """Load default Creole voice profiles"""
        return {
            # ============================================================
            # STANDARD VOICES / VWA ESTANDA
            # ============================================================
            "creole_female_standard": CreoleVoiceProfile(
                name="Kreyòl Fanm Estanda",
                region=CreoleRegion.STANDARD,
                speaker_type=CreoleSpeakerType.CASUAL,
                gender="female",
                pitch_shift=2.0,
                speed_factor=0.95,
                nasalization_strength=1.2,
                rhythm_emphasis=1.0,
                preferred_tts="edge-fr-ca"
            ),
            
            "creole_male_standard": CreoleVoiceProfile(
                name="Kreyòl Gason Estanda",
                region=CreoleRegion.STANDARD,
                speaker_type=CreoleSpeakerType.CASUAL,
                gender="male",
                pitch_shift=-2.0,
                speed_factor=0.95,
                nasalization_strength=1.1,
                rhythm_emphasis=1.0,
                preferred_tts="edge-fr-ca"
            ),
            
            # ============================================================
            # NEWS ANCHOR / JOURNALIST
            # ============================================================
            "creole_news_anchor": CreoleVoiceProfile(
                name="Journalist Kreyòl",
                region=CreoleRegion.PORT_AU_PRINCE,
                speaker_type=CreoleSpeakerType.NEWS_ANCHOR,
                gender="neutral",
                pitch_shift=0.0,
                speed_factor=1.0,
                volume_boost=2.0,
                nasalization_strength=0.9,
                rhythm_emphasis=1.1,
                consonant_clarity=1.3,
                preferred_tts="edge-fr-ca"
            ),
            
            # ============================================================
            # STORYTELLER / RACONTEUR
            # ============================================================
            "creole_storyteller": CreoleVoiceProfile(
                name="Rakontè Kreyòl",
                region=CreoleRegion.STANDARD,
                speaker_type=CreoleSpeakerType.STORYTELLER,
                gender="neutral",
                pitch_shift=1.0,
                speed_factor=0.90,
                nasalization_strength=1.3,
                rhythm_emphasis=1.2,
                consonant_clarity=1.1,
                preferred_tts="gtts-fr"
            ),
            
            # ============================================================
            # TEACHER / EDUCATOR
            # ============================================================
            "creole_teacher": CreoleVoiceProfile(
                name="Pwofesè Kreyòl",
                region=CreoleRegion.STANDARD,
                speaker_type=CreoleSpeakerType.TEACHER,
                gender="neutral",
                pitch_shift=0.5,
                speed_factor=0.85,
                volume_boost=1.0,
                nasalization_strength=1.0,
                rhythm_emphasis=1.0,
                consonant_clarity=1.4,
                preferred_tts="edge-fr-ca"
            ),
            
            # ============================================================
            # REGIONAL ACCENTS
            # ============================================================
            "creole_cap_haitien": CreoleVoiceProfile(
                name="Kreyòl Okap",
                region=CreoleRegion.CAP_HAITIEN,
                speaker_type=CreoleSpeakerType.CASUAL,
                gender="neutral",
                pitch_shift=0.0,
                speed_factor=1.05,  # Slightly faster
                nasalization_strength=1.1,
                rhythm_emphasis=0.95,
                preferred_tts="gtts-fr"
            ),
            
            "creole_les_cayes": CreoleVoiceProfile(
                name="Kreyòl Okay",
                region=CreoleRegion.LES_CAYES,
                speaker_type=CreoleSpeakerType.CASUAL,
                gender="neutral",
                pitch_shift=0.5,
                speed_factor=0.95,  # Slightly slower
                nasalization_strength=1.3,
                rhythm_emphasis=1.05,
                preferred_tts="gtts-fr"
            ),
            
            # ============================================================
            # AGE GROUPS
            # ============================================================
            "creole_elderly": CreoleVoiceProfile(
                name="Kreyòl Granmoun",
                region=CreoleRegion.STANDARD,
                speaker_type=CreoleSpeakerType.ELDERLY,
                gender="neutral",
                pitch_shift=-1.0,
                speed_factor=0.80,  # Slower
                volume_boost=-1.0,
                nasalization_strength=1.4,
                rhythm_emphasis=0.9,
                consonant_clarity=0.9,
                preferred_tts="gtts-fr"
            ),
            
            "creole_youth": CreoleVoiceProfile(
                name="Kreyòl Jèn",
                region=CreoleRegion.PORT_AU_PRINCE,
                speaker_type=CreoleSpeakerType.YOUTH,
                gender="neutral",
                pitch_shift=2.0,
                speed_factor=1.10,  # Faster
                nasalization_strength=1.0,
                rhythm_emphasis=1.1,
                consonant_clarity=1.2,
                preferred_tts="edge-fr-ca"
            ),
        }
    
    def get_profile(self, name: str) -> CreoleVoiceProfile:
        """Get voice profile by name"""
        return self.profiles.get(name)
    
    def list_profiles(self) -> List[Dict]:
        """List all available profiles"""
        return [
            {
                "id": key,
                "name": profile.name,
                "region": profile.region.value,
                "type": profile.speaker_type.value,
                "gender": profile.gender
            }
            for key, profile in self.profiles.items()
        ]
    
    def get_by_region(self, region: CreoleRegion) -> List[CreoleVoiceProfile]:
        """Get all profiles for a specific region"""
        return [
            profile for profile in self.profiles.values()
            if profile.region == region
        ]
    
    def get_by_type(self, speaker_type: CreoleSpeakerType) -> List[CreoleVoiceProfile]:
        """Get all profiles for a specific speaker type"""
        return [
            profile for profile in self.profiles.values()
            if profile.speaker_type == speaker_type
        ]
    
    def recommend_profile(
        self,
        use_case: str,
        gender_preference: str = "neutral"
    ) -> CreoleVoiceProfile:
        """
        Recommend best voice profile for use case
        
        Args:
            use_case: "audiobook", "podcast", "education", "news", "casual"
            gender_preference: "male", "female", "neutral"
        
        Returns:
            Recommended voice profile
        """
        recommendations = {
            "audiobook": "creole_storyteller",
            "podcast": "creole_female_standard",
            "education": "creole_teacher",
            "news": "creole_news_anchor",
            "casual": "creole_male_standard"
        }
        
        profile_key = recommendations.get(use_case, "creole_female_standard")
        return self.profiles[profile_key]


# ============================================================
# USAGE EXAMPLES
# ============================================================

def demo_creole_voices():
    """Demonstrate Creole voice profiles"""
    print("🇭🇹 Creole Voice Profiles Library\n")
    
    library = CreoleVoiceLibrary()
    
    print("Available Profiles:")
    for profile in library.list_profiles():
        print(f"  • {profile['name']} ({profile['id']})")
        print(f"    Region: {profile['region']}, Type: {profile['type']}")
    
    print("\nRecommendations:")
    use_cases = ["audiobook", "podcast", "education", "news"]
    for use_case in use_cases:
        profile = library.recommend_profile(use_case)
        print(f"  {use_case}: {profile.name}")


if __name__ == "__main__":
    demo_creole_voices()

