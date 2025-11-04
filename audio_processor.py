#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎚️ Audio Processing and Quality Enhancement
Pwosesis ak Amelyorasyon Kalite Odyo

Features:
- Normalize volume
- Remove silence
- Convert formats
- Adjust bitrate
- Add fade in/out
- Compress audio
"""

from pathlib import Path
from typing import Optional, Literal
import logging

logger = logging.getLogger('FanerStudio.AudioProcessor')


class AudioProcessor:
    """
    Professional audio processing
    Pwosesis pwofesyonèl pou odyo
    """
    
    def __init__(self):
        try:
            from pydub import AudioSegment
            from pydub.effects import normalize, compress_dynamic_range
            self.pydub_available = True
        except ImportError:
            logger.warning("pydub not available, audio processing limited")
            self.pydub_available = False
    
    def normalize_audio(
        self,
        input_path: Path,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Normalize audio volume
        Nòmalize volim odyo
        """
        if not self.pydub_available:
            raise RuntimeError("pydub required for audio processing")
        
        from pydub import AudioSegment
        from pydub.effects import normalize
        
        output_path = output_path or input_path.parent / f"{input_path.stem}_normalized{input_path.suffix}"
        
        logger.info(f"Normalizing: {input_path.name}")
        
        audio = AudioSegment.from_file(str(input_path))
        normalized = normalize(audio)
        normalized.export(str(output_path), format=input_path.suffix[1:])
        
        logger.info(f"✅ Saved: {output_path}")
        return output_path
    
    def remove_silence(
        self,
        input_path: Path,
        output_path: Optional[Path] = None,
        silence_thresh: int = -40,
        min_silence_len: int = 500
    ) -> Path:
        """
        Remove silence from audio
        Retire silans nan odyo
        """
        if not self.pydub_available:
            raise RuntimeError("pydub required")
        
        from pydub import AudioSegment
        from pydub.silence import detect_nonsilent
        
        output_path = output_path or input_path.parent / f"{input_path.stem}_no_silence{input_path.suffix}"
        
        logger.info(f"Removing silence: {input_path.name}")
        
        audio = AudioSegment.from_file(str(input_path))
        
        # Detect non-silent parts
        nonsilent_ranges = detect_nonsilent(
            audio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh
        )
        
        # Combine non-silent parts
        if nonsilent_ranges:
            output = AudioSegment.empty()
            for start, end in nonsilent_ranges:
                output += audio[start:end]
            
            output.export(str(output_path), format=input_path.suffix[1:])
            
            original_duration = len(audio) / 1000
            new_duration = len(output) / 1000
            saved = original_duration - new_duration
            
            logger.info(f"✅ Removed {saved:.1f}s of silence")
        else:
            # No silence detected, copy original
            import shutil
            shutil.copy2(input_path, output_path)
        
        return output_path
    
    def convert_format(
        self,
        input_path: Path,
        output_format: Literal["mp3", "wav", "ogg", "flac"],
        bitrate: str = "192k"
    ) -> Path:
        """
        Convert audio format
        Konvèti fòma odyo
        """
        if not self.pydub_available:
            raise RuntimeError("pydub required")
        
        from pydub import AudioSegment
        
        output_path = input_path.parent / f"{input_path.stem}.{output_format}"
        
        logger.info(f"Converting to {output_format}: {input_path.name}")
        
        audio = AudioSegment.from_file(str(input_path))
        
        audio.export(
            str(output_path),
            format=output_format,
            bitrate=bitrate
        )
        
        logger.info(f"✅ Converted: {output_path}")
        return output_path
    
    def add_fade(
        self,
        input_path: Path,
        output_path: Optional[Path] = None,
        fade_in_ms: int = 1000,
        fade_out_ms: int = 2000
    ) -> Path:
        """
        Add fade in/out
        Ajoute fade in/out
        """
        if not self.pydub_available:
            raise RuntimeError("pydub required")
        
        from pydub import AudioSegment
        
        output_path = output_path or input_path.parent / f"{input_path.stem}_faded{input_path.suffix}"
        
        audio = AudioSegment.from_file(str(input_path))
        faded = audio.fade_in(fade_in_ms).fade_out(fade_out_ms)
        faded.export(str(output_path), format=input_path.suffix[1:])
        
        logger.info(f"✅ Added fade: {output_path}")
        return output_path
    
    def optimize_for_web(
        self,
        input_path: Path,
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Optimize audio for web streaming
        Optimize pou streaming sou wèb
        """
        if not self.pydub_available:
            raise RuntimeError("pydub required")
        
        from pydub import AudioSegment
        from pydub.effects import normalize
        
        output_path = output_path or input_path.parent / f"{input_path.stem}_web.mp3"
        
        logger.info(f"Optimizing for web: {input_path.name}")
        
        audio = AudioSegment.from_file(str(input_path))
        
        # Normalize
        audio = normalize(audio)
        
        # Convert to mono if stereo (reduces size)
        if audio.channels > 1:
            audio = audio.set_channels(1)
        
        # Set to 44.1kHz (standard)
        audio = audio.set_frame_rate(44100)
        
        # Export with web-friendly bitrate
        audio.export(
            str(output_path),
            format="mp3",
            bitrate="128k",
            parameters=["-ar", "44100"]
        )
        
        original_size = input_path.stat().st_size / (1024 * 1024)
        new_size = output_path.stat().st_size / (1024 * 1024)
        
        logger.info(f"✅ Optimized: {original_size:.2f}MB → {new_size:.2f}MB")
        return output_path


# Global processor instance
audio_processor = AudioProcessor()

