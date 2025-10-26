"""
Simple audio generation wrapper
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.audio_generator import AudiobookGenerator
from src.config import Config


def generate_audio(text: str, output_path: str, language: str = "ht") -> str:
    """
    Jenere liv odyo / Generate audiobook
    
    Args:
        text: Text to convert to speech
        output_path: Output MP3 file path
        language: Language for TTS (default: "ht" for Haitian Creole)
    
    Returns:
        Path to generated audio file
    """
    # Create config
    config = Config()
    config.tts_language = language
    
    generator = AudiobookGenerator(config)
    
    # Generate audio
    audio_path = generator.generate(text, output_path=Path(output_path))
    return str(audio_path)

