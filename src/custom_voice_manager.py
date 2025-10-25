#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom Voice Manager - Add Natural Haitian Creole Voices
Gestionnaire de Voix Personnalisées - Ajouter des voix naturelles en créole
"""

import logging
import json
from pathlib import Path
from typing import Optional, Dict, List
import hashlib
from datetime import datetime

logger = logging.getLogger('KreyolAI.CustomVoice')


class CustomVoiceManager:
    """
    Manage custom voice recordings for natural Haitian Creole pronunciation
    Gérer les enregistrements vocaux personnalisés pour une prononciation naturelle
    """
    
    def __init__(self, voices_dir: Path = None):
        """
        Initialize custom voice manager
        
        Args:
            voices_dir: Directory to store custom voices
        """
        self.voices_dir = voices_dir or Path("custom_voices")
        self.voices_dir.mkdir(exist_ok=True, parents=True)
        
        self.metadata_file = self.voices_dir / "voices_metadata.json"
        self.voices = self._load_metadata()
        
        logger.info(f"Custom voice manager initialized: {len(self.voices)} voices loaded")
    
    def _load_metadata(self) -> Dict:
        """Load voice metadata from JSON file"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load metadata: {e}")
                return {}
        return {}
    
    def _save_metadata(self):
        """Save voice metadata to JSON file"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.voices, f, indent=2, ensure_ascii=False)
            logger.info("Voice metadata saved")
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")
    
    def add_voice(
        self,
        audio_file: Path,
        voice_name: str,
        speaker_name: str,
        text_content: str,
        language: str = "ht",
        gender: str = "unknown",
        age_range: str = "unknown",
        region: str = "Haiti",
        notes: str = ""
    ) -> str:
        """
        Add a new custom voice recording
        
        Args:
            audio_file: Path to the audio file (MP3, WAV, etc.)
            voice_name: Unique name for this voice
            speaker_name: Name of the speaker
            text_content: The text that was spoken in the recording
            language: Language code (default: 'ht' for Haitian Creole)
            gender: Speaker gender (male/female/other/unknown)
            age_range: Age range (child/young_adult/adult/senior/unknown)
            region: Region/accent (Haiti, Port-au-Prince, Cap-Haïtien, etc.)
            notes: Additional notes
        
        Returns:
            voice_id: Unique ID for the voice
        """
        # Generate unique voice ID
        voice_id = hashlib.md5(
            f"{voice_name}_{speaker_name}_{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]
        
        # Copy audio file to voices directory
        audio_extension = audio_file.suffix
        new_audio_path = self.voices_dir / f"{voice_id}{audio_extension}"
        
        try:
            import shutil
            shutil.copy2(audio_file, new_audio_path)
        except Exception as e:
            logger.error(f"Failed to copy audio file: {e}")
            raise RuntimeError(f"Could not add voice: {e}")
        
        # Create metadata
        self.voices[voice_id] = {
            "voice_id": voice_id,
            "voice_name": voice_name,
            "speaker_name": speaker_name,
            "text_content": text_content,
            "language": language,
            "gender": gender,
            "age_range": age_range,
            "region": region,
            "notes": notes,
            "audio_file": new_audio_path.name,
            "audio_format": audio_extension.lstrip('.'),
            "duration_seconds": self._get_audio_duration(new_audio_path),
            "file_size_mb": new_audio_path.stat().st_size / (1024 * 1024),
            "added_date": datetime.now().isoformat(),
            "times_used": 0,
            "rating": 0.0
        }
        
        self._save_metadata()
        
        logger.info(f"Voice added: {voice_name} (ID: {voice_id})")
        print(f"✅ Vwa ajoute / Voice added: {voice_name}")
        print(f"   ID: {voice_id}")
        
        return voice_id
    
    def _get_audio_duration(self, audio_path: Path) -> float:
        """Get audio duration in seconds"""
        try:
            # Try with pydub
            from pydub import AudioSegment
            audio = AudioSegment.from_file(str(audio_path))
            return len(audio) / 1000.0  # milliseconds to seconds
        except:
            try:
                # Try with mutagen
                from mutagen.mp3 import MP3
                audio = MP3(str(audio_path))
                return audio.info.length
            except:
                # Default if we can't determine
                return 0.0
    
    def get_voice(self, voice_id: str) -> Optional[Dict]:
        """Get voice metadata by ID"""
        return self.voices.get(voice_id)
    
    def get_voice_path(self, voice_id: str) -> Optional[Path]:
        """Get path to voice audio file"""
        voice = self.get_voice(voice_id)
        if voice:
            return self.voices_dir / voice['audio_file']
        return None
    
    def list_voices(
        self,
        language: Optional[str] = None,
        gender: Optional[str] = None,
        region: Optional[str] = None
    ) -> List[Dict]:
        """
        List available custom voices with optional filtering
        
        Args:
            language: Filter by language
            gender: Filter by gender
            region: Filter by region
        
        Returns:
            List of voice metadata dictionaries
        """
        voices = list(self.voices.values())
        
        if language:
            voices = [v for v in voices if v['language'] == language]
        if gender:
            voices = [v for v in voices if v['gender'] == gender]
        if region:
            voices = [v for v in voices if region.lower() in v['region'].lower()]
        
        # Sort by rating, then by times used
        voices.sort(key=lambda x: (x['rating'], x['times_used']), reverse=True)
        
        return voices
    
    def delete_voice(self, voice_id: str) -> bool:
        """Delete a custom voice"""
        voice = self.get_voice(voice_id)
        if not voice:
            logger.warning(f"Voice not found: {voice_id}")
            return False
        
        try:
            # Delete audio file
            audio_path = self.voices_dir / voice['audio_file']
            if audio_path.exists():
                audio_path.unlink()
            
            # Remove from metadata
            del self.voices[voice_id]
            self._save_metadata()
            
            logger.info(f"Voice deleted: {voice_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete voice: {e}")
            return False
    
    def update_voice_stats(self, voice_id: str, rating: Optional[float] = None):
        """Update voice usage statistics"""
        if voice_id in self.voices:
            self.voices[voice_id]['times_used'] += 1
            if rating is not None:
                # Update rolling average rating
                current_rating = self.voices[voice_id]['rating']
                times_used = self.voices[voice_id]['times_used']
                new_rating = ((current_rating * (times_used - 1)) + rating) / times_used
                self.voices[voice_id]['rating'] = round(new_rating, 2)
            
            self._save_metadata()
    
    def search_voices(self, query: str) -> List[Dict]:
        """
        Search voices by name, speaker, text content, or region
        
        Args:
            query: Search query
        
        Returns:
            List of matching voices
        """
        query_lower = query.lower()
        results = []
        
        for voice in self.voices.values():
            if (query_lower in voice['voice_name'].lower() or
                query_lower in voice['speaker_name'].lower() or
                query_lower in voice['text_content'].lower() or
                query_lower in voice['region'].lower() or
                query_lower in voice['notes'].lower()):
                results.append(voice)
        
        return results
    
    def get_best_voice_for_text(self, text: str, max_results: int = 5) -> List[Dict]:
        """
        Find the best matching voice for a given text
        Uses simple keyword matching
        
        Args:
            text: The text to be spoken
            max_results: Maximum number of results to return
        
        Returns:
            List of best matching voices
        """
        # Get all Haitian Creole voices
        voices = self.list_voices(language='ht')
        
        if not voices:
            return []
        
        # Simple scoring based on text similarity
        text_lower = text.lower()
        scored_voices = []
        
        for voice in voices:
            score = 0
            
            # Check if voice text contains similar words
            voice_words = set(voice['text_content'].lower().split())
            text_words = set(text_lower.split())
            common_words = voice_words & text_words
            
            score += len(common_words) * 10
            
            # Boost score for highly rated voices
            score += voice['rating'] * 5
            
            # Boost score for frequently used voices
            score += min(voice['times_used'] / 10, 5)
            
            scored_voices.append((score, voice))
        
        # Sort by score and return top results
        scored_voices.sort(key=lambda x: x[0], reverse=True)
        return [v for _, v in scored_voices[:max_results]]
    
    def export_voice_catalog(self, output_file: Path):
        """Export voice catalog to a readable format"""
        catalog = {
            "total_voices": len(self.voices),
            "voices": list(self.voices.values()),
            "export_date": datetime.now().isoformat()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Voice catalog exported to {output_file}")
    
    def get_statistics(self) -> Dict:
        """Get statistics about custom voices"""
        if not self.voices:
            return {
                "total_voices": 0,
                "total_duration_minutes": 0,
                "total_size_mb": 0,
                "languages": {},
                "genders": {},
                "regions": {}
            }
        
        voices_list = list(self.voices.values())
        
        return {
            "total_voices": len(voices_list),
            "total_duration_minutes": sum(v['duration_seconds'] for v in voices_list) / 60,
            "total_size_mb": sum(v['file_size_mb'] for v in voices_list),
            "average_duration_seconds": sum(v['duration_seconds'] for v in voices_list) / len(voices_list),
            "average_rating": sum(v['rating'] for v in voices_list) / len(voices_list),
            "most_used": max(voices_list, key=lambda x: x['times_used'])['voice_name'],
            "highest_rated": max(voices_list, key=lambda x: x['rating'])['voice_name'],
            "languages": self._count_by_field(voices_list, 'language'),
            "genders": self._count_by_field(voices_list, 'gender'),
            "regions": self._count_by_field(voices_list, 'region')
        }
    
    def _count_by_field(self, voices: List[Dict], field: str) -> Dict:
        """Count voices by a specific field"""
        counts = {}
        for voice in voices:
            value = voice.get(field, 'unknown')
            counts[value] = counts.get(value, 0) + 1
        return counts


def create_voice_manager(voices_dir: Path = None) -> CustomVoiceManager:
    """Factory function to create voice manager"""
    return CustomVoiceManager(voices_dir)

