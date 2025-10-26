#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 Video Processing Service
Sèvis pou pwosese videyo (voiceover, SFX, captions, etc.)
"""

from pathlib import Path
from datetime import datetime
import subprocess
import os
import sys
from typing import Optional, List, Dict

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class VideoService:
    """Sèvis pou pwosese videyo"""
    
    def __init__(self):
        """Initialize video service"""
        self.output_dir = Path("output/videos")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if ffmpeg is available
        self.ffmpeg_available = self._check_ffmpeg()
        
        if self.ffmpeg_available:
            print("✅ Video Service initialized (ffmpeg available)")
        else:
            print("⚠️  Video Service initialized (ffmpeg NOT available)")
            print("   Install ffmpeg for full video features")
    
    def _check_ffmpeg(self) -> bool:
        """Check if ffmpeg is installed"""
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    # ============================================================
    # VIDEO VOICEOVER
    # ============================================================
    
    async def add_voiceover(
        self,
        video_file: Path,
        voiceover_text: str,
        voice: str = "creole-native",
        mix_volume: float = 0.5
    ) -> Path:
        """
        Ajoute voiceover nan videyo
        
        Args:
            video_file: Fichye videyo orijinal
            voiceover_text: Tèks pou narration
            voice: Vwa pou itilize
            mix_volume: Volim pou orijinal audio (0.0-1.0)
        
        Returns:
            Path: Videyo ak voiceover
        """
        if not self.ffmpeg_available:
            raise RuntimeError("ffmpeg pa disponib! Enstale ffmpeg pou pwosese videyo.")
        
        try:
            from app.services.tts_service import TTSService
            
            print(f"\n🎬 AJOUTE VOICEOVER")
            print(f"   Videyo: {video_file.name}")
            print(f"   Vwa: {voice}\n")
            
            # 1. Generate voiceover audio
            tts = TTSService()
            voiceover_audio = Path("output") / f"voiceover_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            await tts.text_to_speech_file(voiceover_text, str(voiceover_audio), voice)
            
            print(f"   ✓ Voiceover audio generated")
            
            # 2. Mix voiceover with video
            output_file = self.output_dir / f"voiceover_{video_file.stem}_{datetime.now().strftime('%H%M%S')}.mp4"
            
            # ffmpeg command to mix audio
            cmd = [
                "ffmpeg", "-i", str(video_file),
                "-i", str(voiceover_audio),
                "-filter_complex",
                f"[0:a]volume={mix_volume}[a1];[1:a]volume=1.0[a2];[a1][a2]amix=inputs=2[a]",
                "-map", "0:v",
                "-map", "[a]",
                "-c:v", "copy",
                "-c:a", "aac",
                "-y",
                str(output_file)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            print(f"   ✓ Voiceover mixed successfully")
            print(f"   📁 Output: {output_file.name}\n")
            
            # Cleanup temp file
            voiceover_audio.unlink(missing_ok=True)
            
            return output_file
            
        except Exception as e:
            print(f"❌ Error adding voiceover: {e}")
            raise
    
    # ============================================================
    # SFX & MUSIC
    # ============================================================
    
    async def add_background_music(
        self,
        video_file: Path,
        music_file: Path,
        music_volume: float = 0.3
    ) -> Path:
        """
        Ajoute mizik background
        
        Args:
            video_file: Fichye videyo
            music_file: Fichye mizik
            music_volume: Volim mizik (0.0-1.0)
        
        Returns:
            Path: Videyo ak mizik
        """
        if not self.ffmpeg_available:
            raise RuntimeError("ffmpeg pa disponib!")
        
        try:
            output_file = self.output_dir / f"music_{video_file.stem}_{datetime.now().strftime('%H%M%S')}.mp4"
            
            # Loop music if shorter than video
            cmd = [
                "ffmpeg", "-i", str(video_file),
                "-stream_loop", "-1", "-i", str(music_file),
                "-filter_complex",
                f"[0:a]volume=1.0[a1];[1:a]volume={music_volume}[a2];[a1][a2]amix=inputs=2:duration=first[a]",
                "-map", "0:v",
                "-map", "[a]",
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                "-y",
                str(output_file)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            print(f"✓ Background music added: {output_file.name}")
            return output_file
            
        except Exception as e:
            print(f"❌ Error adding music: {e}")
            raise
    
    # ============================================================
    # CAPTIONS / SUBTITLES
    # ============================================================
    
    async def generate_captions(
        self,
        video_file: Path,
        language: str = "ht"
    ) -> Path:
        """
        Jenere soutit ak Whisper STT
        
        Args:
            video_file: Fichye videyo
            language: Lang (ht=Kreyòl, en=Anglè, fr=Frans)
        
        Returns:
            Path: Fichye SRT soutit
        """
        try:
            from app.services.stt_service import STTService
            
            print(f"\n📝 JENERE SOUTIT")
            print(f"   Videyo: {video_file.name}")
            print(f"   Lang: {language}\n")
            
            # 1. Extract audio from video
            audio_file = Path("output") / f"temp_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            
            if self.ffmpeg_available:
                cmd = [
                    "ffmpeg", "-i", str(video_file),
                    "-vn",  # No video
                    "-acodec", "mp3",
                    "-y",
                    str(audio_file)
                ]
                subprocess.run(cmd, check=True, capture_output=True)
                print(f"   ✓ Audio extracted")
            else:
                raise RuntimeError("ffmpeg needed to extract audio")
            
            # 2. Transcribe with STT
            stt = STTService()
            transcription = await stt.transcribe_audio(str(audio_file), language=language)
            
            # 3. Generate SRT file
            srt_file = self.output_dir / f"captions_{video_file.stem}.srt"
            
            # Simple SRT generation (TODO: Add proper timestamps)
            lines = transcription.split('. ')
            
            with open(srt_file, 'w', encoding='utf-8') as f:
                for i, line in enumerate(lines, 1):
                    if line.strip():
                        start_time = self._seconds_to_srt_time(i * 5)
                        end_time = self._seconds_to_srt_time((i + 1) * 5)
                        
                        f.write(f"{i}\n")
                        f.write(f"{start_time} --> {end_time}\n")
                        f.write(f"{line.strip()}\n\n")
            
            print(f"   ✓ Captions generated: {srt_file.name}\n")
            
            # Cleanup
            audio_file.unlink(missing_ok=True)
            
            return srt_file
            
        except Exception as e:
            print(f"❌ Error generating captions: {e}")
            raise
    
    async def burn_captions(
        self,
        video_file: Path,
        srt_file: Path
    ) -> Path:
        """
        Ajoute soutit dirèkteman nan videyo
        
        Args:
            video_file: Fichye videyo
            srt_file: Fichye SRT soutit
        
        Returns:
            Path: Videyo ak soutit
        """
        if not self.ffmpeg_available:
            raise RuntimeError("ffmpeg pa disponib!")
        
        try:
            output_file = self.output_dir / f"captioned_{video_file.stem}.mp4"
            
            # Escape subtitle file path for ffmpeg
            srt_path = str(srt_file).replace('\\', '/')
            
            cmd = [
                "ffmpeg", "-i", str(video_file),
                "-vf", f"subtitles='{srt_path}'",
                "-c:a", "copy",
                "-y",
                str(output_file)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            print(f"✓ Captions burned: {output_file.name}")
            return output_file
            
        except Exception as e:
            print(f"❌ Error burning captions: {e}")
            raise
    
    # ============================================================
    # AUDIO PROCESSING
    # ============================================================
    
    async def denoise_audio(
        self,
        video_file: Path,
        noise_reduction: int = 20
    ) -> Path:
        """
        Retire bri nan audio videyo a
        
        Args:
            video_file: Fichye videyo
            noise_reduction: Nivo reduction (0-100, default: 20)
        
        Returns:
            Path: Videyo ak audio netwaye
        """
        if not self.ffmpeg_available:
            raise RuntimeError("ffmpeg pa disponib!")
        
        try:
            output_file = self.output_dir / f"denoised_{video_file.stem}.mp4"
            
            # Use ffmpeg highpass and lowpass filters to reduce noise
            cmd = [
                "ffmpeg", "-i", str(video_file),
                "-af", f"highpass=f=200,lowpass=f=3000,volume=1.5",
                "-c:v", "copy",
                "-y",
                str(output_file)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            print(f"✓ Audio denoised: {output_file.name}")
            return output_file
            
        except Exception as e:
            print(f"❌ Error denoising audio: {e}")
            raise
    
    async def normalize_audio(
        self,
        video_file: Path
    ) -> Path:
        """
        Nòmalize volim audio
        
        Args:
            video_file: Fichye videyo
        
        Returns:
            Path: Videyo ak audio normalized
        """
        if not self.ffmpeg_available:
            raise RuntimeError("ffmpeg pa disponib!")
        
        try:
            output_file = self.output_dir / f"normalized_{video_file.stem}.mp4"
            
            cmd = [
                "ffmpeg", "-i", str(video_file),
                "-af", "loudnorm",
                "-c:v", "copy",
                "-y",
                str(output_file)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            print(f"✓ Audio normalized: {output_file.name}")
            return output_file
            
        except Exception as e:
            print(f"❌ Error normalizing audio: {e}")
            raise
    
    # ============================================================
    # UTILITY FUNCTIONS
    # ============================================================
    
    def _seconds_to_srt_time(self, seconds: float) -> str:
        """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    async def get_video_info(
        self,
        video_file: Path
    ) -> Dict:
        """
        Jwenn enfòmasyon sou yon videyo
        
        Args:
            video_file: Fichye videyo
        
        Returns:
            dict: Enfòmasyon videyo
        """
        if not self.ffmpeg_available:
            return {"error": "ffmpeg not available"}
        
        try:
            cmd = [
                "ffprobe", "-v", "quiet",
                "-print_format", "json",
                "-show_format", "-show_streams",
                str(video_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            import json
            data = json.loads(result.stdout)
            
            # Extract useful info
            video_stream = next((s for s in data.get("streams", []) if s["codec_type"] == "video"), {})
            audio_stream = next((s for s in data.get("streams", []) if s["codec_type"] == "audio"), {})
            
            return {
                "duration": float(data.get("format", {}).get("duration", 0)),
                "size": int(data.get("format", {}).get("size", 0)),
                "bitrate": int(data.get("format", {}).get("bit_rate", 0)),
                "width": video_stream.get("width"),
                "height": video_stream.get("height"),
                "fps": eval(video_stream.get("r_frame_rate", "0/1")),
                "video_codec": video_stream.get("codec_name"),
                "audio_codec": audio_stream.get("codec_name"),
                "has_audio": bool(audio_stream)
            }
            
        except Exception as e:
            return {"error": str(e)}


# Global instance
video_service = VideoService()


if __name__ == "__main__":
    import asyncio
    
    print("🎬 Video Service Test")
    print("=" * 60)
    print(f"ffmpeg available: {video_service.ffmpeg_available}")
    print("=" * 60)

