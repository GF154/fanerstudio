#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎵 Professional Audio Management System
Sistèm Pwofesyonèl pou Jere Odyo

Features:
- Organized file storage
- Metadata tracking
- Quality optimization
- Format conversion
- CDN integration ready
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging
from dataclasses import dataclass, asdict
import mimetypes

logger = logging.getLogger('FanerStudio.AudioManager')


@dataclass
class AudioFile:
    """Metadata for audio file"""
    id: str
    filename: str
    original_filename: str
    file_path: str
    url: str
    format: str
    size_bytes: int
    size_mb: float
    duration_seconds: float
    bitrate: str
    sample_rate: int
    channels: int
    created_by: Optional[str]
    project_id: Optional[str]
    project_type: str  # audiobook, podcast, tts, custom_voice
    tags: List[str]
    is_public: bool
    created_at: str
    last_accessed: Optional[str]
    access_count: int
    
    def to_dict(self) -> dict:
        return asdict(self)


class AudioManager:
    """
    Manage all audio files professionally
    Jere tout fichye odyo pwofesyonèlman
    """
    
    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path("audio_storage")
        
        # Create organized directory structure
        self.directories = {
            "audiobooks": self.base_dir / "audiobooks",
            "podcasts": self.base_dir / "podcasts",
            "tts": self.base_dir / "tts",
            "voices": self.base_dir / "custom_voices",
            "temp": self.base_dir / "temp",
            "cache": self.base_dir / "cache"
        }
        
        # Create all directories
        for directory in self.directories.values():
            directory.mkdir(parents=True, exist_ok=True)
        
        # Metadata storage
        self.metadata_file = self.base_dir / "audio_metadata.json"
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, AudioFile]:
        """Load metadata from file"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        k: AudioFile(**v) for k, v in data.items()
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
    
    def store_audio(
        self,
        audio_path: Path,
        project_type: str,
        user_id: Optional[str] = None,
        project_id: Optional[str] = None,
        tags: List[str] = None,
        is_public: bool = False
    ) -> AudioFile:
        """
        Store audio file with metadata
        
        Args:
            audio_path: Path to audio file
            project_type: Type (audiobook, podcast, tts, custom_voice)
            user_id: User who created it
            project_id: Associated project ID
            tags: Tags for searching
            is_public: Whether file is publicly accessible
        
        Returns:
            AudioFile metadata object
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Generate unique ID
        file_id = self._generate_file_id(audio_path)
        
        # Determine storage directory
        storage_dir = self.directories.get(f"{project_type}s", self.directories["temp"])
        
        # Create user subdirectory if user_id provided
        if user_id:
            storage_dir = storage_dir / user_id
            storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_ext = audio_path.suffix
        new_filename = f"{project_type}_{timestamp}_{file_id[:8]}{file_ext}"
        
        # Copy file to storage
        destination = storage_dir / new_filename
        import shutil
        shutil.copy2(audio_path, destination)
        
        # Extract audio metadata
        audio_info = self._extract_audio_info(destination)
        
        # Generate URL (relative to API)
        relative_path = destination.relative_to(self.base_dir)
        url = f"/audio/{relative_path}"
        
        # Create metadata object
        audio_file = AudioFile(
            id=file_id,
            filename=new_filename,
            original_filename=audio_path.name,
            file_path=str(destination),
            url=url,
            format=file_ext[1:],  # Remove dot
            size_bytes=destination.stat().st_size,
            size_mb=round(destination.stat().st_size / (1024 * 1024), 2),
            duration_seconds=audio_info.get("duration", 0.0),
            bitrate=audio_info.get("bitrate", "unknown"),
            sample_rate=audio_info.get("sample_rate", 44100),
            channels=audio_info.get("channels", 2),
            created_by=user_id,
            project_id=project_id,
            project_type=project_type,
            tags=tags or [],
            is_public=is_public,
            created_at=datetime.now().isoformat(),
            last_accessed=None,
            access_count=0
        )
        
        # Store metadata
        self.metadata[file_id] = audio_file
        self._save_metadata()
        
        logger.info(f"✅ Audio stored: {new_filename} ({audio_file.size_mb}MB)")
        
        return audio_file
    
    def _generate_file_id(self, file_path: Path) -> str:
        """Generate unique file ID"""
        content = file_path.read_bytes()
        timestamp = str(datetime.now().timestamp())
        hash_input = content + timestamp.encode()
        return hashlib.sha256(hash_input).hexdigest()
    
    def _extract_audio_info(self, file_path: Path) -> Dict:
        """Extract audio file information"""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(str(file_path))
            
            return {
                "duration": len(audio) / 1000.0,  # Convert to seconds
                "bitrate": f"{audio.frame_rate}kbps",
                "sample_rate": audio.frame_rate,
                "channels": audio.channels
            }
        except Exception as e:
            logger.warning(f"Could not extract audio info: {e}")
            return {
                "duration": 0.0,
                "bitrate": "unknown",
                "sample_rate": 44100,
                "channels": 2
            }
    
    def get_audio(self, file_id: str) -> Optional[AudioFile]:
        """Get audio file by ID"""
        audio = self.metadata.get(file_id)
        if audio:
            # Update access stats
            audio.last_accessed = datetime.now().isoformat()
            audio.access_count += 1
            self._save_metadata()
        return audio
    
    def list_audios(
        self,
        project_type: Optional[str] = None,
        user_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100
    ) -> List[AudioFile]:
        """List audio files with filters"""
        results = []
        
        for audio in self.metadata.values():
            # Apply filters
            if project_type and audio.project_type != project_type:
                continue
            if user_id and audio.created_by != user_id:
                continue
            if tags and not any(tag in audio.tags for tag in tags):
                continue
            
            results.append(audio)
            
            if len(results) >= limit:
                break
        
        # Sort by creation date (newest first)
        results.sort(key=lambda x: x.created_at, reverse=True)
        
        return results
    
    def delete_audio(self, file_id: str) -> bool:
        """Delete audio file"""
        audio = self.metadata.get(file_id)
        if not audio:
            return False
        
        try:
            # Delete physical file
            file_path = Path(audio.file_path)
            if file_path.exists():
                file_path.unlink()
            
            # Remove from metadata
            del self.metadata[file_id]
            self._save_metadata()
            
            logger.info(f"✅ Audio deleted: {audio.filename}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to delete audio: {e}")
            return False
    
    def get_storage_stats(self) -> Dict:
        """Get storage statistics"""
        stats = {
            "total_files": len(self.metadata),
            "total_size_mb": sum(a.size_mb for a in self.metadata.values()),
            "by_type": {},
            "by_user": {},
            "most_accessed": []
        }
        
        # Count by type
        for audio in self.metadata.values():
            type_count = stats["by_type"].get(audio.project_type, 0)
            stats["by_type"][audio.project_type] = type_count + 1
            
            if audio.created_by:
                user_count = stats["by_user"].get(audio.created_by, 0)
                stats["by_user"][audio.created_by] = user_count + 1
        
        # Most accessed
        sorted_audios = sorted(
            self.metadata.values(),
            key=lambda x: x.access_count,
            reverse=True
        )
        stats["most_accessed"] = [
            {
                "id": a.id,
                "filename": a.filename,
                "access_count": a.access_count
            }
            for a in sorted_audios[:10]
        ]
        
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
        
        logger.info(f"🧹 Cleaned up {deleted_count} temp files")
        return deleted_count


# Global audio manager instance
audio_manager = AudioManager()


if __name__ == "__main__":
    print("🧪 Testing Audio Manager\n")
    
    manager = AudioManager()
    
    # Test storage
    print(f"Storage directories:")
    for name, path in manager.directories.items():
        print(f"  {name}: {path}")
    
    # Test stats
    stats = manager.get_storage_stats()
    print(f"\nStorage stats:")
    print(f"  Total files: {stats['total_files']}")
    print(f"  Total size: {stats['total_size_mb']}MB")
    
    print("\n✅ Audio Manager ready!")

