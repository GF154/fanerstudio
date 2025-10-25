#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create sample voice files for testing
Créer des exemples de voix pour tester
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.tts_enhanced import EnhancedTTS
from src.custom_voice_manager import CustomVoiceManager


async def create_sample_voices():
    """Create sample voice files using Edge TTS"""
    
    print("\n" + "="*70)
    print("🎙️  KREYE EGZANP VWA / CREATE SAMPLE VOICES")
    print("="*70 + "\n")
    
    # Initialize TTS
    tts = EnhancedTTS()
    
    # Create samples directory
    samples_dir = Path("voice_samples")
    samples_dir.mkdir(exist_ok=True)
    
    print(f"📁 Dossier / Directory: {samples_dir.absolute()}\n")
    
    # Sample texts and voices
    samples = [
        {
            "name": "Marie_Salutation",
            "speaker": "Marie (Voice Demo)",
            "text": "Bonjou zanmi! Kijan ou ye jodi a? Mwen espere ou byen.",
            "voice": "fr-CA-SylvieNeural",
            "gender": "female",
            "region": "Canada (proche créole)",
            "notes": "Voix canadienne, très naturelle pour le créole"
        },
        {
            "name": "Jean_Histoire",
            "speaker": "Jean (Voice Demo)",
            "text": "Yon jou, te gen yon ti gason ki te rele Pierre. Li te renmen ale lekòl anpil.",
            "voice": "fr-CA-AntoineNeural",
            "gender": "male",
            "region": "Canada",
            "notes": "Voix masculine canadienne, idéale pour narration"
        },
        {
            "name": "Sophie_Education",
            "speaker": "Sophie (Voice Demo)",
            "text": "Jodi a n ap aprann kijan pou li an kreyòl. Se yon lang bèl e rich anpil.",
            "voice": "fr-FR-DeniseNeural",
            "gender": "female",
            "region": "France",
            "notes": "Voix française claire, parfaite pour l'éducation"
        }
    ]
    
    voice_manager = CustomVoiceManager()
    created_voices = []
    
    for i, sample in enumerate(samples, 1):
        print(f"{"="*70}")
        print(f"Sample {i}/3: {sample['name']}")
        print(f"{"="*70}")
        
        # Generate audio file
        audio_file = samples_dir / f"{sample['name']}.mp3"
        
        print(f"\n📝 Texte / Text:")
        print(f"   {sample['text']}")
        print(f"\n🎤 Voix / Voice: {sample['voice']}")
        print(f"👤 Speaker: {sample['speaker']}")
        
        try:
            # Generate audio
            print(f"\n⏳ Génération audio en cours...")
            await tts.generate_edge_tts(
                sample['text'],
                audio_file,
                sample['voice']
            )
            
            # Check file
            if audio_file.exists():
                size_kb = audio_file.stat().st_size / 1024
                print(f"✅ Audio généré: {audio_file.name} ({size_kb:.1f} KB)")
                
                # Add to voice manager
                print(f"\n⏳ Ajout à la bibliothèque...")
                voice_id = voice_manager.add_voice(
                    audio_file=audio_file,
                    voice_name=sample['name'],
                    speaker_name=sample['speaker'],
                    text_content=sample['text'],
                    language="ht",
                    gender=sample['gender'],
                    age_range="adult",
                    region=sample['region'],
                    notes=sample['notes']
                )
                
                created_voices.append({
                    'id': voice_id,
                    'name': sample['name'],
                    'file': audio_file
                })
                
                print(f"✅ Ajouté avec ID: {voice_id}\n")
            else:
                print(f"❌ Erreur: fichier non créé\n")
                
        except Exception as e:
            print(f"❌ Erreur: {e}\n")
            continue
    
    # Summary
    print("\n" + "="*70)
    print("✅ CRÉATION TERMINÉE / CREATION COMPLETE")
    print("="*70)
    print(f"\n📊 Résumé / Summary:")
    print(f"   Voix créées / Voices created: {len(created_voices)}")
    print(f"   Dossier / Directory: {samples_dir.absolute()}")
    
    if created_voices:
        print(f"\n🎤 Voix disponibles / Available voices:")
        for v in created_voices:
            print(f"   → {v['name']} (ID: {v['id']})")
        
        print(f"\n📁 Fichiers audio / Audio files:")
        for v in created_voices:
            print(f"   → {v['file'].name}")
        
        # Show statistics
        stats = voice_manager.get_statistics()
        print(f"\n📊 Statistiques bibliothèque / Library stats:")
        print(f"   Total voix / Total voices: {stats['total_voices']}")
        print(f"   Durée totale / Total duration: {stats['total_duration_minutes']:.1f} min")
        print(f"   Taille totale / Total size: {stats['total_size_mb']:.2f} MB")
        
        print(f"\n🎧 Écouter les voix / Listen to voices:")
        print(f"   1. Ouvrez / Open: {samples_dir.absolute()}")
        print(f"   2. Double-cliquez sur les fichiers MP3")
        
        print(f"\n🌐 Dans Streamlit / In Streamlit:")
        print(f"   streamlit run app.py")
        print(f"   → Sidebar → 🎙️ Custom Voices")
        
        print(f"\n💻 Via l'outil / Via tool:")
        print(f"   python add_custom_voice.py")
        print(f"   → Option 2: Wè tout vwa / List all voices")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(create_sample_voices())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

