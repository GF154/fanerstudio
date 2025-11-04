#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎵 Music and Sound Effects Library for Podcast Production
Biblyotèk Mizik ak Efè Son pou Pwodiksyon Podcast
"""

from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger('KreyolAI.MusicLibrary')


class MusicLibrary:
    """
    Manage royalty-free music and sound effects
    Jere mizik san dwa otè ak efè son
    """
    
    def __init__(self, library_dir: Path = None):
        self.library_dir = library_dir or Path("audio_library")
        self.library_dir.mkdir(exist_ok=True, parents=True)
        
        # Create subdirectories
        (self.library_dir / "music").mkdir(exist_ok=True)
        (self.library_dir / "sfx").mkdir(exist_ok=True)
        (self.library_dir / "jingles").mkdir(exist_ok=True)
        
        self._create_default_library()
    
    def _create_default_library(self):
        """Create default audio library with simple tones"""
        try:
            from pydub.generators import Sine, Square, Sawtooth
            from pydub import AudioSegment
            import numpy as np
        except ImportError:
            logger.warning("pydub not available, skipping default library creation")
            return
        
        # Only create if library is empty
        if list((self.library_dir / "music").glob("*.mp3")):
            logger.info("Music library already populated")
            return
        
        logger.info("Creating default audio library...")
        
        try:
            # Create simple background music tracks
            self._generate_corporate_music()
            self._generate_upbeat_music()
            self._generate_calm_music()
            
            # Create sound effects
            self._generate_sfx()
            
            # Create jingles
            self._generate_jingles()
            
            logger.info("✅ Default audio library created")
        except Exception as e:
            logger.error(f"Failed to create default library: {e}")
    
    def _generate_corporate_music(self):
        """Generate simple corporate background music"""
        from pydub.generators import Sine
        from pydub import AudioSegment
        
        # Create a simple chord progression (C major)
        duration = 30000  # 30 seconds
        fade_duration = 2000
        
        c = Sine(261.63).to_audio_segment(duration=duration)  # C
        e = Sine(329.63).to_audio_segment(duration=duration)  # E
        g = Sine(392.00).to_audio_segment(duration=duration)  # G
        
        # Mix the notes at low volumes
        corporate = c.apply_gain(-20) + e.apply_gain(-23) + g.apply_gain(-21)
        
        # Add fade in/out
        corporate = corporate.fade_in(fade_duration).fade_out(fade_duration)
        
        # Export
        output_path = self.library_dir / "music" / "corporate.mp3"
        corporate.export(str(output_path), format="mp3")
        logger.info(f"Created: {output_path}")
    
    def _generate_upbeat_music(self):
        """Generate upbeat background music"""
        from pydub.generators import Sine
        from pydub import AudioSegment
        
        duration = 30000
        fade_duration = 2000
        
        # Higher frequencies for upbeat feel
        notes = [
            Sine(523.25).to_audio_segment(duration=duration),  # C5
            Sine(659.25).to_audio_segment(duration=duration),  # E5
            Sine(783.99).to_audio_segment(duration=duration),  # G5
        ]
        
        upbeat = sum(n.apply_gain(-21) for n in notes)
        upbeat = upbeat.fade_in(fade_duration).fade_out(fade_duration)
        
        output_path = self.library_dir / "music" / "upbeat.mp3"
        upbeat.export(str(output_path), format="mp3")
        logger.info(f"Created: {output_path}")
    
    def _generate_calm_music(self):
        """Generate calm background music"""
        from pydub.generators import Sine
        from pydub import AudioSegment
        
        duration = 30000
        fade_duration = 3000
        
        # Lower, smoother frequencies
        a = Sine(220.00).to_audio_segment(duration=duration)  # A3
        c = Sine(261.63).to_audio_segment(duration=duration)  # C4
        e = Sine(329.63).to_audio_segment(duration=duration)  # E4
        
        calm = a.apply_gain(-22) + c.apply_gain(-24) + e.apply_gain(-23)
        calm = calm.fade_in(fade_duration).fade_out(fade_duration)
        
        output_path = self.library_dir / "music" / "calm.mp3"
        calm.export(str(output_path), format="mp3")
        logger.info(f"Created: {output_path}")
    
    def _generate_sfx(self):
        """Generate sound effects"""
        from pydub.generators import Sine, WhiteNoise
        from pydub import AudioSegment
        
        # Transition swoosh
        swoosh = WhiteNoise().to_audio_segment(duration=500)
        swoosh = swoosh.fade_in(50).fade_out(200).apply_gain(-10)
        swoosh.export(str(self.library_dir / "sfx" / "transition.mp3"), format="mp3")
        
        # Ding notification
        ding = Sine(800).to_audio_segment(duration=200)
        ding = ding.fade_out(150).apply_gain(-15)
        ding.export(str(self.library_dir / "sfx" / "ding.mp3"), format="mp3")
        
        # Intro swoosh
        intro = WhiteNoise().to_audio_segment(duration=800)
        intro = intro.fade_in(100).fade_out(300).apply_gain(-12)
        intro.export(str(self.library_dir / "sfx" / "intro_swoosh.mp3"), format="mp3")
        
        # Outro fade
        outro = Sine(400).to_audio_segment(duration=1500)
        outro = outro.fade_in(200).fade_out(1000).apply_gain(-18)
        outro.export(str(self.library_dir / "sfx" / "outro_fade.mp3"), format="mp3")
        
        logger.info("Created sound effects")
    
    def _generate_jingles(self):
        """Generate podcast jingles"""
        from pydub.generators import Sine
        from pydub import AudioSegment
        
        # Simple intro jingle (3 notes ascending)
        c = Sine(523.25).to_audio_segment(duration=300)  # C5
        e = Sine(659.25).to_audio_segment(duration=300)  # E5
        g = Sine(783.99).to_audio_segment(duration=300)  # G5
        
        intro_jingle = c.apply_gain(-10) + e.apply_gain(-10) + g.apply_gain(-8)
        intro_jingle = intro_jingle.fade_in(50).fade_out(200)
        intro_jingle.export(str(self.library_dir / "jingles" / "intro.mp3"), format="mp3")
        
        # Simple outro jingle (3 notes descending)
        outro_jingle = g.apply_gain(-8) + e.apply_gain(-10) + c.apply_gain(-10)
        outro_jingle = outro_jingle.fade_in(50).fade_out(300)
        outro_jingle.export(str(self.library_dir / "jingles" / "outro.mp3"), format="mp3")
        
        logger.info("Created jingles")
    
    def get_music(self, genre: str) -> Optional[Path]:
        """
        Get background music file by genre
        
        Args:
            genre: Music genre (corporate, upbeat, calm, etc.)
        
        Returns:
            Path to music file or None
        """
        music_file = self.library_dir / "music" / f"{genre.lower()}.mp3"
        
        if music_file.exists():
            return music_file
        
        logger.warning(f"Music not found: {genre}")
        return None
    
    def get_sfx(self, effect: str) -> Optional[Path]:
        """
        Get sound effect file
        
        Args:
            effect: Sound effect name (transition, ding, intro_swoosh, etc.)
        
        Returns:
            Path to SFX file or None
        """
        sfx_file = self.library_dir / "sfx" / f"{effect.lower()}.mp3"
        
        if sfx_file.exists():
            return sfx_file
        
        logger.warning(f"SFX not found: {effect}")
        return None
    
    def get_jingle(self, type: str) -> Optional[Path]:
        """
        Get jingle file
        
        Args:
            type: Jingle type (intro, outro)
        
        Returns:
            Path to jingle file or None
        """
        jingle_file = self.library_dir / "jingles" / f"{type.lower()}.mp3"
        
        if jingle_file.exists():
            return jingle_file
        
        logger.warning(f"Jingle not found: {type}")
        return None
    
    def list_available(self) -> Dict:
        """List all available audio assets"""
        return {
            "music": [f.stem for f in (self.library_dir / "music").glob("*.mp3")],
            "sfx": [f.stem for f in (self.library_dir / "sfx").glob("*.mp3")],
            "jingles": [f.stem for f in (self.library_dir / "jingles").glob("*.mp3")]
        }


class AudioMixer:
    """
    Mix audio tracks with proper levels and effects
    Melanje pis odyo ak nivo ak efè pwòp
    """
    
    def __init__(self):
        try:
            from pydub import AudioSegment
            self.AudioSegment = AudioSegment
            self.available = True
        except ImportError:
            logger.error("pydub not available - audio mixing disabled")
            self.available = False
    
    def mix_with_background(
        self,
        voice_track: Path,
        background_music: Path,
        music_volume: float = 0.3,
        fade_in: float = 2.0,
        fade_out: float = 3.0
    ) -> Path:
        """
        Mix voice track with background music
        
        Args:
            voice_track: Path to voice audio
            background_music: Path to background music
            music_volume: Background music volume (0.0-1.0)
            fade_in: Fade in duration (seconds)
            fade_out: Fade out duration (seconds)
        
        Returns:
            Path to mixed audio file
        """
        if not self.available:
            logger.warning("Audio mixing not available, returning original voice track")
            return voice_track
        
        try:
            # Load tracks
            voice = self.AudioSegment.from_file(str(voice_track))
            music = self.AudioSegment.from_file(str(background_music))
            
            # Calculate volume reduction for background music
            db_reduction = -20 * (1 - music_volume)  # Convert 0-1 to dB
            
            # Adjust music to voice length and reduce volume
            if len(music) < len(voice):
                # Loop music if too short
                music = music * (len(voice) // len(music) + 1)
            
            music = music[:len(voice)].apply_gain(db_reduction)
            
            # Add fades to music
            fade_in_ms = int(fade_in * 1000)
            fade_out_ms = int(fade_out * 1000)
            music = music.fade_in(fade_in_ms).fade_out(fade_out_ms)
            
            # Mix
            mixed = voice.overlay(music)
            
            # Export
            output_path = voice_track.parent / f"{voice_track.stem}_mixed.mp3"
            mixed.export(str(output_path), format="mp3")
            
            logger.info(f"✅ Mixed audio saved: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Audio mixing failed: {e}")
            return voice_track
    
    def combine_segments(
        self,
        segments: list,
        crossfade: float = 0.5,
        normalize: bool = True
    ) -> Path:
        """
        Combine multiple audio segments into one file
        
        Args:
            segments: List of audio file paths
            crossfade: Crossfade duration between segments (seconds)
            normalize: Normalize audio levels
        
        Returns:
            Path to combined audio file
        """
        if not self.available or not segments:
            return None
        
        try:
            crossfade_ms = int(crossfade * 1000)
            
            # Load first segment
            combined = self.AudioSegment.from_file(str(segments[0]))
            
            # Add remaining segments with crossfade
            for segment_path in segments[1:]:
                segment = self.AudioSegment.from_file(str(segment_path))
                
                if crossfade_ms > 0:
                    combined = combined.append(segment, crossfade=crossfade_ms)
                else:
                    combined = combined + segment
            
            # Normalize if requested
            if normalize:
                combined = combined.normalize()
            
            # Export
            output_path = segments[0].parent / "combined_podcast.mp3"
            combined.export(str(output_path), format="mp3", bitrate="192k")
            
            logger.info(f"✅ Combined audio saved: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"Audio combination failed: {e}")
            return None


# Test function
def test_audio_library():
    """Test audio library creation"""
    print("🧪 Testing Audio Library...")
    
    library = MusicLibrary()
    available = library.list_available()
    
    print("📊 Available Audio Assets:")
    print(f"  Music: {available['music']}")
    print(f"  SFX: {available['sfx']}")
    print(f"  Jingles: {available['jingles']}")
    
    # Test mixer
    mixer = AudioMixer()
    if mixer.available:
        print("✅ Audio mixer available")
    else:
        print("⚠️  Audio mixer not available (install pydub)")


if __name__ == "__main__":
    test_audio_library()

