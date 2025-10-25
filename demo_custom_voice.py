#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script to showcase custom voice features
Script de démonstration des voix personnalisées
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.custom_voice_manager import CustomVoiceManager


def print_banner():
    """Print demo banner"""
    print("\n" + "="*70)
    print("🎙️  DEMO VWA PERSONALIZE / CUSTOM VOICE DEMO")
    print("   Plateforme Kreyòl IA")
    print("="*70 + "\n")


def demo_features():
    """Demonstrate custom voice features"""
    print_banner()
    
    # Initialize manager
    print("📦 Initialization / Inisyalizasyon")
    print("-" * 70)
    manager = CustomVoiceManager()
    print(f"✅ Voice manager initialized")
    print(f"   Voices directory: {manager.voices_dir.absolute()}")
    print(f"   Total voices: {len(manager.voices)}\n")
    
    # Show statistics
    print("📊 Statistics / Estatistik")
    print("-" * 70)
    stats = manager.get_statistics()
    
    if stats['total_voices'] == 0:
        print("Pa gen vwa ankò / No voices yet")
        print("\nPou ajoute vwa / To add voices:")
        print("  python add_custom_voice.py")
        print("\n")
        return
    
    print(f"Total voices: {stats['total_voices']}")
    print(f"Total duration: {stats['total_duration_minutes']:.1f} minutes")
    print(f"Total size: {stats['total_size_mb']:.1f} MB")
    print(f"Average rating: {stats['average_rating']:.1f} ⭐")
    print(f"Most used: {stats['most_used']}")
    print(f"Highest rated: {stats['highest_rated']}\n")
    
    # List all voices
    print("📚 All Voices / Tout Vwa")
    print("-" * 70)
    voices = manager.list_voices()
    
    for i, voice in enumerate(voices, 1):
        print(f"\n{i}. {voice['voice_name']}")
        print(f"   Speaker: {voice['speaker_name']}")
        print(f"   Language: {voice['language']}")
        print(f"   Gender: {voice['gender']}")
        print(f"   Region: {voice['region']}")
        print(f"   Rating: {'⭐' * int(voice['rating'])} ({voice['rating']:.1f})")
        print(f"   Used: {voice['times_used']} times")
        print(f"   Duration: {voice['duration_seconds']:.1f}s")
        print(f"   File: {voice['audio_file']}")
        print(f"   Text: {voice['text_content'][:100]}...")
    
    print("\n")
    
    # Demonstrate search
    print("🔍 Search Demo / Rechèch Demo")
    print("-" * 70)
    query = "bonjou"
    results = manager.search_voices(query)
    print(f"Search for '{query}': {len(results)} results")
    for result in results:
        print(f"  → {result['voice_name']}")
    print("\n")
    
    # Demonstrate best match
    print("🎯 Best Match Demo / Pi bon match")
    print("-" * 70)
    test_text = "Bonjou zanmi! Kijan ou ye jodi a?"
    best_voices = manager.get_best_voice_for_text(test_text, max_results=3)
    print(f"Best voices for: '{test_text}'")
    for i, voice in enumerate(best_voices, 1):
        print(f"  {i}. {voice['voice_name']} (rating: {voice['rating']:.1f})")
    print("\n")
    
    # Show by gender
    print("👥 By Gender / Pa Sèks")
    print("-" * 70)
    for gender in ['male', 'female', 'other']:
        gender_voices = manager.list_voices(gender=gender)
        if gender_voices:
            print(f"{gender.capitalize()}: {len(gender_voices)}")
            for v in gender_voices:
                print(f"  → {v['voice_name']}")
    print("\n")
    
    # Show by region
    print("🌍 By Region / Pa Rejyon")
    print("-" * 70)
    regions = set(v['region'] for v in voices)
    for region in regions:
        region_voices = manager.list_voices(region=region)
        print(f"{region}: {len(region_voices)}")
        for v in region_voices:
            print(f"  → {v['voice_name']}")
    print("\n")
    
    # API examples
    print("💻 API Examples / Egzanp API")
    print("-" * 70)
    print("""
# Initialize manager
from src.custom_voice_manager import CustomVoiceManager
manager = CustomVoiceManager()

# List all voices
all_voices = manager.list_voices()

# Filter by language
creole_voices = manager.list_voices(language='ht')

# Filter by gender
female_voices = manager.list_voices(gender='female')

# Search voices
results = manager.search_voices("bonjou")

# Get best voice for text
best = manager.get_best_voice_for_text("Kijan ou ye?")

# Get voice path
voice_path = manager.get_voice_path(voice_id)

# Update stats (after using)
manager.update_voice_stats(voice_id, rating=5.0)

# Get statistics
stats = manager.get_statistics()
    """)
    
    print("="*70)
    print("✅ DEMO COMPLETE!")
    print("="*70)
    print("\n📖 Pou plis enfòmasyon / For more information:")
    print("   → CUSTOM_VOICE_GUIDE.md")
    print("   → QUICK_START_CUSTOM_VOICES.md")
    print("\n🎙️ Pou ajoute vwa / To add voices:")
    print("   → python add_custom_voice.py")
    print("\n")


if __name__ == "__main__":
    try:
        demo_features()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

