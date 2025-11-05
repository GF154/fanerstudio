#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎙️ Faner Studio - Voice B Configuration
Gason Naratè - Optimal pou Liv Odyo & Podcast
"""

# ============================================================
# VOICE B - GASON NARATÈ CONFIGURATION
# ============================================================

VOICE_B_CONFIG = {
    "name": "Gason Naratè",
    "code": "B",
    "gender": "Male",
    "style": "Professional Narrator",
    "best_for": ["Liv Odyo", "Podcast", "Naratif", "Edikasyon"],
    
    # Engine-specific settings
    "engines": {
        "coqui": {
            "model": "tts_models/multilingual/multi-dataset/your_tts",
            "language": "fr",  # French for Haitian Creole
            "speaker": None,   # Will use default French male voice
            "speed": 0.95,     # Slightly slower for clarity
        },
        "edge": {
            "voice": "fr-FR-HenriNeural",  # Male French voice
            "rate": "-5%",     # Slightly slower
            "pitch": "-2Hz",   # Slightly lower/deeper
            "volume": "+0%",   # Normal volume
        },
        "gtts": {
            "lang": "fr",
            "slow": False,
            "tld": "fr",  # French accent
        }
    },
    
    # Audiobook-specific settings
    "audiobook": {
        "speed": 0.95,           # 95% speed for clarity
        "pitch": -2,             # Deeper voice
        "pause_sentence": 0.5,   # 500ms pause after sentences
        "pause_paragraph": 1.0,  # 1 second pause after paragraphs
        "volume": 100,           # Normal volume
    },
    
    # Podcast-specific settings
    "podcast": {
        "speed": 1.0,            # Normal speed for conversation
        "pitch": 0,              # Natural pitch
        "energy": "moderate",    # Not too flat, not too energetic
        "pause_sentence": 0.3,   # Shorter pauses for conversation
        "pause_paragraph": 0.7,
        "volume": 105,           # Slightly louder
    },
    
    # Text processing rules for Creole
    "text_processing": {
        "abbreviations": {
            "M.": "Mesye",
            "Mme": "Madanm",
            "Dr.": "Doktè",
            "Sr.": "Sè",
            "Fr.": "Frè",
        },
        "emphasis_words": [
            "trè", "anpil", "vrèman", "absoliman", "totalman"
        ],
        "pause_markers": ["...", "—", ":", ";"],
    },
    
    # Quality settings
    "quality": {
        "sample_rate": 22050,    # CD quality
        "bit_depth": 16,
        "channels": 1,           # Mono for narration
        "format": "wav",         # Best quality
        "compression": "none",   # No compression for master
    },
    
    # Performance optimization
    "performance": {
        "chunk_size": 500,       # Words per chunk
        "max_text_length": 5000, # Characters per request
        "cache_enabled": True,
        "async_processing": True,
    }
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_voice_b_config(engine: str = "coqui", use_case: str = "audiobook"):
    """
    Get Voice B configuration for specific engine and use case
    
    Args:
        engine: TTS engine (coqui, edge, gtts)
        use_case: audiobook or podcast
        
    Returns:
        Configuration dict
    """
    config = VOICE_B_CONFIG.copy()
    
    # Merge engine-specific settings
    if engine in config["engines"]:
        config.update(config["engines"][engine])
    
    # Merge use case settings
    if use_case in ["audiobook", "podcast"]:
        config["settings"] = config[use_case]
    
    return config


def apply_voice_b_processing(text: str):
    """
    Apply Voice B specific text processing
    
    Args:
        text: Input text
        
    Returns:
        Processed text
    """
    # Replace abbreviations
    for abbr, full in VOICE_B_CONFIG["text_processing"]["abbreviations"].items():
        text = text.replace(abbr, full)
    
    # Add pauses for emphasis
    for word in VOICE_B_CONFIG["text_processing"]["emphasis_words"]:
        # Add slight pause before emphasis words
        text = text.replace(f" {word} ", f" ... {word} ... ")
    
    return text


def get_optimal_settings(text_length: int, use_case: str = "audiobook"):
    """
    Get optimal Voice B settings based on text length
    
    Args:
        text_length: Length of text in characters
        use_case: audiobook or podcast
        
    Returns:
        Optimized settings dict
    """
    config = VOICE_B_CONFIG[use_case].copy()
    
    # Adjust speed based on text length
    if text_length > 10000:  # Very long text
        config["speed"] = 0.9  # Slower for endurance
    elif text_length > 5000:  # Long text
        config["speed"] = 0.95  # Slightly slower
    else:  # Short text
        config["speed"] = 1.0  # Normal speed
    
    return config


# ============================================================
# EXAMPLE USAGE
# ============================================================

if __name__ == "__main__":
    print("🎙️ Voice B - Gason Naratè Configuration")
    print("=" * 60)
    
    # Show config
    print(f"Name: {VOICE_B_CONFIG['name']}")
    print(f"Code: {VOICE_B_CONFIG['code']}")
    print(f"Gender: {VOICE_B_CONFIG['gender']}")
    print(f"Style: {VOICE_B_CONFIG['style']}")
    print(f"Best for: {', '.join(VOICE_B_CONFIG['best_for'])}")
    
    print("\n📊 Engine Settings:")
    for engine, settings in VOICE_B_CONFIG["engines"].items():
        print(f"\n  {engine.upper()}:")
        for key, value in settings.items():
            print(f"    - {key}: {value}")
    
    print("\n📚 Audiobook Settings:")
    for key, value in VOICE_B_CONFIG["audiobook"].items():
        print(f"  - {key}: {value}")
    
    print("\n🎙️ Podcast Settings:")
    for key, value in VOICE_B_CONFIG["podcast"].items():
        print(f"  - {key}: {value}")
    
    print("\n" + "=" * 60)
    print("✅ Configuration ready!")
    
    # Test text processing
    test_text = "M. Jean di: 'Sa trè enpòtan pou nou konprann...'"
    processed = apply_voice_b_processing(test_text)
    print(f"\n🧪 Test Text Processing:")
    print(f"Input:  {test_text}")
    print(f"Output: {processed}")

