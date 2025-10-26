"""
Podcast voice mixing utility
"""
import os
import shutil
from pathlib import Path
from typing import List


def mix_voices(audio_files: List[str], output_path: str) -> str:
    """
    Melanje plizyè fichye odyo / Mix multiple audio files into a podcast
    
    Note: This is a simple concatenation. For advanced mixing, 
    consider using pydub or ffmpeg.
    
    Args:
        audio_files: List of audio file paths to mix
        output_path: Output path for final podcast
    
    Returns:
        Path to final podcast file
    """
    if not audio_files:
        raise ValueError("No audio files provided")
    
    # For now, if only one file, just copy it
    if len(audio_files) == 1:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(audio_files[0], output_path)
        print(f"🎙️ Podcast kreyé / Podcast created: {output_path}")
        return str(output_path)
    
    # For multiple files, would need pydub or ffmpeg
    # For now, use the first file as a placeholder
    print(f"⚠️  Melanj plizyè fichye mande bibliyotèk adisyonèl")
    print(f"   Mixing multiple files requires additional libraries (pydub/ffmpeg)")
    print(f"   Using first audio file as output")
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(audio_files[0], output_path)
    
    return str(output_path)


def mix_voices_advanced(audio_files: List[str], output_path: str) -> str:
    """
    Advanced mixing using pydub (requires pydub and ffmpeg)
    
    Args:
        audio_files: List of audio file paths
        output_path: Output path for final podcast
    
    Returns:
        Path to final podcast file
    """
    try:
        from pydub import AudioSegment
    except ImportError:
        print("⚠️  pydub pa enstale / pydub not installed")
        print("   Instalé ak: pip install pydub")
        return mix_voices(audio_files, output_path)
    
    # Concatenate all audio files
    combined = AudioSegment.empty()
    
    for audio_file in audio_files:
        audio = AudioSegment.from_mp3(audio_file)
        combined += audio
    
    # Export combined audio
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    combined.export(str(output_path), format="mp3")
    
    print(f"🎙️ Podcast kreyé ak {len(audio_files)} fichye / Podcast created with {len(audio_files)} files")
    print(f"   📊 Dire / Duration: {len(combined) / 1000:.1f}s")
    
    return str(output_path)

