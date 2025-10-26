#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive tool to add custom voices to the platform
Outil interactif pour ajouter des voix personnalisées
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.custom_voice_manager import CustomVoiceManager


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*70)
    print("🎙️  AJOUTE YON VWA NATIRÈL / ADD A NATURAL VOICE")
    print("   Plateforme Kreyòl IA - Custom Voice Manager")
    print("="*70 + "\n")


def get_input(prompt: str, default: str = "") -> str:
    """Get user input with optional default"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    return input(f"{prompt}: ").strip()


def add_voice_interactive():
    """Interactive wizard to add a custom voice"""
    print_banner()
    
    # Initialize voice manager
    manager = CustomVoiceManager()
    
    print("📋 Enfòmasyon / Information")
    print("-" * 70)
    print("Pou ajoute yon vwa natirèl, ou bezwen:")
    print("To add a natural voice, you need:")
    print("  1. Yon fichye odyo (MP3, WAV, etc.)")
    print("     An audio file (MP3, WAV, etc.)")
    print("  2. Tèks ki te di nan odyo a")
    print("     The text that was spoken in the audio")
    print("\n")
    
    # Get audio file path
    while True:
        audio_path_str = get_input("📁 Chemen fichye odyo / Audio file path")
        audio_path = Path(audio_path_str)
        
        if audio_path.exists():
            print(f"   ✅ Fichye jwenn / File found: {audio_path.name}")
            break
        else:
            print(f"   ❌ Fichye pa egziste / File not found. Try again.")
    
    print("\n")
    
    # Get voice details
    print("📝 Detay vwa a / Voice details")
    print("-" * 70)
    
    voice_name = get_input("Non vwa a / Voice name", f"Voice_{len(manager.voices) + 1}")
    speaker_name = get_input("Non moun ki pale a / Speaker name", "Anonymous")
    
    print("\n📄 Tèks ki te di / Text that was spoken:")
    print("   (Tape ou kolye vwa a, tape 'END' sou yon liy pou fini)")
    print("   (Paste or type the text, type 'END' on a line to finish)")
    print("-" * 70)
    
    text_lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        text_lines.append(line)
    
    text_content = "\n".join(text_lines).strip()
    
    if not text_content:
        print("❌ Ou dwe bay tèks la / You must provide the text")
        return
    
    print("\n")
    
    # Optional details
    print("📊 Enfòmasyon opsyonèl / Optional information")
    print("-" * 70)
    
    print("\nSèks / Gender:")
    print("  1. Gason / Male")
    print("  2. Fanm / Female")
    print("  3. Lòt / Other")
    print("  4. Pa konnen / Unknown")
    gender_choice = get_input("Chwazi / Choose (1-4)", "4")
    gender_map = {"1": "male", "2": "female", "3": "other", "4": "unknown"}
    gender = gender_map.get(gender_choice, "unknown")
    
    print("\nLaj / Age range:")
    print("  1. Timoun / Child")
    print("  2. Jèn granmoun / Young adult")
    print("  3. Granmoun / Adult")
    print("  4. Ajan / Senior")
    print("  5. Pa konnen / Unknown")
    age_choice = get_input("Chwazi / Choose (1-5)", "5")
    age_map = {"1": "child", "2": "young_adult", "3": "adult", "4": "senior", "5": "unknown"}
    age_range = age_map.get(age_choice, "unknown")
    
    region = get_input("\nRejyon / Region", "Haiti")
    notes = get_input("Nòt adisyonèl / Additional notes (optional)", "")
    
    print("\n")
    print("="*70)
    print("📊 REZIME / SUMMARY")
    print("="*70)
    print(f"Vwa / Voice: {voice_name}")
    print(f"Moun ki pale / Speaker: {speaker_name}")
    print(f"Fichye / File: {audio_path.name}")
    print(f"Sèks / Gender: {gender}")
    print(f"Laj / Age: {age_range}")
    print(f"Rejyon / Region: {region}")
    print(f"\nTèks / Text preview:")
    print("-" * 70)
    preview = text_content[:200] + "..." if len(text_content) > 200 else text_content
    print(preview)
    print("-" * 70)
    print("\n")
    
    # Confirm
    confirm = get_input("✅ Ajoute vwa sa a? / Add this voice? (yes/no)", "yes")
    
    if confirm.lower() in ['yes', 'y', 'wi', 'oui']:
        try:
            voice_id = manager.add_voice(
                audio_file=audio_path,
                voice_name=voice_name,
                speaker_name=speaker_name,
                text_content=text_content,
                language="ht",
                gender=gender,
                age_range=age_range,
                region=region,
                notes=notes
            )
            
            print("\n" + "="*70)
            print("✅ SIKSÈ / SUCCESS!")
            print("="*70)
            print(f"Vwa ajoute avèk siksè / Voice added successfully!")
            print(f"ID: {voice_id}")
            print(f"Fichye sove nan / File saved in: custom_voices/")
            print("\nOu ka kounye a itilize vwa sa a nan aplikasyon an!")
            print("You can now use this voice in the application!")
            print("="*70 + "\n")
            
        except Exception as e:
            print(f"\n❌ Erè / Error: {e}")
            print("Vwa pa t ajoute / Voice was not added\n")
    else:
        print("\n❌ Anile / Cancelled\n")


def list_voices():
    """List all custom voices"""
    manager = CustomVoiceManager()
    voices = manager.list_voices()
    
    print("\n" + "="*70)
    print(f"📚 VWA DISPONIB / AVAILABLE VOICES ({len(voices)} total)")
    print("="*70 + "\n")
    
    if not voices:
        print("Pa gen vwa ankò. Ajoute youn!")
        print("No voices yet. Add one!")
        print("\n")
        return
    
    for i, voice in enumerate(voices, 1):
        print(f"{i}. {voice['voice_name']}")
        print(f"   ID: {voice['voice_id']}")
        print(f"   Moun ki pale / Speaker: {voice['speaker_name']}")
        print(f"   Sèks / Gender: {voice['gender']}")
        print(f"   Rejyon / Region: {voice['region']}")
        print(f"   Rating: {'⭐' * int(voice['rating'])} ({voice['rating']:.1f})")
        print(f"   Itilize / Used: {voice['times_used']} fwa / times")
        print(f"   Fichye / File: {voice['audio_file']}")
        print(f"   Tèks preview / Text preview: {voice['text_content'][:80]}...")
        print("-" * 70)
    
    print("\n")


def show_statistics():
    """Show voice statistics"""
    manager = CustomVoiceManager()
    stats = manager.get_statistics()
    
    print("\n" + "="*70)
    print("📊 ESTATISTIK VWA / VOICE STATISTICS")
    print("="*70 + "\n")
    
    if stats['total_voices'] == 0:
        print("Pa gen vwa ankò / No voices yet\n")
        return
    
    print(f"Total vwa / Total voices: {stats['total_voices']}")
    print(f"Total tan / Total duration: {stats['total_duration_minutes']:.1f} minit / minutes")
    print(f"Total gwosè / Total size: {stats['total_size_mb']:.1f} MB")
    print(f"Rating mwayen / Average rating: {stats['average_rating']:.1f} ⭐")
    print(f"Pi itilize / Most used: {stats['most_used']}")
    print(f"Pi bon rating / Highest rated: {stats['highest_rated']}")
    
    print("\nLang / Languages:")
    for lang, count in stats['languages'].items():
        print(f"  {lang}: {count}")
    
    print("\nSèks / Genders:")
    for gender, count in stats['genders'].items():
        print(f"  {gender}: {count}")
    
    print("\nRejyon / Regions:")
    for region, count in stats['regions'].items():
        print(f"  {region}: {count}")
    
    print("\n")


def main_menu():
    """Main menu"""
    while True:
        print("\n" + "="*70)
        print("🎙️  JESYON VWA NATIRÈL / NATURAL VOICE MANAGER")
        print("="*70)
        print("\n1. Ajoute yon vwa / Add a voice")
        print("2. Wè tout vwa / List all voices")
        print("3. Estatistik / Statistics")
        print("4. Kite / Exit")
        print("\n")
        
        choice = get_input("Chwazi / Choose (1-4)")
        
        if choice == "1":
            add_voice_interactive()
        elif choice == "2":
            list_voices()
        elif choice == "3":
            show_statistics()
        elif choice == "4":
            print("\n👋 Orevwa / Goodbye!\n")
            break
        else:
            print("\n❌ Chwa envalid / Invalid choice\n")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Pwogram fèmen / Program interrupted\n")
        sys.exit(0)

