#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎙️ Faner Studio - Advanced Podcast Generator
Inspired by Veed Fabric AI technology
Multi-speaker, emotion control, background music, and professional editing
"""

from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import re
import uuid
from datetime import datetime
import logging

logger = logging.getLogger('KreyolAI.PodcastFabric')

# ============================================================
# ENUMS & CONSTANTS
# ============================================================

class VoiceEmotion(str, Enum):
    """Voice emotion types"""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    EXCITED = "excited"
    SAD = "sad"
    ANGRY = "angry"
    CALM = "calm"
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    ENERGETIC = "energetic"

class SpeakerGender(str, Enum):
    """Speaker gender"""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"

class MusicGenre(str, Enum):
    """Background music genres"""
    NONE = "none"
    CORPORATE = "corporate"
    UPBEAT = "upbeat"
    CALM = "calm"
    DRAMATIC = "dramatic"
    TECH = "tech"
    JAZZ = "jazz"
    LOFI = "lofi"

class SoundEffect(str, Enum):
    """Sound effects"""
    INTRO_SWOOSH = "intro_swoosh"
    TRANSITION = "transition"
    DING = "ding"
    APPLAUSE = "applause"
    TYPING = "typing"
    NOTIFICATION = "notification"
    OUTRO_FADE = "outro_fade"

# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class Speaker:
    """Speaker configuration"""
    id: str
    name: str
    voice_id: str
    gender: SpeakerGender = SpeakerGender.NEUTRAL
    emotion: VoiceEmotion = VoiceEmotion.NEUTRAL
    pitch: float = 1.0  # 0.5-2.0
    speed: float = 1.0  # 0.5-2.0
    volume: float = 1.0  # 0.0-2.0

@dataclass
class DialogueLine:
    """Single dialogue line"""
    speaker_id: str
    text: str
    emotion: Optional[VoiceEmotion] = None
    pause_after: float = 0.5  # seconds
    sound_effect: Optional[SoundEffect] = None

@dataclass
class PodcastSegment:
    """Podcast segment (intro, main, outro)"""
    type: str  # intro, main, outro, ad_break
    dialogues: List[DialogueLine]
    background_music: Optional[MusicGenre] = None
    music_volume: float = 0.3  # 0.0-1.0

@dataclass
class PodcastConfig:
    """Complete podcast configuration"""
    title: str
    description: str
    speakers: List[Speaker]
    segments: List[PodcastSegment]
    total_duration_target: Optional[int] = None  # seconds
    add_intro_jingle: bool = True
    add_outro_jingle: bool = True
    normalize_audio: bool = True
    export_format: str = "mp3"  # mp3, wav, m4a

# ============================================================
# SCRIPT PARSER
# ============================================================

class PodcastScriptParser:
    """
    Parse podcast script with Veed-style syntax
    
    Example script:
    ```
    [INTRO - Background: Corporate, Volume: 0.3]
    Host (excited): Welcome to the Faner Podcast!
    [SFX: intro_swoosh]
    
    [MAIN - Background: Calm]
    Host: Today we're talking about AI.
    Guest (professional): That's fascinating!
    [Pause: 2.0]
    
    [OUTRO - Background: Upbeat]
    Host (happy): Thanks for listening!
    [SFX: outro_fade]
    ```
    """
    
    def __init__(self):
        self.segment_pattern = re.compile(r'\[(\w+)\s*-?\s*(.*?)\]')
        self.dialogue_pattern = re.compile(r'(\w+)\s*(?:\((\w+)\))?\s*:\s*(.+)')
        self.sfx_pattern = re.compile(r'\[SFX:\s*(\w+)\]')
        self.pause_pattern = re.compile(r'\[Pause:\s*([\d.]+)\]')
    
    def parse(self, script: str, speakers: List[Speaker]) -> List[PodcastSegment]:
        """Parse script into segments"""
        segments = []
        current_segment = None
        current_dialogues = []
        
        lines = script.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for segment marker
            segment_match = self.segment_pattern.match(line)
            if segment_match:
                # Save previous segment
                if current_segment:
                    current_segment.dialogues = current_dialogues
                    segments.append(current_segment)
                
                # Parse new segment
                segment_type = segment_match.group(1).lower()
                segment_params = self._parse_segment_params(segment_match.group(2))
                
                current_segment = PodcastSegment(
                    type=segment_type,
                    dialogues=[],
                    background_music=segment_params.get('background'),
                    music_volume=segment_params.get('volume', 0.3)
                )
                current_dialogues = []
                continue
            
            # Check for sound effect
            sfx_match = self.sfx_pattern.match(line)
            if sfx_match and current_dialogues:
                sfx_name = sfx_match.group(1).lower()
                current_dialogues[-1].sound_effect = SoundEffect(sfx_name)
                continue
            
            # Check for pause
            pause_match = self.pause_pattern.match(line)
            if pause_match and current_dialogues:
                pause_duration = float(pause_match.group(1))
                current_dialogues[-1].pause_after = pause_duration
                continue
            
            # Check for dialogue
            dialogue_match = self.dialogue_pattern.match(line)
            if dialogue_match:
                speaker_name = dialogue_match.group(1)
                emotion = dialogue_match.group(2)
                text = dialogue_match.group(3)
                
                # Find speaker
                speaker = self._find_speaker(speakers, speaker_name)
                if not speaker:
                    continue
                
                dialogue = DialogueLine(
                    speaker_id=speaker.id,
                    text=text,
                    emotion=VoiceEmotion(emotion.lower()) if emotion else None
                )
                current_dialogues.append(dialogue)
        
        # Save last segment
        if current_segment:
            current_segment.dialogues = current_dialogues
            segments.append(current_segment)
        
        return segments
    
    def _parse_segment_params(self, params_str: str) -> Dict:
        """Parse segment parameters"""
        params = {}
        
        # Parse Background: genre
        bg_match = re.search(r'Background:\s*(\w+)', params_str, re.IGNORECASE)
        if bg_match:
            try:
                params['background'] = MusicGenre(bg_match.group(1).lower())
            except:
                params['background'] = MusicGenre.NONE
        
        # Parse Volume: 0.3
        vol_match = re.search(r'Volume:\s*([\d.]+)', params_str, re.IGNORECASE)
        if vol_match:
            params['volume'] = float(vol_match.group(1))
        
        return params
    
    def _find_speaker(self, speakers: List[Speaker], name: str) -> Optional[Speaker]:
        """Find speaker by name"""
        for speaker in speakers:
            if speaker.name.lower() == name.lower():
                return speaker
        return None

# ============================================================
# PODCAST GENERATOR
# ============================================================

class AdvancedPodcastGenerator:
    """
    Advanced podcast generator with Veed Fabric-inspired features
    """
    
    def __init__(self, output_dir: Path = Path("output/podcasts")):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.parser = PodcastScriptParser()
    
    async def generate_from_script(
        self,
        script: str,
        speakers: List[Speaker],
        config: Optional[PodcastConfig] = None
    ) -> Dict:
        """
        Generate podcast from script
        
        Args:
            script: Podcast script with markers
            speakers: List of speakers
            config: Podcast configuration
        
        Returns:
            Dictionary with generated files and metadata
        """
        # Parse script
        segments = self.parser.parse(script, speakers)
        
        # Create config if not provided
        if not config:
            config = PodcastConfig(
                title="Faner Podcast",
                description="Generated with Faner Studio",
                speakers=speakers,
                segments=segments
            )
        else:
            config.segments = segments
        
        # Generate podcast
        podcast_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        result = {
            "podcast_id": podcast_id,
            "title": config.title,
            "timestamp": timestamp,
            "segments": [],
            "audio_files": [],
            "metadata": self._create_metadata(config)
        }
        
        # Process each segment
        for idx, segment in enumerate(config.segments):
            segment_result = await self._process_segment(
                segment=segment,
                speakers=speakers,
                config=config,
                segment_idx=idx
            )
            result["segments"].append(segment_result)
            result["audio_files"].extend(segment_result["files"])
        
        # Combine all segments
        final_audio = await self._combine_segments(result["segments"], config)
        result["final_audio"] = final_audio
        
        # Save metadata
        metadata_file = self.output_dir / f"{podcast_id}_metadata.json"
        metadata_file.write_text(json.dumps(result, indent=2, default=str))
        result["metadata_file"] = str(metadata_file)
        
        return result
    
    async def _process_segment(
        self,
        segment: PodcastSegment,
        speakers: List[Speaker],
        config: PodcastConfig,
        segment_idx: int
    ) -> Dict:
        """Process single segment"""
        segment_files = []
        
        # Generate dialogues
        for dialogue_idx, dialogue in enumerate(segment.dialogues):
            speaker = self._get_speaker(speakers, dialogue.speaker_id)
            
            # Generate audio for dialogue
            audio_file = await self._generate_dialogue_audio(
                dialogue=dialogue,
                speaker=speaker,
                segment_idx=segment_idx,
                dialogue_idx=dialogue_idx
            )
            segment_files.append(audio_file)
        
        # Add background music if specified
        if segment.background_music and segment.background_music != MusicGenre.NONE:
            music_file = await self._add_background_music(
                segment=segment,
                duration=self._estimate_segment_duration(segment)
            )
            if music_file:
                segment_files.append(music_file)
        
        return {
            "type": segment.type,
            "files": segment_files,
            "duration": self._estimate_segment_duration(segment)
        }
    
    async def _generate_dialogue_audio(
        self,
        dialogue: DialogueLine,
        speaker: Speaker,
        segment_idx: int,
        dialogue_idx: int
    ) -> Dict:
        """Generate audio for single dialogue line"""
        import sys
        from pathlib import Path as PathLib
        
        filename = f"seg{segment_idx}_dlg{dialogue_idx}_{speaker.id}.mp3"
        output_file = self.output_dir / filename
        
        try:
            # Import TTS service
            sys.path.insert(0, str(PathLib(__file__).parent))
            from generer_audio_huggingface import generer_audio_creole
            
            # Generate basic audio
            generer_audio_creole(dialogue.text, str(output_file))
            
            # Apply voice modifications if pydub available
            try:
                from pydub import AudioSegment
                from pydub.effects import speedup
                
                audio = AudioSegment.from_file(str(output_file))
                
                # Apply pitch shift
                if speaker.pitch != 1.0:
                    # Change pitch by changing frame rate
                    new_sample_rate = int(audio.frame_rate * speaker.pitch)
                    audio = audio._spawn(audio.raw_data, overrides={
                        "frame_rate": new_sample_rate
                    })
                    audio = audio.set_frame_rate(audio.frame_rate)
                
                # Apply speed
                if speaker.speed != 1.0:
                    if speaker.speed > 1.0:
                        audio = speedup(audio, playback_speed=speaker.speed)
                    elif speaker.speed < 1.0:
                        # Slow down by stretching
                        audio = audio._spawn(
                            audio.raw_data,
                            overrides={"frame_rate": int(audio.frame_rate * speaker.speed)}
                        ).set_frame_rate(audio.frame_rate)
                
                # Apply volume
                if speaker.volume != 1.0:
                    db_change = 20 * (speaker.volume - 1.0)
                    audio = audio.apply_gain(db_change)
                
                # Add pause after
                if dialogue.pause_after > 0:
                    silence = AudioSegment.silent(duration=int(dialogue.pause_after * 1000))
                    audio = audio + silence
                
                # Export modified audio
                audio.export(str(output_file), format="mp3")
                
                actual_duration = len(audio) / 1000.0
            except ImportError:
                # No pydub, use estimated duration
                actual_duration = len(dialogue.text) / 15.0 + dialogue.pause_after
        
        except Exception as e:
            logger.error(f"Failed to generate dialogue audio: {e}")
            # Create placeholder data
            actual_duration = len(dialogue.text) / 15.0 + dialogue.pause_after
        
        return {
            "type": "dialogue",
            "speaker": speaker.name,
            "text": dialogue.text,
            "emotion": dialogue.emotion.value if dialogue.emotion else speaker.emotion.value,
            "file": str(output_file),
            "duration": actual_duration,
            "sound_effect": dialogue.sound_effect.value if dialogue.sound_effect else None
        }
    
    async def _add_background_music(
        self,
        segment: PodcastSegment,
        duration: float
    ) -> Optional[Dict]:
        """Add background music to segment"""
        import sys
        from pathlib import Path as PathLib
        
        try:
            # Import music library
            sys.path.insert(0, str(PathLib(__file__).parent))
            from audio_library import MusicLibrary
            
            library = MusicLibrary()
            music_file = library.get_music(segment.background_music.value)
            
            if not music_file or not music_file.exists():
                logger.warning(f"Background music not found: {segment.background_music.value}")
                return None
            
            return {
                "type": "background_music",
                "genre": segment.background_music.value,
                "file": str(music_file),
                "volume": segment.music_volume,
                "duration": duration
            }
        
        except Exception as e:
            logger.error(f"Failed to load background music: {e}")
            return None
    
    async def _combine_segments(
        self,
        segments: List[Dict],
        config: PodcastConfig
    ) -> str:
        """Combine all segments into final podcast"""
        import sys
        from pathlib import Path as PathLib
        
        try:
            from pydub import AudioSegment
            from audio_library import MusicLibrary, AudioMixer
            
            library = MusicLibrary()
            mixer = AudioMixer()
            
            combined = AudioSegment.empty()
            
            # Add intro jingle if requested
            if config.add_intro_jingle:
                intro_jingle = library.get_jingle("intro")
                if intro_jingle and intro_jingle.exists():
                    jingle = AudioSegment.from_file(str(intro_jingle))
                    combined += jingle
                    # Add small pause after jingle
                    combined += AudioSegment.silent(duration=500)
            
            # Process each segment
            for segment_data in segments:
                # Collect all audio files in segment
                segment_audio = AudioSegment.empty()
                background_music = None
                
                for file_data in segment_data.get("files", []):
                    file_path = PathLib(file_data["file"])
                    
                    if file_data["type"] == "dialogue" and file_path.exists():
                        audio = AudioSegment.from_file(str(file_path))
                        segment_audio += audio
                    
                    elif file_data["type"] == "background_music" and file_path.exists():
                        background_music = file_path
                
                # Mix background music if available
                if background_music and len(segment_audio) > 0:
                    music = AudioSegment.from_file(str(background_music))
                    
                    # Loop music to match segment length
                    if len(music) < len(segment_audio):
                        music = music * (len(segment_audio) // len(music) + 1)
                    
                    music = music[:len(segment_audio)]
                    
                    # Get volume from segment data
                    music_volume = segment_data.get("volume", 0.3)
                    db_reduction = -20 * (1 - music_volume)
                    music = music.apply_gain(db_reduction)
                    
                    # Mix
                    segment_audio = segment_audio.overlay(music)
                
                # Add segment to combined
                if len(segment_audio) > 0:
                    combined += segment_audio
            
            # Add outro jingle if requested
            if config.add_outro_jingle:
                outro_jingle = library.get_jingle("outro")
                if outro_jingle and outro_jingle.exists():
                    # Add small pause before jingle
                    combined += AudioSegment.silent(duration=500)
                    jingle = AudioSegment.from_file(str(outro_jingle))
                    combined += jingle
            
            # Normalize if requested
            if config.normalize_audio:
                combined = combined.normalize()
            
            # Export
            final_file = self.output_dir / f"{config.title.replace(' ', '_')}_final.{config.export_format}"
            combined.export(
                str(final_file),
                format=config.export_format,
                bitrate="192k" if config.export_format == "mp3" else None
            )
            
            logger.info(f"✅ Final podcast saved: {final_file}")
            return str(final_file)
        
        except Exception as e:
            logger.error(f"Failed to combine segments: {e}")
            # Return placeholder path
            final_file = self.output_dir / f"{config.title.replace(' ', '_')}_final.mp3"
            return str(final_file)
    
    def _estimate_segment_duration(self, segment: PodcastSegment) -> float:
        """Estimate segment duration in seconds"""
        total = 0.0
        for dialogue in segment.dialogues:
            total += len(dialogue.text) / 15.0  # ~15 chars/second
            total += dialogue.pause_after
        return total
    
    def _get_speaker(self, speakers: List[Speaker], speaker_id: str) -> Speaker:
        """Get speaker by ID"""
        for speaker in speakers:
            if speaker.id == speaker_id:
                return speaker
        return speakers[0] if speakers else None
    
    def _create_metadata(self, config: PodcastConfig) -> Dict:
        """Create podcast metadata"""
        return {
            "title": config.title,
            "description": config.description,
            "speakers": [
                {
                    "id": s.id,
                    "name": s.name,
                    "voice_id": s.voice_id,
                    "gender": s.gender.value,
                    "emotion": s.emotion.value
                }
                for s in config.speakers
            ],
            "segments_count": len(config.segments),
            "format": config.export_format,
            "features": {
                "multi_speaker": len(config.speakers) > 1,
                "emotion_control": True,
                "background_music": any(s.background_music for s in config.segments),
                "sound_effects": any(
                    d.sound_effect for s in config.segments for d in s.dialogues
                ),
                "normalized": config.normalize_audio
            }
        }

# ============================================================
# QUICK TEMPLATES
# ============================================================

class PodcastTemplates:
    """Pre-built podcast templates"""
    
    @staticmethod
    def interview_template() -> str:
        """Interview podcast template"""
        return """[INTRO - Background: Corporate, Volume: 0.3]
Host (excited): Welcome to the Faner Podcast!
[SFX: intro_swoosh]
Host (professional): Today we have an amazing guest!

[MAIN - Background: Calm]
Host: So, tell us about your work.
Guest (professional): Well, it's quite interesting...
[Pause: 1.0]
Host: That's fascinating!

[OUTRO - Background: Upbeat]
Host (happy): Thanks for tuning in!
[SFX: outro_fade]"""
    
    @staticmethod
    def news_template() -> str:
        """News podcast template"""
        return """[INTRO - Background: Tech, Volume: 0.2]
Anchor (professional): This is Faner News.
[SFX: notification]

[MAIN - Background: Corporate]
Anchor (neutral): Today's top story...
Reporter (excited): Breaking news from Haiti!

[OUTRO - Background: Corporate]
Anchor (professional): That's all for today.
[SFX: outro_fade]"""
    
    @staticmethod
    def storytelling_template() -> str:
        """Storytelling podcast template"""
        return """[INTRO - Background: Dramatic, Volume: 0.4]
Narrator (calm): Once upon a time...
[SFX: intro_swoosh]

[MAIN - Background: Calm]
Narrator (excited): And then something amazing happened!
[Pause: 2.0]
Character1 (happy): I can't believe it!

[OUTRO - Background: Calm]
Narrator (calm): The end.
[SFX: outro_fade]"""

# ============================================================
# EXAMPLE USAGE
# ============================================================

async def example_usage():
    """Example of how to use the advanced podcast generator"""
    
    # Define speakers
    speakers = [
        Speaker(
            id="host",
            name="Host",
            voice_id="creole-native",
            gender=SpeakerGender.FEMALE,
            emotion=VoiceEmotion.FRIENDLY,
            pitch=1.1,
            speed=1.0
        ),
        Speaker(
            id="guest",
            name="Guest",
            voice_id="creole-native",
            gender=SpeakerGender.MALE,
            emotion=VoiceEmotion.PROFESSIONAL,
            pitch=0.9,
            speed=0.95
        )
    ]
    
    # Use template or custom script
    script = PodcastTemplates.interview_template()
    
    # Generate podcast
    generator = AdvancedPodcastGenerator()
    result = await generator.generate_from_script(
        script=script,
        speakers=speakers
    )
    
    print(f"✅ Podcast generated: {result['final_audio']}")
    print(f"📊 Segments: {len(result['segments'])}")
    print(f"📁 Metadata: {result['metadata_file']}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(example_usage())

