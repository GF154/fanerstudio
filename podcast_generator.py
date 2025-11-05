#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎙️ Podcast Generator - Multi-Speaker Support
Jeneratè Podkas - Sipò Multi-Speaker
"""

import os
import tempfile
from typing import List, Dict, Optional
from datetime import datetime

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("⚠️ gTTS not available")

try:
    from pydub import AudioSegment
    from pydub.effects import normalize
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("⚠️ pydub not available")


class PodcastGenerator:
    """
    Advanced podcast generator with multi-speaker support
    """
    
    def __init__(self):
        if not GTTS_AVAILABLE:
            raise ImportError("gTTS required. Install: pip install gtts")
        if not PYDUB_AVAILABLE:
            raise ImportError("pydub required. Install: pip install pydub")
    
    def parse_script(self, script: str) -> List[Dict]:
        """
        Parse podcast script with speaker tags
        
        Format:
            [Speaker1]: Hello everyone!
            [Speaker2]: Welcome to our show!
        
        Returns:
            List of segments with speaker and text
        """
        segments = []
        lines = script.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for speaker tag
            if line.startswith('[') and ']:' in line:
                # Format: [Speaker]: Text
                speaker_end = line.find(']:')
                speaker = line[1:speaker_end].strip()
                text = line[speaker_end+2:].strip()
                
                segments.append({
                    'speaker': speaker,
                    'text': text
                })
            else:
                # No speaker tag, use default
                segments.append({
                    'speaker': 'Speaker1',
                    'text': line
                })
        
        return segments
    
    def generate_segment_audio(
        self,
        text: str,
        speaker: str,
        lang: str = "fr",
        output_file: Optional[str] = None
    ) -> str:
        """
        Generate audio for a single segment
        
        Args:
            text: Text to convert
            speaker: Speaker name (affects voice selection)
            lang: Language code
            output_file: Output file path (auto-generated if None)
            
        Returns:
            Path to generated audio file
        """
        if not output_file:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            output_file = temp_file.name
            temp_file.close()
        
        # Generate TTS
        # Note: gTTS doesn't have multiple voices, but we can use different languages
        # for variety, or adjust speed/pitch with pydub
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_file)
        
        return output_file
    
    def combine_segments(
        self,
        segment_files: List[str],
        pause_duration: int = 500
    ) -> AudioSegment:
        """
        Combine multiple audio segments with pauses
        
        Args:
            segment_files: List of audio file paths
            pause_duration: Pause between segments in milliseconds
            
        Returns:
            Combined AudioSegment
        """
        combined = AudioSegment.empty()
        pause = AudioSegment.silent(duration=pause_duration)
        
        for i, file_path in enumerate(segment_files):
            segment = AudioSegment.from_mp3(file_path)
            combined += segment
            
            # Add pause between segments (but not after last)
            if i < len(segment_files) - 1:
                combined += pause
        
        return combined
    
    def add_intro_outro(
        self,
        podcast: AudioSegment,
        intro_text: Optional[str] = None,
        outro_text: Optional[str] = None,
        lang: str = "fr"
    ) -> AudioSegment:
        """
        Add intro and outro to podcast
        
        Args:
            podcast: Main podcast audio
            intro_text: Intro text (optional)
            outro_text: Outro text (optional)
            lang: Language code
            
        Returns:
            Podcast with intro/outro
        """
        result = AudioSegment.empty()
        
        # Add intro
        if intro_text:
            intro_file = self.generate_segment_audio(intro_text, "Intro", lang)
            intro = AudioSegment.from_mp3(intro_file)
            result += intro + AudioSegment.silent(duration=1000)
            os.unlink(intro_file)
        
        # Add main podcast
        result += podcast
        
        # Add outro
        if outro_text:
            outro_file = self.generate_segment_audio(outro_text, "Outro", lang)
            outro = AudioSegment.from_mp3(outro_file)
            result += AudioSegment.silent(duration=1000) + outro
            os.unlink(outro_file)
        
        return result
    
    def add_background_music(
        self,
        podcast: AudioSegment,
        music_file: Optional[str] = None,
        music_volume: float = 0.3
    ) -> AudioSegment:
        """
        Add background music to podcast
        
        Args:
            podcast: Podcast audio
            music_file: Background music file path (optional)
            music_volume: Music volume (0.0 to 1.0)
            
        Returns:
            Podcast with background music
        """
        if not music_file or not os.path.exists(music_file):
            return podcast
        
        # Load music
        music = AudioSegment.from_file(music_file)
        
        # Adjust music volume
        music = music - (20 * (1 - music_volume))
        
        # Loop music if shorter than podcast
        if len(music) < len(podcast):
            loops_needed = (len(podcast) // len(music)) + 1
            music = music * loops_needed
        
        # Trim music to podcast length
        music = music[:len(podcast)]
        
        # Overlay music on podcast
        result = podcast.overlay(music)
        
        return result
    
    def generate_podcast(
        self,
        script: str,
        output_file: str,
        lang: str = "fr",
        intro_text: Optional[str] = None,
        outro_text: Optional[str] = None,
        music_file: Optional[str] = None,
        music_volume: float = 0.3,
        format: str = "mp3",
        progress_callback: Optional[callable] = None
    ) -> str:
        """
        Generate complete podcast from script
        
        Args:
            script: Podcast script with speaker tags
            output_file: Output file path
            lang: Language code
            intro_text: Intro text (optional)
            outro_text: Outro text (optional)
            music_file: Background music file (optional)
            music_volume: Music volume (0.0 to 1.0)
            format: Output format (mp3, wav, etc.)
            progress_callback: Progress callback function
            
        Returns:
            Path to generated podcast file
        """
        if progress_callback:
            progress_callback(10, "Ap analyze skrip la...")
        
        # Parse script into segments
        segments = self.parse_script(script)
        
        if not segments:
            raise ValueError("No segments found in script")
        
        if progress_callback:
            progress_callback(20, f"Ap jenere {len(segments)} segment yo...")
        
        # Generate audio for each segment
        segment_files = []
        for i, segment in enumerate(segments):
            if progress_callback:
                progress = 20 + (40 * (i + 1) / len(segments))
                progress_callback(int(progress), f"Ap jenere segment {i+1}/{len(segments)}...")
            
            audio_file = self.generate_segment_audio(
                text=segment['text'],
                speaker=segment['speaker'],
                lang=lang
            )
            segment_files.append(audio_file)
        
        if progress_callback:
            progress_callback(65, "Ap melanje segment yo...")
        
        # Combine segments
        podcast = self.combine_segments(segment_files)
        
        # Clean up segment files
        for file in segment_files:
            try:
                os.unlink(file)
            except:
                pass
        
        if progress_callback:
            progress_callback(75, "Ap ajoute intro/outro...")
        
        # Add intro/outro
        podcast = self.add_intro_outro(podcast, intro_text, outro_text, lang)
        
        if progress_callback:
            progress_callback(85, "Ap ajoute mizik background...")
        
        # Add background music
        if music_file:
            podcast = self.add_background_music(podcast, music_file, music_volume)
        
        if progress_callback:
            progress_callback(95, "Ap normalize ak eksporte...")
        
        # Normalize audio
        podcast = normalize(podcast)
        
        # Export
        podcast.export(output_file, format=format)
        
        if progress_callback:
            progress_callback(100, "Fini!")
        
        return output_file
    
    @staticmethod
    def get_audio_duration(file_path: str) -> float:
        """Get duration in seconds"""
        if not PYDUB_AVAILABLE:
            return 0.0
        try:
            audio = AudioSegment.from_file(file_path)
            return len(audio) / 1000.0
        except:
            return 0.0
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration as MM:SS"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"


# Quick test
if __name__ == "__main__":
    print("🎙️ Testing Podcast Generator...")
    
    # Test script
    test_script = """
[Host]: Bonjou tout moun! Byenveni nan emisyon nou an.
[Guest]: Mèsi anpil pou envitasyon an!
[Host]: Ki nouvel ou?
[Guest]: M byen wi, m kontan pou m la.
[Host]: Ann kòmanse!
"""
    
    try:
        generator = PodcastGenerator()
        
        # Parse script
        segments = generator.parse_script(test_script)
        print(f"✅ Found {len(segments)} segments")
        
        for i, seg in enumerate(segments, 1):
            print(f"  {i}. [{seg['speaker']}]: {seg['text'][:50]}...")
        
        print("\n✅ Podcast generator ready!")
        print("📝 Use generate_podcast() to create full podcasts")
        
    except Exception as e:
        print(f"❌ Error: {e}")

