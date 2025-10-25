#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pwojè Kreyòl IA - Tradiksyon ak Liv Odyo
Haitian Creole AI Project - Translation and Audiobook Generation
Version 3.0 - Phase 2: Modular Architecture
"""

import sys
from pathlib import Path

# Fix Windows console encoding for Unicode support
if sys.platform.startswith('win'):
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

# Import modules
from src import Config, PDFExtractor, CreoleTranslator, AudiobookGenerator, setup_logging


def print_header():
    """Print application header"""
    print("="*60)
    print("🇭🇹 PWOJÈ KREYÒL IA / HAITIAN CREOLE AI PROJECT")
    print("="*60)
    print("Version 3.0 - Phase 2: Modular Architecture")
    print()


def print_results(config: Config, success: bool = True):
    """Print final results"""
    print("\n" + "="*60)
    if success:
        print("✅ LIV ODYO AN KREYÒL PARE!")
        print("✅ CREOLE AUDIOBOOK READY!")
    else:
        print("⚠️  Pwosesis la echwe / Process failed")
    print("="*60)
    print(f"📄 Tèks orijinal / Original text: {config.output_text_path}")
    print(f"🌍 Tèks tradui / Translated text: {config.output_translation_path}")
    print(f"🔊 Liv odyo / Audiobook: {config.output_audio_path}")
    print(f"📋 Log files: {config.logs_dir}/")
    if config.enable_cache:
        print(f"💾 Cache: {config.cache_dir}/")
    print("="*60)


def main():
    """Fonksyon prensipal / Main function"""
    
    # Print header
    print_header()
    
    # Load configuration
    config = Config.from_env()
    logger = setup_logging(config.logs_dir, config.log_level)
    
    logger.info("="*60)
    logger.info("Starting Kreyol AI Project - Version 3.0")
    logger.info(f"Configuration: {config}")
    logger.info("="*60)
    
    try:
        # Initialize modules
        pdf_extractor = PDFExtractor(config)
        translator = CreoleTranslator(config)
        audio_generator = AudiobookGenerator(config)
        
        # Check if PDF exists
        if not config.pdf_input_path.exists():
            print(f"\n❌ FICHYE PA JWENN / FILE NOT FOUND:")
            print(f"   {config.pdf_input_path}")
            print(f"\n📝 Tanpri mete yon fichye PDF nan dosye 'data/' ak non 'input.pdf'")
            print(f"📝 Please place a PDF file in the 'data/' folder named 'input.pdf'")
            logger.error(f"PDF file not found: {config.pdf_input_path}")
            return 1
        
        # ETAP 1: Ekstraksyon PDF / PDF Extraction
        print("\n⏳ ETAP 1: Ekstraksyon tèks nan PDF...")
        print("⏳ STEP 1: Extracting text from PDF...")
        
        text = pdf_extractor.extract_and_save(
            config.pdf_input_path,
            show_progress=True
        )
        
        # ETAP 2: Tradiksyon / Translation
        print("\n🧠 ETAP 2: Tradiksyon an kreyòl ayisyen...")
        print("🧠 STEP 2: Translating to Haitian Creole...")
        print("⚠️  Sa ka pran kèk minit... / This may take several minutes...")
        
        translated_text = translator.translate_and_save(
            text,
            show_progress=True
        )
        
        # ETAP 3: Kreye Liv Odyo / Create Audiobook
        print("\n🎧 ETAP 3: Kreye liv odyo kreyòl...")
        print("🎧 STEP 3: Creating Creole audiobook...")
        
        audio_generator.generate(translated_text)
        
        # Print results
        print_results(config, success=True)
        
        logger.info("Process completed successfully!")
        return 0
        
    except FileNotFoundError as e:
        print(f"\n❌ FICHYE PA JWENN / FILE NOT FOUND:")
        print(f"   {str(e)}")
        logger.error(f"File not found: {e}")
        return 1
        
    except ValueError as e:
        print(f"\n❌ ERÈR VALIDASYON / VALIDATION ERROR:")
        print(f"   {str(e)}")
        logger.error(f"Validation error: {e}")
        return 1
        
    except RuntimeError as e:
        print(f"\n❌ ERÈR PWOSESIS / PROCESSING ERROR:")
        print(f"   {str(e)}")
        logger.error(f"Runtime error: {e}")
        return 1
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Pwosesis enti pa itilizatè / Process interrupted by user")
        logger.warning("Process interrupted by user")
        return 130
        
    except Exception as e:
        print(f"\n❌ ERÈR ENATENDU / UNEXPECTED ERROR:")
        print(f"   {str(e)}")
        print("\n💡 KONSÈY / TIP:")
        print("   - Verifye log file nan dosye 'logs/'")
        print("   - Check log file in 'logs/' folder")
        print("   - Verifye ke ou gen tout depandans yo enstale")
        print("   - Verify that all dependencies are installed")
        print("   - pip install -r requirements.txt")
        logger.exception("Unexpected error occurred")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
