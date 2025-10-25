"""
Simple translation wrapper
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.translator import CreoleTranslator
from src.config import Config


def translate_text(text: str, target_lang: str = "ht") -> str:
    """
    Tradui tèks / Translate text
    
    Args:
        text: Text to translate
        target_lang: Target language code (default: "ht" for Haitian Creole)
    
    Returns:
        Translated text
    """
    # Create config with target language
    config = Config()
    config.target_language = target_lang
    
    translator = CreoleTranslator(config)
    
    # Translate text
    translated = translator.translate(text, show_progress=True)
    return translated

