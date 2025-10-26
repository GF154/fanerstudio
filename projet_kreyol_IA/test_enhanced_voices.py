#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for enhanced TTS voices
Script pour tester les voix améliorées
"""

import asyncio
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.tts_enhanced import EnhancedTTS

async def test_voices():
    """Test different voices with Haitian Creole text"""
    
    tts = EnhancedTTS()
    
    print("\n" + "="*60)
    print("🎙️  TEST DES VOIX POUR LE CREOLE HAITIEN")
    print("   Testing Voices for Haitian Creole")
    print("="*60 + "\n")
    
    # Sample Haitian Creole text
    text = """
    Bonjou zanmi! Kijan ou ye jodi a? 
    Mwen espere ou pase yon bon jounen.
    Sa a se yon tès pou wè si vwa a klè.
    """
    
    print(f"📝 Texte de test / Test text:")
    print(f"   {text.strip()}\n")
    
    # Create output directory
    output_dir = Path("test_voices_output")
    output_dir.mkdir(exist_ok=True)
    
    print(f"📁 Fichiers seront sauvegardés dans / Files will be saved in:")
    print(f"   {output_dir.absolute()}\n")
    
    print("="*60)
    print("TEST 1: Meilleure voix disponible (Automatique)")
    print("Test 1: Best available voice (Automatic)")
    print("="*60)
    
    try:
        output_path = output_dir / "test_best_available.mp3"
        result_path, engine_used = tts.generate_best_available(
            text, output_path, prefer_quality=True
        )
        print(f"✅ Success!")
        print(f"   Engine: {engine_used}")
        print(f"   File: {result_path}")
        print(f"   Size: {result_path.stat().st_size / 1024:.1f} KB\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    
    # Test Edge TTS if available
    if tts.available_engines['edge']['available']:
        print("="*60)
        print("TEST 2: Microsoft Edge TTS (Voix recommandées)")
        print("Test 2: Microsoft Edge TTS (Recommended voices)")
        print("="*60 + "\n")
        
        voices = [
            ("fr-CA-SylvieNeural", "Canadienne (MEILLEUR pour Créole)"),
            ("fr-FR-DeniseNeural", "Française (Claire et naturelle)"),
            ("fr-CA-AntoineNeural", "Canadien homme"),
        ]
        
        for voice, description in voices:
            print(f"Testing {voice}...")
            print(f"   {description}")
            try:
                output_path = output_dir / f"test_{voice}.mp3"
                await tts.generate_edge_tts(text, output_path, voice)
                print(f"   ✅ Saved to: {output_path.name}")
                print(f"   Size: {output_path.stat().st_size / 1024:.1f} KB\n")
            except Exception as e:
                print(f"   ❌ Error: {e}\n")
    
    # Test gTTS
    print("="*60)
    print("TEST 3: Google TTS (Français Canadien)")
    print("Test 3: Google TTS (Canadian French)")
    print("="*60)
    
    try:
        output_path = output_dir / "test_gtts_canadian.mp3"
        tts.generate_gtts_canadian_french(text, output_path)
        print(f"✅ Success!")
        print(f"   File: {output_path}")
        print(f"   Size: {output_path.stat().st_size / 1024:.1f} KB\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    
    # Test pyttsx3 if available
    if tts.available_engines['pyttsx3']['available']:
        print("="*60)
        print("TEST 4: pyttsx3 (Voix hors ligne)")
        print("Test 4: pyttsx3 (Offline voice)")
        print("="*60)
        
        try:
            output_path = output_dir / "test_pyttsx3.mp3"
            tts.generate_pyttsx3(text, output_path)
            print(f"✅ Success!")
            print(f"   File: {output_path}")
            print(f"   Size: {output_path.stat().st_size / 1024:.1f} KB\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")
    
    print("="*60)
    print("✅ TESTS COMPLETES!")
    print("="*60)
    print(f"\n📁 Ecoutez les fichiers dans: {output_dir.absolute()}")
    print(f"   Listen to files in: {output_dir.absolute()}")
    print("\n🎧 Choisissez votre voix préférée!")
    print("   Choose your favorite voice!\n")
    
    # Show recommendations
    print("="*60)
    print("🌟 RECOMMANDATIONS POUR LE CREOLE")
    print("   Recommendations for Creole")
    print("="*60)
    recs = tts.get_recommendations_for_creole()
    print(f"\n1. Meilleure qualité en ligne:")
    print(f"   Best online quality:")
    print(f"   → {recs['best_online']['voice']}")
    print(f"   Raison: {recs['best_online']['reason']}")
    print(f"\n2. Meilleure option hors ligne:")
    print(f"   Best offline option:")
    print(f"   → {recs['best_offline']['voice']}")
    print(f"   Raison: {recs['best_offline']['reason']}")
    print(f"\n3. Option actuelle (recommandée):")
    print(f"   Current option (recommended):")
    print(f"   → {recs['current']['voice']}")
    print(f"   Raison: {recs['current']['reason']}")
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(test_voices())

