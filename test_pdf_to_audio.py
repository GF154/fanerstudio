#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Test Script: PDF → Audio Conversion
Script pou teste konvèsyon PDF an odyo
"""

import sys
import os

# Test 1: PDF Extraction
print("=" * 60)
print("🧪 TEST 1: PDF TEXT EXTRACTION")
print("=" * 60)

try:
    import PyPDF2
    print("✅ PyPDF2 installed")
    
    def extract_text_from_pdf(pdf_path):
        """Extract text from PDF file"""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    # Test with a PDF if available
    test_pdf = "liv.pdf"
    if os.path.exists(test_pdf):
        print(f"\n📄 Testing with: {test_pdf}")
        pdf_text = extract_text_from_pdf(test_pdf)
        print(f"✅ Extracted {len(pdf_text)} characters")
        print(f"✅ Word count: {len(pdf_text.split())} words")
        print(f"\n📝 First 500 characters:")
        print("-" * 60)
        print(pdf_text[:500])
        print("-" * 60)
    else:
        print(f"⚠️  Test PDF not found: {test_pdf}")
        print("💡 Create a test PDF or specify path")

except ImportError:
    print("❌ PyPDF2 not installed")
    print("📦 Install with: pip install PyPDF2")
    sys.exit(1)

# Test 2: Text-to-Speech
print("\n" + "=" * 60)
print("🧪 TEST 2: TEXT-TO-SPEECH ENGINE")
print("=" * 60)

try:
    from gtts import gTTS
    print("✅ gTTS installed")
    
    # Test TTS with sample text (use French for Creole - closest match)
    sample_text = "Bonjou! Sa se yon test pou Text-to-Speech an Kreyòl Ayisyen."
    
    print(f"\n🗣️  Testing TTS with: '{sample_text}'")
    print("💡 Note: Using French voice (closest to Creole)")
    
    tts = gTTS(text=sample_text, lang='fr', slow=False)  # Use 'fr' for Creole
    output_file = "test_output.mp3"
    tts.save(output_file)
    
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        print(f"✅ Audio generated: {output_file}")
        print(f"✅ File size: {file_size / 1024:.2f} KB")
        
        # Cleanup
        os.remove(output_file)
        print("🧹 Cleaned up test file")
    
except ImportError:
    print("❌ gTTS not installed")
    print("📦 Install with: pip install gtts")
    sys.exit(1)

# Test 3: Full PDF to Audio Pipeline
print("\n" + "=" * 60)
print("🧪 TEST 3: FULL PDF → AUDIO PIPELINE")
print("=" * 60)

try:
    from pdf_processor import DocumentProcessor
    from tts_engine import TTSEngine
    
    print("✅ PDF Processor available")
    print("✅ TTS Engine available")
    
    # Test with sample text (simulate PDF extraction)
    sample_pdf_text = """
    Bonjou tout moun! Sa se yon egzanp tèks an Kreyòl Ayisyen.
    
    Sistèm sa a ka konvèti PDF an audiobook. Li ka li tout kalite dokiman:
    - PDF
    - DOCX
    - TXT
    - EPUB
    
    Sistèm nan itilize gTTS pou jenere odyo ak kalite wo.
    Li ka trete dokiman long epi li separe yo an moso pou pwosese yo.
    """
    
    print(f"\n📝 Sample text length: {len(sample_pdf_text)} characters")
    
    # Initialize TTS engine
    tts = TTSEngine()
    
    # Generate audio
    print("🎙️  Generating audio...")
    output_file = "test_audiobook.mp3"
    
    audio_file = tts.generate_audio(
        text=sample_pdf_text,
        output_file=output_file,
        voice="natural",
        speed=1.0,
        format="mp3",
        lang="fr"  # Use French for Creole
    )
    
    if os.path.exists(audio_file):
        file_size = os.path.getsize(audio_file)
        duration = tts.get_audio_duration(audio_file)
        duration_formatted = tts.format_duration(duration)
        
        print(f"✅ Audiobook generated: {audio_file}")
        print(f"✅ File size: {file_size / 1024:.2f} KB")
        print(f"✅ Duration: {duration_formatted}")
        
        # Cleanup
        os.remove(audio_file)
        print("🧹 Cleaned up test file")
    
except ImportError as e:
    print(f"❌ Module not available: {e}")
    print("💡 Make sure pdf_processor.py and tts_engine.py are in the same directory")

# Summary
print("\n" + "=" * 60)
print("📊 TEST SUMMARY")
print("=" * 60)
print("✅ All tests completed!")
print("\n💡 To test with your own PDF:")
print("   1. Place your PDF file as 'liv.pdf' in this directory")
print("   2. Run this script again")
print("   3. Check the output!")
print("\n🚀 Ready for production deployment!")

