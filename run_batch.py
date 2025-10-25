#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run batch processing from config file
Lance traitement batch depi fichye config
"""

import os
import json
import sys
from pathlib import Path
from batch_processor import BatchProcessor


def load_books_config(config_file: str = "books_config.json") -> list:
    """Load books configuration"""
    config_path = Path(config_file)
    
    if not config_path.exists():
        print(f"❌ Fichye config pa jwenn / Config file not found: {config_file}")
        print(f"\n💡 Kreye {config_file} ak estrikti sa a / Create {config_file} with this structure:")
        print("""
{
  "books": [
    {
      "name": "book1",
      "input_pdf": "input/book1.pdf",
      "metadata": {
        "title": "Book Title",
        "author": "Author Name"
      }
    }
  ]
}
        """)
        sys.exit(1)
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    return config.get('books', [])


def main():
    """Main function"""
    
    print("="*60)
    print("🚀 BATCH PROCESSOR - Traitement Multiple")
    print("="*60)
    
    # Check bucket
    bucket = os.getenv("GCS_BUCKET_NAME")
    if not bucket:
        print("\n❌ GCS_BUCKET_NAME pa defini / not defined")
        print("   Defini l ak / Set it with:")
        print("   export GCS_BUCKET_NAME=your-bucket-name")
        sys.exit(1)
    
    print(f"✅ Bucket: {bucket}")
    
    # Load books configuration
    print(f"\n📚 Chajman konfigirasyon / Loading configuration...")
    books = load_books_config()
    
    if not books:
        print("❌ Pa gen liv nan config / No books in config")
        sys.exit(1)
    
    print(f"✅ {len(books)} liv jwenn / books found")
    
    # Show books
    print(f"\n📖 Liv pou trete / Books to process:")
    for i, book in enumerate(books, 1):
        print(f"   {i}. {book['name']} - {book.get('metadata', {}).get('title', 'No title')}")
    
    # Confirm
    response = input("\n❓ Kontinye? / Continue? (y/n): ")
    if response.lower() != 'y':
        print("❌ Anile / Cancelled")
        sys.exit(0)
    
    # Process batch
    print(f"\n{'='*60}")
    processor = BatchProcessor(bucket)
    results = processor.process_batch(books)
    
    print("\n🎉 Tout fini! / All done!")


if __name__ == "__main__":
    main()

