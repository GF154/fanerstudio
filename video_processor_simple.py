#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎥 Video Processor - Add Voiceover, Captions, Music
Pwosesè Videyo - Ajoute Voiceover, Captions, Mizik
"""

import os
import subprocess
import tempfile
from typing import List, Dict, Optional
from datetime import datetime

try:
    import ffmpeg
    FFMPEG_AVAILABLE = True
except ImportError:
    FFMPEG_AVAILABLE = False
    print("⚠️ ffmpeg-python not available - install with: pip install ffmpeg-python")


class VideoProcessor:
    """
    Professional video processing with FFmpeg
    """
    
    def __init__(self):
        # Check if FFmpeg is installed on system
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            self.ffmpeg_installed = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.ffmpeg_installed = False
            print("⚠️ FFmpeg not installed on system")
    
    def add_voiceover(
        self,
        video_file: str,
        audio_file: str,
        output_file: str,
        video_volume: float = 0.5,
        audio_volume: float = 1.0
    ) -> str:
        """
        Add voiceover to video
        
        Args:
            video_file: Input video file
            audio_file: Voiceover audio file
            output_file: Output video file
            video_volume: Original video volume (0.0 to 1.0)
            audio_volume: Voiceover volume (0.0 to 1.0)
            
        Returns:
            Path to output video file
        """
        if not self.ffmpeg_installed:
            raise RuntimeError("FFmpeg not installed")
        
        try:
            # Build FFmpeg command
            cmd = [
                'ffmpeg',
                '-i', video_file,
                '-i', audio_file,
                '-filter_complex',
                f'[0:a]volume={video_volume}[a1];[1:a]volume={audio_volume}[a2];[a1][a2]amix=inputs=2:duration=first[a]',
                '-map', '0:v',
                '-map', '[a]',
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-y',  # Overwrite output
                output_file
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return output_file
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFmpeg error: {e.stderr.decode()}")
    
    def add_captions(
        self,
        video_file: str,
        captions: List[Dict],
        output_file: str,
        font: str = "Arial",
        font_size: int = 24,
        font_color: str = "white",
        background: bool = True
    ) -> str:
        """
        Add captions to video
        
        Args:
            video_file: Input video file
            captions: List of caption dicts with 'start', 'end', 'text'
            output_file: Output video file
            font: Font name
            font_size: Font size
            font_color: Font color
            background: Add background to text
            
        Returns:
            Path to output video file
        """
        if not self.ffmpeg_installed:
            raise RuntimeError("FFmpeg not installed")
        
        try:
            # Create SRT file
            srt_file = tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False, encoding='utf-8')
            
            for i, caption in enumerate(captions, 1):
                srt_file.write(f"{i}\n")
                srt_file.write(f"{caption['start']} --> {caption['end']}\n")
                srt_file.write(f"{caption['text']}\n\n")
            
            srt_file.close()
            
            # Add subtitles with FFmpeg
            subtitle_style = f"Fontname={font},Fontsize={font_size},PrimaryColour=&H{self._color_to_hex(font_color)}"
            if background:
                subtitle_style += ",BackColour=&H80000000,BorderStyle=4"
            
            cmd = [
                'ffmpeg',
                '-i', video_file,
                '-vf', f"subtitles={srt_file.name}:force_style='{subtitle_style}'",
                '-c:a', 'copy',
                '-y',
                output_file
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Clean up SRT file
            os.unlink(srt_file.name)
            
            return output_file
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFmpeg error: {e.stderr.decode()}")
    
    def add_background_music(
        self,
        video_file: str,
        music_file: str,
        output_file: str,
        video_volume: float = 1.0,
        music_volume: float = 0.3
    ) -> str:
        """
        Add background music to video
        
        Args:
            video_file: Input video file
            music_file: Background music file
            output_file: Output video file
            video_volume: Original video volume (0.0 to 1.0)
            music_volume: Music volume (0.0 to 1.0)
            
        Returns:
            Path to output video file
        """
        if not self.ffmpeg_installed:
            raise RuntimeError("FFmpeg not installed")
        
        try:
            # Mix audio with FFmpeg
            cmd = [
                'ffmpeg',
                '-i', video_file,
                '-i', music_file,
                '-filter_complex',
                f'[0:a]volume={video_volume}[a1];[1:a]volume={music_volume},aloop=loop=-1:size=2e+09[a2];[a1][a2]amix=inputs=2:duration=first[a]',
                '-map', '0:v',
                '-map', '[a]',
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',  # End when shortest stream ends
                '-y',
                output_file
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return output_file
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"FFmpeg error: {e.stderr.decode()}")
    
    def get_video_info(self, video_file: str) -> Dict:
        """
        Get video metadata
        
        Returns:
            Dict with duration, resolution, size, format
        """
        if not self.ffmpeg_installed:
            return {
                "duration": "00:00",
                "resolution": "Unknown",
                "size": "Unknown",
                "format": "Unknown"
            }
        
        try:
            # Use ffprobe to get video info
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                video_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, check=True)
            import json
            data = json.loads(result.stdout)
            
            # Extract info
            duration = float(data['format'].get('duration', 0))
            duration_formatted = self.format_duration(duration)
            
            # Get video stream
            video_stream = next((s for s in data['streams'] if s['codec_type'] == 'video'), None)
            resolution = f"{video_stream['width']}x{video_stream['height']}" if video_stream else "Unknown"
            
            size = os.path.getsize(video_file)
            size_mb = f"{size / (1024 * 1024):.2f} MB"
            
            format_name = data['format'].get('format_name', 'Unknown')
            
            return {
                "duration": duration_formatted,
                "duration_seconds": duration,
                "resolution": resolution,
                "size": size_mb,
                "format": format_name
            }
            
        except Exception as e:
            print(f"Error getting video info: {e}")
            return {
                "duration": "00:00",
                "resolution": "Unknown",
                "size": "Unknown",
                "format": "Unknown"
            }
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration as MM:SS"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    @staticmethod
    def _color_to_hex(color: str) -> str:
        """Convert color name to hex for FFmpeg"""
        colors = {
            'white': 'FFFFFF',
            'black': '000000',
            'red': 'FF0000',
            'green': '00FF00',
            'blue': '0000FF',
            'yellow': 'FFFF00'
        }
        return colors.get(color.lower(), 'FFFFFF')


# Quick test
if __name__ == "__main__":
    print("🎥 Testing Video Processor...")
    
    try:
        processor = VideoProcessor()
        
        if processor.ffmpeg_installed:
            print("✅ FFmpeg installed and ready!")
            print("📝 Use add_voiceover(), add_captions(), add_background_music()")
        else:
            print("❌ FFmpeg not installed")
            print("💡 Install FFmpeg:")
            print("   Windows: choco install ffmpeg")
            print("   Mac: brew install ffmpeg")
            print("   Linux: sudo apt-get install ffmpeg")
        
    except Exception as e:
        print(f"❌ Error: {e}")

