#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 Professional Video Management System
Sistèm Pwofesyonèl pou Jere Videyo

Features:
- Organized video storage
- Complete metadata tracking
- Thumbnail generation
- Progress tracking for long videos
- Format conversion
- Quality optimization
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging
from dataclasses import dataclass, asdict

logger = logging.getLogger('FanerStudio.VideoManager')


@dataclass
class VideoFile:
    """Metadata for video file"""
    id: str
    filename: str
    original_filename: str
    file_path: str
    url: str
    format: str
    size_bytes: int
    size_mb: float
    duration_seconds: float
    resolution: str  # "1920x1080"
    width: int
    height: int
    fps: float
    video_codec: str
    audio_codec: str
    bitrate: str
    has_audio: bool
    thumbnail_url: Optional[str]
    preview_url: Optional[str]
    created_by: Optional[str]
    project_id: Optional[str]
    project_type: str  # original, voiceover, captioned, edited
    tags: List[str]
    is_public: bool
    processing_status: str  # pending, processing, completed, error
    created_at: str
    last_accessed: Optional[str]
    access_count: int
    
    def to_dict(self) -> dict:
        return asdict(self)


class VideoManager:
    """
    Manage all video files professionally
    Jere tout fichye videyo pwofesyonèlman
    """
    
    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path("video_storage")
        
        # Create organized directory structure
        self.directories = {
            "originals": self.base_dir / "originals",
            "voiceovers": self.base_dir / "voiceovers",
            "captioned": self.base_dir / "captioned",
            "edited": self.base_dir / "edited",
            "thumbnails": self.base_dir / "thumbnails",
            "previews": self.base_dir / "previews",
            "temp": self.base_dir / "temp",
            "cache": self.base_dir / "cache"
        }
        
        # Create all directories
        for directory in self.directories.values():
            directory.mkdir(parents=True, exist_ok=True)
        
        # Metadata storage
        self.metadata_file = self.base_dir / "video_metadata.json"
        self.metadata = self._load_metadata()
        
        # Check ffmpeg availability
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
            logger.warning("ffmpeg not available - video processing will be limited")
            return False
    
    def _load_metadata(self) -> Dict[str, VideoFile]:
        """Load metadata from file"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        k: VideoFile(**v) for k, v in data.items()
                    }
            except Exception as e:
                logger.error(f"Failed to load metadata: {e}")
        return {}
    
    def _save_metadata(self):
        """Save metadata to file"""
        try:
            data = {k: v.to_dict() for k, v in self.metadata.items()}
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")
    
    def store_video(
        self,
        video_path: Path,
        project_type: str = "original",
        user_id: Optional[str] = None,
        project_id: Optional[str] = None,
        tags: List[str] = None,
        is_public: bool = False,
        generate_thumbnail: bool = True
    ) -> VideoFile:
        """
        Store video file with metadata
        
        Args:
            video_path: Path to video file
            project_type: Type (original, voiceover, captioned, edited)
            user_id: User who created it
            project_id: Associated project ID
            tags: Tags for searching
            is_public: Whether file is publicly accessible
            generate_thumbnail: Generate thumbnail image
        
        Returns:
            VideoFile metadata object
        """
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Generate unique ID
        file_id = self._generate_file_id(video_path)
        
        # Determine storage directory
        storage_dir = self.directories.get(f"{project_type}s", self.directories["originals"])
        
        # Create user subdirectory if user_id provided
        if user_id:
            storage_dir = storage_dir / user_id
            storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_ext = video_path.suffix
        new_filename = f"{project_type}_{timestamp}_{file_id[:8]}{file_ext}"
        
        # Copy file to storage
        destination = storage_dir / new_filename
        import shutil
        shutil.copy2(video_path, destination)
        
        # Extract video metadata
        video_info = self._extract_video_info(destination)
        
        # Generate thumbnail
        thumbnail_url = None
        if generate_thumbnail and self.ffmpeg_available:
            thumbnail_url = self._generate_thumbnail(destination, file_id)
        
        # Generate URL (relative to API)
        relative_path = destination.relative_to(self.base_dir)
        url = f"/video/{relative_path}"
        
        # Create metadata object
        video_file = VideoFile(
            id=file_id,
            filename=new_filename,
            original_filename=video_path.name,
            file_path=str(destination),
            url=url,
            format=file_ext[1:],
            size_bytes=destination.stat().st_size,
            size_mb=round(destination.stat().st_size / (1024 * 1024), 2),
            duration_seconds=video_info.get("duration", 0.0),
            resolution=video_info.get("resolution", "unknown"),
            width=video_info.get("width", 0),
            height=video_info.get("height", 0),
            fps=video_info.get("fps", 0.0),
            video_codec=video_info.get("video_codec", "unknown"),
            audio_codec=video_info.get("audio_codec", "unknown"),
            bitrate=video_info.get("bitrate", "unknown"),
            has_audio=video_info.get("has_audio", False),
            thumbnail_url=thumbnail_url,
            preview_url=None,
            created_by=user_id,
            project_id=project_id,
            project_type=project_type,
            tags=tags or [],
            is_public=is_public,
            processing_status="completed",
            created_at=datetime.now().isoformat(),
            last_accessed=None,
            access_count=0
        )
        
        # Store metadata
        self.metadata[file_id] = video_file
        self._save_metadata()
        
        logger.info(f"✅ Video stored: {new_filename} ({video_file.size_mb}MB, {video_file.resolution})")
        
        return video_file
    
    def _generate_file_id(self, file_path: Path) -> str:
        """Generate unique file ID"""
        content = file_path.read_bytes()[:10000]  # First 10KB for speed
        timestamp = str(datetime.now().timestamp())
        hash_input = content + timestamp.encode()
        return hashlib.sha256(hash_input).hexdigest()
    
    def _extract_video_info(self, file_path: Path) -> Dict:
        """Extract video file information using ffprobe"""
        if not self.ffmpeg_available:
            return {
                "duration": 0.0,
                "resolution": "unknown",
                "width": 0,
                "height": 0,
                "fps": 0.0,
                "video_codec": "unknown",
                "audio_codec": "unknown",
                "bitrate": "unknown",
                "has_audio": False
            }
        
        try:
            import subprocess
            import json
            
            # Use ffprobe to extract metadata
            cmd = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                str(file_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                
                # Extract video stream info
                video_stream = next(
                    (s for s in data.get("streams", []) if s.get("codec_type") == "video"),
                    {}
                )
                
                # Extract audio stream info
                audio_stream = next(
                    (s for s in data.get("streams", []) if s.get("codec_type") == "audio"),
                    {}
                )
                
                format_data = data.get("format", {})
                
                width = video_stream.get("width", 0)
                height = video_stream.get("height", 0)
                
                return {
                    "duration": float(format_data.get("duration", 0)),
                    "resolution": f"{width}x{height}",
                    "width": width,
                    "height": height,
                    "fps": eval(video_stream.get("r_frame_rate", "0/1")),
                    "video_codec": video_stream.get("codec_name", "unknown"),
                    "audio_codec": audio_stream.get("codec_name", "unknown"),
                    "bitrate": f"{int(format_data.get('bit_rate', 0)) // 1000}kbps",
                    "has_audio": bool(audio_stream)
                }
        
        except Exception as e:
            logger.error(f"Failed to extract video info: {e}")
            return {
                "duration": 0.0,
                "resolution": "unknown",
                "width": 0,
                "height": 0,
                "fps": 0.0,
                "video_codec": "unknown",
                "audio_codec": "unknown",
                "bitrate": "unknown",
                "has_audio": False
            }
    
    def _generate_thumbnail(self, video_path: Path, file_id: str) -> Optional[str]:
        """Generate thumbnail for video"""
        try:
            import subprocess
            
            # Create thumbnail directory
            thumb_dir = self.directories["thumbnails"]
            thumb_path = thumb_dir / f"{file_id}.jpg"
            
            # Generate thumbnail at 1 second
            cmd = [
                "ffmpeg",
                "-i", str(video_path),
                "-ss", "00:00:01",
                "-vframes", "1",
                "-vf", "scale=320:-1",
                "-y",
                str(thumb_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=30
            )
            
            if result.returncode == 0 and thumb_path.exists():
                relative_path = thumb_path.relative_to(self.base_dir)
                thumbnail_url = f"/video/{relative_path}"
                logger.info(f"✅ Thumbnail generated: {thumb_path.name}")
                return thumbnail_url
        
        except Exception as e:
            logger.error(f"Failed to generate thumbnail: {e}")
        
        return None
    
    def get_video(self, file_id: str) -> Optional[VideoFile]:
        """Get video file by ID"""
        video = self.metadata.get(file_id)
        if video:
            # Update access stats
            video.last_accessed = datetime.now().isoformat()
            video.access_count += 1
            self._save_metadata()
        return video
    
    def list_videos(
        self,
        project_type: Optional[str] = None,
        user_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100
    ) -> List[VideoFile]:
        """List video files with filters"""
        results = []
        
        for video in self.metadata.values():
            # Apply filters
            if project_type and video.project_type != project_type:
                continue
            if user_id and video.created_by != user_id:
                continue
            if tags and not any(tag in video.tags for tag in tags):
                continue
            
            results.append(video)
            
            if len(results) >= limit:
                break
        
        # Sort by creation date (newest first)
        results.sort(key=lambda x: x.created_at, reverse=True)
        
        return results
    
    def delete_video(self, file_id: str) -> bool:
        """Delete video file and associated files (thumbnail, preview)"""
        video = self.metadata.get(file_id)
        if not video:
            return False
        
        try:
            # Delete video file
            file_path = Path(video.file_path)
            if file_path.exists():
                file_path.unlink()
            
            # Delete thumbnail
            if video.thumbnail_url:
                thumb_path = self.base_dir / video.thumbnail_url.replace("/video/", "")
                if thumb_path.exists():
                    thumb_path.unlink()
            
            # Delete preview
            if video.preview_url:
                preview_path = self.base_dir / video.preview_url.replace("/video/", "")
                if preview_path.exists():
                    preview_path.unlink()
            
            # Remove from metadata
            del self.metadata[file_id]
            self._save_metadata()
            
            logger.info(f"✅ Video deleted: {video.filename}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to delete video: {e}")
            return False
    
    def get_storage_stats(self) -> Dict:
        """Get storage statistics"""
        stats = {
            "total_videos": len(self.metadata),
            "total_size_mb": sum(v.size_mb for v in self.metadata.values()),
            "total_duration_seconds": sum(v.duration_seconds for v in self.metadata.values()),
            "by_type": {},
            "by_resolution": {},
            "by_user": {},
            "most_accessed": []
        }
        
        # Count by type
        for video in self.metadata.values():
            type_count = stats["by_type"].get(video.project_type, 0)
            stats["by_type"][video.project_type] = type_count + 1
            
            res_count = stats["by_resolution"].get(video.resolution, 0)
            stats["by_resolution"][video.resolution] = res_count + 1
            
            if video.created_by:
                user_count = stats["by_user"].get(video.created_by, 0)
                stats["by_user"][video.created_by] = user_count + 1
        
        # Most accessed
        sorted_videos = sorted(
            self.metadata.values(),
            key=lambda x: x.access_count,
            reverse=True
        )
        stats["most_accessed"] = [
            {
                "id": v.id,
                "filename": v.filename,
                "access_count": v.access_count
            }
            for v in sorted_videos[:10]
        ]
        
        # Format duration
        total_hours = stats["total_duration_seconds"] / 3600
        stats["total_duration_formatted"] = f"{total_hours:.2f} hours"
        
        return stats
    
    def cleanup_temp_files(self, older_than_hours: int = 24):
        """Clean up temporary files older than X hours"""
        temp_dir = self.directories["temp"]
        cache_dir = self.directories["cache"]
        
        import time
        cutoff_time = time.time() - (older_than_hours * 3600)
        deleted_count = 0
        
        for directory in [temp_dir, cache_dir]:
            for file_path in directory.glob("**/*"):
                if file_path.is_file():
                    if file_path.stat().st_mtime < cutoff_time:
                        try:
                            file_path.unlink()
                            deleted_count += 1
                        except Exception as e:
                            logger.error(f"Failed to delete {file_path}: {e}")
        
        logger.info(f"🧹 Cleaned up {deleted_count} temp video files")
        return deleted_count


# Global video manager instance
video_manager = VideoManager()


if __name__ == "__main__":
    print("🧪 Testing Video Manager\n")
    
    manager = VideoManager()
    
    # Test storage
    print(f"Storage directories:")
    for name, path in manager.directories.items():
        print(f"  {name}: {path}")
    
    # Test stats
    stats = manager.get_storage_stats()
    print(f"\nStorage stats:")
    print(f"  Total videos: {stats['total_videos']}")
    print(f"  Total size: {stats['total_size_mb']}MB")
    print(f"  Total duration: {stats['total_duration_formatted']}")
    print(f"  ffmpeg available: {manager.ffmpeg_available}")
    
    print("\n✅ Video Manager ready!")

