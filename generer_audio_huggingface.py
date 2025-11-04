#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎤 Haitian Creole TTS Generator using Hugging Face Models
Jeneratè TTS Kreyòl Ayisyen ak modèl Hugging Face
"""

import os
import sys
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger('KreyolAI.TTS')

# Try multiple TTS approaches
TTS_METHOD = None

# Method 1: Try gTTS (simple, always works)
try:
    from gtts import gTTS
    TTS_METHOD = "gtts"
    logger.info("✅ Using gTTS for Haitian Creole")
except ImportError:
    pass

# Method 2: Try Coqui TTS (better quality)
if not TTS_METHOD:
    try:
        from TTS.api import TTS as CoquiTTS
        TTS_METHOD = "coqui"
        logger.info("✅ Using Coqui TTS for Haitian Creole")
    except ImportError:
        pass

# Method 3: Try pyttsx3 (offline fallback)
if not TTS_METHOD:
    try:
        import pyttsx3
        TTS_METHOD = "pyttsx3"
        logger.info("✅ Using pyttsx3 for Haitian Creole")
    except ImportError:
        pass


def generer_audio_creole(
    text: str,
    output_path: str | Path,
    voice: str = "default",
    lang: str = "ht"
) -> Path:
    """
    Generate Haitian Creole audio from text
    Jenere odyo Kreyòl Ayisyen soti nan tèks
    
    Args:
        text: Text to convert to speech
        output_path: Where to save the audio file
        voice: Voice to use (if available)
        lang: Language code (default: ht for Haitian Creole)
    
    Returns:
        Path to the generated audio file
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    try:
        if TTS_METHOD == "gtts":
            return _generate_with_gtts(text, output_path, lang)
        elif TTS_METHOD == "coqui":
            return _generate_with_coqui(text, output_path)
        elif TTS_METHOD == "pyttsx3":
            return _generate_with_pyttsx3(text, output_path)
        else:
            raise RuntimeError("No TTS engine available. Please install gtts: pip install gtts")
    
    except Exception as e:
        logger.error(f"TTS generation failed: {e}")
        raise


def _generate_with_gtts(text: str, output_path: Path, lang: str = "ht") -> Path:
    """Generate audio using Google Text-to-Speech with Creole optimization"""
    from gtts import gTTS
    
    # gTTS doesn't support 'ht' directly, use 'fr' (French) as closest
    # Haitian Creole shares many phonetic features with French
    tts_lang = "fr" if lang == "ht" else lang
    
    # Apply Creole pronunciation optimization
    if lang == "ht":
        try:
            from creole_pronunciation_dictionary import CreolePronunciationDictionary
            dict = CreolePronunciationDictionary()
            text = dict.process_text(text)
            logger.info("✅ Applied Creole pronunciation optimization")
        except Exception as e:
            logger.warning(f"Creole pronunciation optimization failed: {e}")
    
    logger.info(f"Generating audio with gTTS (lang={tts_lang})")
    tts = gTTS(text=text, lang=tts_lang, slow=False)
    tts.save(str(output_path))
    
    logger.info(f"✅ Audio generated: {output_path}")
    return output_path


def _generate_with_coqui(text: str, output_path: Path) -> Path:
    """Generate audio using Coqui TTS (better quality)"""
    from TTS.api import TTS as CoquiTTS
    
    # Use multilingual model
    logger.info("Generating audio with Coqui TTS")
    tts = CoquiTTS(model_name="tts_models/multilingual/multi-dataset/your_tts")
    
    tts.tts_to_file(
        text=text,
        file_path=str(output_path),
        language="fr"  # Use French for Haitian Creole
    )
    
    logger.info(f"✅ Audio generated: {output_path}")
    return output_path


def _generate_with_pyttsx3(text: str, output_path: Path) -> Path:
    """Generate audio using pyttsx3 (offline)"""
    import pyttsx3
    
    logger.info("Generating audio with pyttsx3")
    engine = pyttsx3.init()
    
    # Set properties for better quality
    engine.setProperty('rate', 150)  # Speed
    engine.setProperty('volume', 1.0)  # Volume
    
    # Try to find French voice
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'french' in voice.name.lower() or 'fr' in voice.id.lower():
            engine.setProperty('voice', voice.id)
            break
    
    engine.save_to_file(text, str(output_path))
    engine.runAndWait()
    
    logger.info(f"✅ Audio generated: {output_path}")
    return output_path


def check_tts_available() -> dict:
    """
    Check which TTS engines are available
    Tcheke ki motè TTS ki disponib
    
    Returns:
        Dictionary with available engines
    """
    engines = {
        "gtts": False,
        "coqui": False,
        "pyttsx3": False,
        "current": TTS_METHOD
    }
    
    try:
        import gtts
        engines["gtts"] = True
    except ImportError:
        pass
    
    try:
        from TTS.api import TTS
        engines["coqui"] = True
    except ImportError:
        pass
    
    try:
        import pyttsx3
        engines["pyttsx3"] = True
    except ImportError:
        pass
    
    return engines


def get_supported_languages() -> list:
    """Get list of supported languages for current TTS engine"""
    if TTS_METHOD == "gtts":
        from gtts.lang import tts_langs
        return list(tts_langs().keys())
    elif TTS_METHOD == "coqui":
        return ["en", "es", "fr", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh-cn", "ja", "hu", "ko"]
    elif TTS_METHOD == "pyttsx3":
        return ["en", "fr", "es", "de"]
    else:
        return []


# Simple test function
def test_tts():
    """Test TTS generation"""
    print("🧪 Testing TTS generation...")
    print(f"📊 Available engines: {check_tts_available()}")
    
    test_text = "Bonjou! Kòman ou ye? Mwen se yon sistèm TTS pou Kreyòl Ayisyen."
    test_output = Path("test_output.mp3")
    
    try:
        result = generer_audio_creole(test_text, test_output)
        print(f"✅ Test successful! Audio saved to: {result}")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    # Run test
    test_tts()

