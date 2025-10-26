#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main script pou workflow cloud / Main cloud workflow
Alias pour process_book.py avec affichage des URLs publiques
"""

import os
from pathlib import Path
from utils.cloud_storage import upload_to_gcs, download_from_gcs
from utils.text_extraction import extract_text_from_pdf
from utils.translate import translate_text
from utils.audio_gen import generate_audio
from utils.podcast_mix import mix_voices

bucket = os.getenv("GCS_BUCKET_NAME")

if not bucket:
    print("⚠️  GCS_BUCKET_NAME pa defini nan environment variables")
    print("   Defini l ak: export GCS_BUCKET_NAME=your-bucket-name")
    print("   Oswa kreye yon fichye .env")
    exit(1)

# Create directories
Path("input").mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)

print("=" * 60)
print("🚀 PWOSESIS LIV KREYÒL / BOOK PROCESSING")
print("=" * 60)

# --- 1. Telechaje PDF orijinal la depi nan cloud ---
download_from_gcs("input/liv1.pdf", "input/liv1.pdf", bucket)

# --- 2. Ekstrè tèks ---
text = extract_text_from_pdf("input/liv1.pdf")

# --- 3. Tradui ---
translated = translate_text(text, "ht")
txt_path = "output/liv1_kreyol.txt"
open(txt_path, "w", encoding="utf-8").write(translated)
url_txt = upload_to_gcs(txt_path, "output/liv1_kreyol.txt", bucket)

# --- 4. Kreye audiobook ---
audio_path = generate_audio(translated, "output/liv1_audio.mp3")
url_audio = upload_to_gcs(audio_path, "output/liv1_audio.mp3", bucket)

# --- 5. Kreye podcast ak lòt vwa ---
final_podcast = mix_voices(["output/liv1_audio.mp3"], "output/podcast_final.mp3")
url_podcast = upload_to_gcs(final_podcast, "output/podcast_final.mp3", bucket)

print("\n🎧 --- LYEN PIBLIK YO ---")
print(f"📘 Tèks tradui: {url_txt}")
print(f"🔊 Audiobook: {url_audio}")
print(f"🎙️ Podcast: {url_podcast}")
print("\n✅ Workflow fini avèk siksè!")

