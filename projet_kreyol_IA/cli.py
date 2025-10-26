#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI Advanced / Command Line Interface
Enhanced CLI with arguments and options
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

# Fix Windows console encoding
if sys.platform.startswith('win'):
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

from src import Config, PDFExtractor, CreoleTranslator, AudiobookGenerator, setup_logging


def create_parser() -> argparse.ArgumentParser:
    """
    Kreye parser pou CLI / Create CLI parser
    """
    parser = argparse.ArgumentParser(
        description='🇭🇹 Pwojè Kreyòl IA - Haitian Creole AI Project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples / Egzanp:
  # Basic usage
  python cli.py input.pdf
  
  # With output path
  python cli.py input.pdf -o output/my_audiobook.mp3
  
  # Enable cache and parallel
  python cli.py input.pdf --cache --parallel --workers 4
  
  # Batch processing
  python cli.py *.pdf --batch
  
  # Custom chunk size
  python cli.py input.pdf --chunk-size 1500
  
  # Disable audio generation
  python cli.py input.pdf --no-audio
        '''
    )
    
    # Positional arguments
    parser.add_argument(
        'input',
        nargs='+',
        help='Fichye PDF pou trete / PDF file(s) to process'
    )
    
    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument(
        '-o', '--output',
        type=str,
        help='Chemen pou sove rezilta / Output path for results'
    )
    output_group.add_argument(
        '--output-dir',
        type=str,
        default='output',
        help='Dosye pou sove rezilta / Output directory (default: output)'
    )
    output_group.add_argument(
        '--no-audio',
        action='store_true',
        help='Pa kreye liv odyo / Don\'t generate audiobook'
    )
    
    # Translation options
    trans_group = parser.add_argument_group('Translation Options')
    trans_group.add_argument(
        '--source-lang',
        type=str,
        help='Lang sous (ex: fr, en) / Source language (e.g., fr, en)'
    )
    trans_group.add_argument(
        '--target-lang',
        type=str,
        default='ht',
        help='Lang sib (default: ht) / Target language (default: ht)'
    )
    trans_group.add_argument(
        '--chunk-size',
        type=int,
        default=1000,
        help='Gwosè chunk pou tradiksyon / Chunk size for translation (default: 1000)'
    )
    
    # Performance options
    perf_group = parser.add_argument_group('Performance Options')
    perf_group.add_argument(
        '--cache',
        action='store_true',
        help='Aktive cache / Enable cache'
    )
    perf_group.add_argument(
        '--no-cache',
        action='store_true',
        help='Dezaktive cache / Disable cache'
    )
    perf_group.add_argument(
        '--parallel',
        action='store_true',
        help='Aktive tradiksyon paralèl / Enable parallel translation'
    )
    perf_group.add_argument(
        '--workers',
        type=int,
        default=3,
        help='Kantite workers pou paralèl / Number of workers for parallel (default: 3)'
    )
    
    # Processing options
    proc_group = parser.add_argument_group('Processing Options')
    proc_group.add_argument(
        '--batch',
        action='store_true',
        help='Trete plizyè fichye / Batch process multiple files'
    )
    proc_group.add_argument(
        '--extract-only',
        action='store_true',
        help='Ekstrè tèks sèlman / Extract text only'
    )
    proc_group.add_argument(
        '--translate-only',
        action='store_true',
        help='Tradui sèlman (bezwen fichye tèks) / Translate only (requires text file)'
    )
    
    # Other options
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Mode verbose / Verbose mode'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Mode silansye / Quiet mode'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='Kreyòl IA v3.0.0'
    )
    
    return parser


def process_single_file(
    pdf_path: Path,
    config: Config,
    args: argparse.Namespace,
    logger
) -> bool:
    """
    Trete yon sèl fichye / Process single file
    
    Args:
        pdf_path: Path to PDF
        config: Configuration
        args: CLI arguments
        logger: Logger instance
    
    Returns:
        True if successful
    """
    try:
        if not args.quiet:
            print(f"\n{'='*60}")
            print(f"📄 Ap trete / Processing: {pdf_path.name}")
            print(f"{'='*60}")
        
        logger.info(f"Processing: {pdf_path}")
        
        # Initialize modules
        extractor = PDFExtractor(config)
        translator = CreoleTranslator(config)
        generator = AudiobookGenerator(config)
        
        # Step 1: Extract
        if not args.quiet:
            print("\n⏳ ETAP 1: Ekstraksyon...")
        
        text = extractor.extract_and_save(
            pdf_path,
            show_progress=not args.quiet
        )
        
        if args.extract_only:
            if not args.quiet:
                print("\n✅ Ekstraksyon konplete!")
            return True
        
        # Step 2: Translate
        if not args.quiet:
            print("\n🧠 ETAP 2: Tradiksyon...")
        
        translated = translator.translate_and_save(
            text,
            src_lang=args.source_lang,
            show_progress=not args.quiet
        )
        
        if args.translate_only or args.no_audio:
            if not args.quiet:
                print("\n✅ Tradiksyon konplete!")
            return True
        
        # Step 3: Generate audio
        if not args.quiet:
            print("\n🎧 ETAP 3: Kreyasyon odyo...")
        
        output_path = args.output if args.output else config.output_audio_path
        generator.generate(translated, output_path=Path(output_path))
        
        if not args.quiet:
            print(f"\n{'='*60}")
            print("✅ KONPLE! / COMPLETE!")
            print(f"{'='*60}")
        
        logger.info(f"Successfully processed: {pdf_path}")
        return True
        
    except Exception as e:
        if not args.quiet:
            print(f"\n❌ ERÈR / ERROR: {str(e)}")
        logger.error(f"Error processing {pdf_path}: {e}")
        return False


def process_batch(
    pdf_paths: list[Path],
    config: Config,
    args: argparse.Namespace,
    logger
) -> tuple[int, int]:
    """
    Trete plizyè fichye / Process multiple files
    
    Args:
        pdf_paths: List of PDF paths
        config: Configuration
        args: CLI arguments
        logger: Logger instance
    
    Returns:
        Tuple of (successful, failed) counts
    """
    print(f"\n{'='*60}")
    print(f"📦 BATCH PROCESSING - {len(pdf_paths)} fichye")
    print(f"{'='*60}")
    
    successful = 0
    failed = 0
    
    for i, pdf_path in enumerate(pdf_paths, 1):
        print(f"\n[{i}/{len(pdf_paths)}] {pdf_path.name}")
        
        if process_single_file(pdf_path, config, args, logger):
            successful += 1
        else:
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"✅ Siksè / Success: {successful}")
    print(f"❌ Echwe / Failed: {failed}")
    print(f"{'='*60}")
    
    return successful, failed


def main():
    """Main CLI function"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Create configuration from args
    config = Config(
        output_dir=Path(args.output_dir),
        target_language=args.target_lang,
        source_language=args.source_lang,
        chunk_size=args.chunk_size,
        enable_cache=args.cache if args.cache else not args.no_cache,
        enable_parallel=args.parallel,
        max_workers=args.workers,
        log_level='DEBUG' if args.verbose else 'INFO',
    )
    
    # Setup logging
    logger = setup_logging(
        config.logs_dir,
        log_level='DEBUG' if args.verbose else 'INFO'
    )
    
    if not args.quiet:
        print("🇭🇹 PWOJÈ KREYÒL IA v3.0")
        print(f"Config: cache={config.enable_cache}, parallel={config.enable_parallel}")
    
    # Get PDF files
    pdf_paths = []
    for input_path in args.input:
        path = Path(input_path)
        if path.is_file():
            pdf_paths.append(path)
        elif path.is_dir():
            pdf_paths.extend(path.glob('*.pdf'))
        else:
            # Try glob pattern
            pdf_paths.extend(Path('.').glob(input_path))
    
    if not pdf_paths:
        print("❌ Pa gen fichye PDF jwenn / No PDF files found")
        return 1
    
    # Process files
    if args.batch or len(pdf_paths) > 1:
        successful, failed = process_batch(pdf_paths, config, args, logger)
        return 0 if failed == 0 else 1
    else:
        success = process_single_file(pdf_paths[0], config, args, logger)
        return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

