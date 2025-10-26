#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pou trete liv ak Google Cloud Storage
Process books with Google Cloud Storage integration
"""

import os
from pathlib import Path
from utils.cloud_storage import upload_to_gcs, download_from_gcs
from utils.text_extraction import extract_text_from_pdf
from utils.translate import translate_text
from utils.audio_gen import generate_audio
from utils.podcast_mix import mix_voices

# Configuration
bucket = os.getenv("GCS_BUCKET_NAME")

if not bucket:
    print("⚠️  GCS_BUCKET_NAME pa defini nan environment variables")
    print("   Defini l ak: export GCS_BUCKET_NAME=your-bucket-name")
    print("   Oswa kreye yon fichye .env")
    exit(1)

# Create directories if they don't exist
Path("input").mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)

print("=" * 60)
print("🚀 PWOSESIS LIV KREYÒL / BOOK PROCESSING")
print("=" * 60)

# --- 1. Telechaje PDF orijinal la depi nan cloud ---
print("\n📥 ETAP 1: Telechajman fichye PDF / Downloading PDF file")
print("-" * 60)
try:
    download_from_gcs("input/liv1.pdf", "input/liv1.pdf", bucket)
except Exception as e:
    print(f"❌ Erè telechajman / Download error: {e}")
    print("   Verifye si fichye a egziste nan bucket ou a")
    exit(1)

# --- 2. Ekstrè tèks ---
print("\n📄 ETAP 2: Ekstraksyon tèks / Text extraction")
print("-" * 60)
try:
    text = extract_text_from_pdf("input/liv1.pdf")
    print(f"✅ Tèks ekstré / Text extracted: {len(text)} karaktè / characters")
except Exception as e:
    print(f"❌ Erè ekstraksyon / Extraction error: {e}")
    exit(1)

# --- 3. Tradui ---
print("\n🌍 ETAP 3: Tradiksyon / Translation")
print("-" * 60)
try:
    translated = translate_text(text, "ht")
    
    # Save translated text
    txt_path = "output/liv1_kreyol.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(translated)
    print(f"✅ Tradiksyon sove / Translation saved: {txt_path}")
    
    # Upload to cloud and get public URL
    url_txt = upload_to_gcs(txt_path, "output/liv1_kreyol.txt", bucket)
except Exception as e:
    print(f"❌ Erè tradiksyon / Translation error: {e}")
    exit(1)

# --- 4. Kreye audiobook ---
print("\n🎧 ETAP 4: Kreyasyon audiobook / Audiobook generation")
print("-" * 60)
try:
    audio_path = generate_audio(translated, "output/liv1_audio.mp3", language="ht")
    print(f"✅ Audiobook kreyé / Audiobook created: {audio_path}")
    
    # Upload to cloud and get public URL
    url_audio = upload_to_gcs(audio_path, "output/liv1_audio.mp3", bucket)
except Exception as e:
    print(f"❌ Erè kreyasyon odyo / Audio generation error: {e}")
    exit(1)

# --- 5. Kreye podcast ak lòt vwa ---
print("\n🎙️ ETAP 5: Kreyasyon podcast / Podcast creation")
print("-" * 60)
try:
    final_podcast = mix_voices(["output/liv1_audio.mp3"], "output/podcast_final.mp3")
    print(f"✅ Podcast kreyé / Podcast created: {final_podcast}")
    
    # Upload to cloud and get public URL
    url_podcast = upload_to_gcs(final_podcast, "output/podcast_final.mp3", bucket)
except Exception as e:
    print(f"❌ Erè kreyasyon podcast / Podcast creation error: {e}")
    exit(1)

# --- Summary with public URLs ---
print("\n" + "=" * 60)
print("🎉 Tout rezilta yo televersé nan Google Cloud Storage avèk siksè!")
print("   All results uploaded to Google Cloud Storage successfully!")
print("=" * 60)

print("\n🎧 --- LYEN PIBLIK YO / PUBLIC LINKS ---")
print(f"📘 Tèks tradui / Translated text: {url_txt}")
print(f"🔊 Audiobook: {url_audio}")
print(f"🎙️ Podcast: {url_podcast}")

print("\n✅ Workflow fini avèk siksè!")
print("✅ Workflow completed successfully!")
print("=" * 60)

