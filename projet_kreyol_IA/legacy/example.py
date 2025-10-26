#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Egzanp Itilizasyon / Usage Example
Montre kijan itilize KreyolAIProcessor
Shows how to use KreyolAIProcessor
"""

from main import KreyolAIProcessor
from pathlib import Path

def example_1_basic_usage():
    """Egzanp baz: Trete yon PDF"""
    print("\n" + "="*60)
    print("EGZANP 1: Itilizasyon Baz / EXAMPLE 1: Basic Usage")
    print("="*60)
    
    processor = KreyolAIProcessor()
    
    # Verifye si gen yon PDF
    pdf_path = processor.data_dir / "input.pdf"
    if pdf_path.exists():
        processor.process_full_pipeline(pdf_path)
    else:
        print(f"❌ Pa gen PDF nan: {pdf_path}")
        print("Tanpri ajoute yon fichye 'input.pdf' nan dosye 'data/'")


def example_2_custom_path():
    """Egzanp 2: Itilize yon chemen espesifik"""
    print("\n" + "="*60)
    print("EGZANP 2: Chemen Espesifik / EXAMPLE 2: Custom Path")
    print("="*60)
    
    processor = KreyolAIProcessor()
    
    # Espesifye yon lòt PDF
    custom_pdf = Path("path/to/your/document.pdf")
    
    if custom_pdf.exists():
        processor.process_full_pipeline(custom_pdf)
    else:
        print(f"ℹ️ Egzanp: modifye 'custom_pdf' nan kòd la pou itilize pwòp fichye w")


def example_3_extract_only():
    """Egzanp 3: Ekstrè tèks sèlman"""
    print("\n" + "="*60)
    print("EGZANP 3: Ekstraksyon Sèlman / EXAMPLE 3: Extract Only")
    print("="*60)
    
    processor = KreyolAIProcessor()
    pdf_path = processor.data_dir / "input.pdf"
    
    if pdf_path.exists():
        # Ekstrè tèks sèlman
        text = processor.extract_text_from_pdf(pdf_path)
        if text:
            print(f"\n✅ Ekstrè {len(text)} karaktè")
            print(f"✅ Extracted {len(text)} characters")
            print(f"\nPremye 200 karaktè / First 200 characters:")
            print("-" * 60)
            print(text[:200] + "...")


def example_4_translate_only():
    """Egzanp 4: Tradui tèks ki egziste deja"""
    print("\n" + "="*60)
    print("EGZANP 4: Tradiksyon Sèlman / EXAMPLE 4: Translate Only")
    print("="*60)
    
    processor = KreyolAIProcessor()
    
    # Li tèks ki deja ekstrè
    text_file = processor.data_dir / "output_text.txt"
    if text_file.exists():
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Tradui tèks la
        translated = processor.translate_text(text)
        if translated:
            print(f"\n✅ Tradui {len(translated)} karaktè")
    else:
        print(f"❌ Pa gen tèks pou tradui. Egzekite extract_text_from_pdf dabò")


def example_5_audiobook_only():
    """Egzanp 5: Kreye liv odyo sèlman"""
    print("\n" + "="*60)
    print("EGZANP 5: Liv Odyo Sèlman / EXAMPLE 5: Audiobook Only")
    print("="*60)
    
    processor = KreyolAIProcessor()
    
    # Li tèks ki deja tradui
    translation_file = processor.output_dir / "traduction.txt"
    if translation_file.exists():
        with open(translation_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Kreye liv odyo
        audiobook = processor.create_audiobook(text)
        if audiobook:
            print(f"\n✅ Liv odyo kreye: {audiobook}")
    else:
        print(f"❌ Pa gen tradiksyon. Egzekite translate_text dabò")


def main():
    """Meni prensipal / Main menu"""
    print("\n🇭🇹 EGZANP ITILIZASYON - PWOJÈ KREYÒL IA")
    print("🇭🇹 USAGE EXAMPLES - HAITIAN CREOLE AI PROJECT")
    print("="*60)
    print("\nChwazi yon egzanp / Choose an example:")
    print("1. Trete PDF konplètman (extract + translate + audio)")
    print("2. Itilize chemen espesifik / Use custom path")
    print("3. Ekstrè tèks sèlman / Extract text only")
    print("4. Tradui tèks sèlman / Translate only")
    print("5. Kreye liv odyo sèlman / Create audiobook only")
    print("0. Soti / Exit")
    
    choice = input("\nChwa w (0-5): ")
    
    if choice == "1":
        example_1_basic_usage()
    elif choice == "2":
        example_2_custom_path()
    elif choice == "3":
        example_3_extract_only()
    elif choice == "4":
        example_4_translate_only()
    elif choice == "5":
        example_5_audiobook_only()
    elif choice == "0":
        print("\nOrevwa! / Goodbye!")
    else:
        print("\n❌ Chwa envalid / Invalid choice")


if __name__ == "__main__":
    main()

