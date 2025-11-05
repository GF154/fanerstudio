#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎙️ Faner Studio - PRODUCTION VOICE CONFIGURATION
Voice B + Style 2 - Optimal for Haitian Creole Content
Vwa B + Stil 2 - Optimal pou Kontni Kreyòl Ayisyen
"""

# ============================================================
# FINAL PRODUCTION CONFIGURATION
# Voice: B - Gason Naratè Pwofesyonèl
# Style: 2 - Natirèl, konvèsasyon, balanse
# ============================================================

PRODUCTION_VOICE = {
    # Identity
    "code": "B2",
    "name": "Gason Naratè Natirèl",
    "description": "Professional male narrator with natural, conversational style",
    "language": "Haitian Creole (via French)",
    
    # Classification
    "gender": "male",
    "style": "natural_conversational",
    "age_range": "30-45",
    "tone": "balanced",
    
    # Optimal Use Cases
    "best_for": {
        "audiobook": True,
        "podcast": True,
        "narration": True,
        "education": True,
        "documentation": True
    },
    
    # Primary Engine: Coqui TTS
    "coqui": {
        "model": "tts_models/multilingual/multi-dataset/your_tts",
        "language": "fr",  # French for Haitian Creole
        "speaker_idx": None,  # Default male speaker
        
        # Style 2 - Natural Conversational
        "speed": 1.0,         # Normal speed (not slow, not fast)
        "emotion": "neutral", # Balanced, not dramatic
        "energy": 0.5,        # Medium energy (50%)
        
        # Quality
        "sample_rate": 22050,
        "format": "wav",
    },
    
    # Backup Engine: Edge TTS
    "edge": {
        "voice": "fr-FR-HenriNeural",  # Male French voice
        "rate": "+0%",        # Normal speed
        "pitch": "+0Hz",      # Natural pitch
        "volume": "+0%",      # Normal volume
        "style": "newscast",  # Professional but conversational
    },
    
    # Backup Engine: gTTS
    "gtts": {
        "lang": "fr",
        "slow": False,        # Normal speed
        "tld": "fr",
    },
    
    # Audiobook Settings (Style 2 applied)
    "audiobook": {
        "speed": 1.0,              # Natural conversational speed
        "pitch": 0,                # Natural pitch (not deeper)
        "pause_sentence": 0.4,     # Natural pause
        "pause_paragraph": 0.8,    # Comfortable pause
        "pause_chapter": 2.0,      # Clear chapter break
        "volume": 100,             # Normal
        "emphasis": "moderate",    # Not too dramatic
    },
    
    # Podcast Settings (Style 2 applied)
    "podcast": {
        "speed": 1.05,             # Slightly faster for conversation
        "pitch": 0,                # Natural pitch
        "pause_sentence": 0.3,     # Quick, conversational
        "pause_paragraph": 0.6,    # Brief pause
        "pause_topic": 1.5,        # Topic transition
        "volume": 105,             # Slightly louder
        "emphasis": "natural",     # Conversational emphasis
        "variation": True,         # Vary intonation
    },
    
    # Text Processing
    "text_processing": {
        # Abbreviations
        "abbreviations": {
            "M.": "Mesye",
            "Mme": "Madanm",
            "Mwen": "Mwen",
            "Dr.": "Doktè",
            "pwof.": "pwofesè",
        },
        
        # Natural pauses (Style 2)
        "natural_pauses": {
            ",": 0.2,      # Comma - brief pause
            ";": 0.3,      # Semicolon
            ":": 0.3,      # Colon
            ".": 0.4,      # Period - natural pause
            "?": 0.5,      # Question - emphasize
            "!": 0.5,      # Exclamation - emphasize
            "...": 0.6,    # Ellipsis - thoughtful pause
            "—": 0.4,      # Em dash
        },
        
        # Emphasis (Natural, not exaggerated)
        "emphasis_words": {
            "trè": "slight",
            "anpil": "slight",
            "vrèman": "moderate",
            "absoliman": "moderate",
        },
        
        # Sentence variety (for natural flow)
        "intonation": {
            "statement": "falling",
            "question": "rising",
            "exclamation": "moderate_rise",
            "continuation": "level",
        }
    },
    
    # Quality Settings
    "quality": {
        "sample_rate": 22050,    # CD quality
        "bit_depth": 16,
        "channels": 1,           # Mono for voice
        "format": "wav",         # Lossless master
        "export_formats": ["mp3", "m4a", "opus"],  # Distribution formats
        "mp3_bitrate": "192k",   # High quality MP3
    },
    
    # Performance
    "performance": {
        "chunk_size": 500,           # Words per chunk
        "max_text_length": 5000,     # Characters per request
        "overlap": 50,               # Character overlap between chunks
        "cache_enabled": True,
        "async_processing": True,
        "parallel_chunks": 3,        # Process 3 chunks in parallel
    },
    
    # Metadata
    "metadata": {
        "version": "1.0",
        "created": "2025-11-05",
        "optimized_for": "Haitian Creole content",
        "tested_with": "Audiobooks and Podcasts",
        "recommended": True,
    }
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_production_config(engine: str = "coqui", use_case: str = "audiobook"):
    """
    Get production-ready configuration
    
    Args:
        engine: TTS engine (coqui, edge, gtts)
        use_case: audiobook or podcast
        
    Returns:
        Complete configuration dict
    """
    config = PRODUCTION_VOICE.copy()
    
    # Select engine
    if engine in ["coqui", "edge", "gtts"]:
        config["engine_settings"] = config[engine]
    else:
        config["engine_settings"] = config["coqui"]  # Default
    
    # Select use case
    if use_case in ["audiobook", "podcast"]:
        config["use_case_settings"] = config[use_case]
    else:
        config["use_case_settings"] = config["audiobook"]  # Default
    
    return config


def apply_style_2_processing(text: str):
    """
    Apply Style 2 (Natural Conversational) text processing
    
    Args:
        text: Input text
        
    Returns:
        Processed text with natural pauses and emphasis
    """
    # Replace abbreviations
    for abbr, full in PRODUCTION_VOICE["text_processing"]["abbreviations"].items():
        text = text.replace(abbr, full)
    
    # Add natural pauses (not too many)
    # Style 2 is balanced - only slight emphasis
    emphasis_map = PRODUCTION_VOICE["text_processing"]["emphasis_words"]
    for word, level in emphasis_map.items():
        if level == "slight":
            # Very subtle pause
            text = text.replace(f" {word} ", f" {word} ")
        elif level == "moderate":
            # Moderate pause
            text = text.replace(f" {word} ", f" {word}, ")
    
    return text


def estimate_duration(text: str, use_case: str = "audiobook"):
    """
    Estimate audio duration for Style 2
    
    Args:
        text: Input text
        use_case: audiobook or podcast
        
    Returns:
        Estimated duration in seconds
    """
    # Words per minute for Style 2 (natural conversational)
    wpm = {
        "audiobook": 155,  # Comfortable listening speed
        "podcast": 165     # Slightly faster for conversation
    }
    
    words = len(text.split())
    minutes = words / wpm.get(use_case, 155)
    seconds = minutes * 60
    
    return seconds


def format_duration(seconds: float):
    """Format duration as HH:MM:SS"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


# ============================================================
# EXAMPLE USAGE
# ============================================================

if __name__ == "__main__":
    print("🎙️ PRODUCTION VOICE CONFIGURATION")
    print("=" * 70)
    print(f"Voice: {PRODUCTION_VOICE['code']} - {PRODUCTION_VOICE['name']}")
    print(f"Style: 2 - Natirèl, konvèsasyon, balanse")
    print(f"Language: {PRODUCTION_VOICE['language']}")
    print("=" * 70)
    
    # Show configuration
    print("\n📊 OPTIMAL USE CASES:")
    for use_case, optimal in PRODUCTION_VOICE["best_for"].items():
        status = "✅" if optimal else "❌"
        print(f"  {status} {use_case.capitalize()}")
    
    print("\n🎙️ COQUI TTS SETTINGS:")
    for key, value in PRODUCTION_VOICE["coqui"].items():
        print(f"  - {key}: {value}")
    
    print("\n📚 AUDIOBOOK SETTINGS (Style 2):")
    for key, value in PRODUCTION_VOICE["audiobook"].items():
        print(f"  - {key}: {value}")
    
    print("\n🎤 PODCAST SETTINGS (Style 2):")
    for key, value in PRODUCTION_VOICE["podcast"].items():
        print(f"  - {key}: {value}")
    
    print("\n" + "=" * 70)
    print("✅ CONFIGURATION READY FOR PRODUCTION!")
    print("=" * 70)
    
    # Test text processing
    test_text = """
    Bonjou tout moun! Mwen trè kontan pou m prezante liv sa a.
    Sa vrèman enpòtan pou nou konprann istwa Ayiti...
    Èske nou prè pou aprann plis?
    """
    
    processed = apply_style_2_processing(test_text.strip())
    duration = estimate_duration(test_text, "audiobook")
    
    print("\n🧪 TEST EXAMPLE:")
    print(f"\nOriginal Text ({len(test_text.split())} words):")
    print(test_text)
    print(f"\nProcessed (Style 2):")
    print(processed)
    print(f"\nEstimated Duration: {format_duration(duration)}")
    print(f"Speed: 155 words/minute (natural conversational)")

