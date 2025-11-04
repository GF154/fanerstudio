#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚙️ Video Processing and Quality Enhancement
Pwosesis ak Amelyorasyon Kalite Videyo

Features:
- Trim/cut videos
- Merge videos
- Change resolution
- Change framerate
- Convert formats
- Compress videos
"""

from pathlib import Path
from typing import Optional, Literal
import logging

logger = logging.getLogger('FanerStudio.VideoProcessor')


class VideoProcessor:
    """
    Professional video processing
    Pwosesis pwofesyonèl pou videyo
    """
    
    def __init__(self):
        self.ffmpeg_available = self._check_ffmpeg()
    
    def _check_ffmpeg(self) -> bool:
        """Check if ffmpeg is available"""
        try:
            import subprocess
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            logger.warning("ffmpeg not available")
            return False
    
    def trim_video(
        self,
        input_path: Path,
        output_path: Optional[Path] = None,
        start_time: str = "00:00:00",
        end_time: Optional[str] = None,
        duration: Optional[str] = None
    ) -> Path:
        """
        Trim video to specific time range
        Koupe videyo nan yon peryòd espesifik
        
        Args:
            input_path: Input video path
            output_path: Output video path
            start_time: Start time (HH:MM:SS)
            end_time: End time (HH:MM:SS) OR
            duration: Duration from start (HH:MM:SS)
        """
        if not self.ffmpeg_available:
            raise RuntimeError("ffmpeg required for video processing")
        
        output_path = output_path or input_path.parent / f"{input_path.stem}_trimmed{input_path.suffix}"
        
        logger.info(f"Trimming video: {input_path.name}")
        
        import subprocess
        
        cmd = [
            "ffmpeg",
            "-i", str(input_path),
            "-ss", start_time,
            "-y"
        ]
        
        if end_time:
            cmd.extend(["-to", end_time])
        elif duration:
            cmd.extend(["-t", duration])
        
        cmd.extend([
            "-c", "copy",  # Copy without re-encoding (fast)
            str(output_path)
        ])
        
        result = subprocess.run(cmd, capture_output=True, timeout=300)
        
        if result.returncode == 0:
            logger.info(f"✅ Video trimmed: {output_path}")
            return output_path
        else:
            raise RuntimeError(f"ffmpeg error: {result.stderr.decode()}")
    
    def merge_videos(
        self,
        video_paths: list,
        output_path: Path
    ) -> Path:
        """
        Merge multiple videos
        Konbine plizyè videyo
        """
        if not self.ffmpeg_available:
            raise RuntimeError("ffmpeg required")
        
        logger.info(f"Merging {len(video_paths)} videos")
        
        # Create concat file
        concat_file = output_path.parent / "concat_list.txt"
        with open(concat_file, 'w') as f:
            for video_path in video_paths:
                f.write(f"file '{Path(video_path).absolute()}'\n")
        
        import subprocess
        
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",
            "-y",
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=600)
        
        # Cleanup
        concat_file.unlink()
        
        if result.returncode == 0:
            logger.info(f"✅ Videos merged: {output_path}")
            return output_path
        else:
            raise RuntimeError(f"ffmpeg error: {result.stderr.decode()}")
    
    def change_resolution(
        self,
        input_path: Path,
        output_path: Optional[Path] = None,
        width: int = 1920,
        height: int = 1080
    ) -> Path:
        """
        Change video resolution
        Chanje rezolisyon videyo
        """
        if not self.ffmpeg_available:
            raise RuntimeError("ffmpeg required")
        
        output_path = output_path or input_path.parent / f"{input_path.stem}_{width}x{height}{input_path.suffix}"
        
        logger.info(f"Changing resolution to {width}x{height}")
        
        import subprocess
        
        cmd = [
            "ffmpeg",
            "-i", str(input_path),
            "-vf", f"scale={width}:{height}",
            "-c:a", "copy",
            "-y",
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=600)
        
        if result.returncode == 0:
            logger.info(f"✅ Resolution changed: {output_path}")
            return output_path
        else:
            raise RuntimeError(f"ffmpeg error: {result.stderr.decode()}")
    
    def convert_format(
        self,
        input_path: Path,
        output_format: Literal["mp4", "avi", "mov", "mkv", "webm"],
        quality: Literal["high", "medium", "low"] = "high"
    ) -> Path:
        """
        Convert video format
        Konvèti fòma videyo
        """
        if not self.ffmpeg_available:
            raise RuntimeError("ffmpeg required")
        
        output_path = input_path.parent / f"{input_path.stem}.{output_format}"
        
        logger.info(f"Converting to {output_format}")
        
        # Quality settings
        crf = {"high": "18", "medium": "23", "low": "28"}[quality]
        
        import subprocess
        
        cmd = [
            "ffmpeg",
            "-i", str(input_path),
            "-c:v", "libx264",
            "-crf", crf,
            "-preset", "medium",
            "-c:a", "aac",
            "-b:a", "192k",
            "-y",
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=600)
        
        if result.returncode == 0:
            logger.info(f"✅ Format converted: {output_path}")
            return output_path
        else:
            raise RuntimeError(f"ffmpeg error: {result.stderr.decode()}")
    
    def compress_video(
        self,
        input_path: Path,
        output_path: Optional[Path] = None,
        target_size_mb: Optional[float] = None,
        crf: int = 28
    ) -> Path:
        """
        Compress video for web
        Konprese videyo pou wèb
        """
        if not self.ffmpeg_available:
            raise RuntimeError("ffmpeg required")
        
        output_path = output_path or input_path.parent / f"{input_path.stem}_compressed{input_path.suffix}"
        
        logger.info(f"Compressing video (CRF={crf})")
        
        import subprocess
        
        cmd = [
            "ffmpeg",
            "-i", str(input_path),
            "-c:v", "libx264",
            "-crf", str(crf),
            "-preset", "slower",
            "-c:a", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart",  # Web optimization
            "-y",
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=600)
        
        if result.returncode == 0:
            original_size = input_path.stat().st_size / (1024 * 1024)
            new_size = output_path.stat().st_size / (1024 * 1024)
            logger.info(f"✅ Video compressed: {original_size:.2f}MB → {new_size:.2f}MB")
            return output_path
        else:
            raise RuntimeError(f"ffmpeg error: {result.stderr.decode()}")


# Global processor instance
video_processor = VideoProcessor()

