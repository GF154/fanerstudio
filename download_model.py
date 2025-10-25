#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pre-download the M2M100 translation model
Telechaje modèl tradiksyon M2M100 an avans
"""

import sys
if sys.platform.startswith('win'):
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

print("="*60)
print("🧠 TELECHAJMAN MODÈL / MODEL DOWNLOAD")
print("="*60)
print()
print("📥 Ap telechaje modèl M2M100 (~1.5GB)...")
print("📥 Downloading M2M100 model (~1.5GB)...")
print()
print("⏳ Sa ka pran 5-15 minit selon vitès entènèt ou")
print("⏳ This may take 5-15 minutes depending on internet speed")
print()

try:
    from transformers import pipeline
    
    print("🔄 Enstalasyon modèl / Installing model...")
    translator = pipeline("translation", model="facebook/m2m100_418M")
    
    print()
    print("="*60)
    print("✅ MODÈL TELECHAJE AK SIKSE!")
    print("✅ MODEL DOWNLOADED SUCCESSFULLY!")
    print("="*60)
    print()
    print("🚀 Ou ka kounye a itilize main.py san tann")
    print("🚀 You can now use main.py without waiting")
    print()
    print("📍 Modèl sove nan / Model saved in:")
    print("   C:\\Users\\Fanerlink\\.cache\\huggingface\\hub\\")
    print()
    
except Exception as e:
    print()
    print("❌ ERÈR / ERROR:")
    print(f"   {str(e)}")
    print()
    print("💡 Verifye koneksyon entènèt ou")
    print("💡 Check your internet connection")


