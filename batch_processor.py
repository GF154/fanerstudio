#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Processor - Trete plizyè liv an menm tan
Process multiple books at once
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from utils.cloud_storage import upload_to_gcs, download_from_gcs
from utils.text_extraction import extract_text_from_pdf
from utils.translate import translate_text
from utils.audio_gen import generate_audio
from utils.podcast_mix import mix_voices
from utils.email_notifier import EmailNotifier


class BatchProcessor:
    """Klas pou trete plizyè liv / Class for batch processing"""
    
    def __init__(self, bucket_name: str, enable_email: bool = True):
        self.bucket = bucket_name
        self.results = []
        self.start_time = None
        self.end_time = None
        self.email_notifier = EmailNotifier() if enable_email else None
    
    def process_book(self, book_config: Dict) -> Dict:
        """
        Trete yon liv / Process one book
        
        Args:
            book_config: {
                'name': 'book_name',
                'input_pdf': 'path/to/input.pdf',
                'metadata': {'author': '', 'title': '', ...}
            }
        
        Returns:
            Dict with results and URLs
        """
        book_name = book_config['name']
        input_pdf = book_config['input_pdf']
        
        print(f"\n{'='*60}")
        print(f"📚 Trete liv / Processing: {book_name}")
        print(f"{'='*60}")
        
        result = {
            'name': book_name,
            'status': 'processing',
            'start_time': datetime.now().isoformat(),
            'urls': {},
            'errors': []
        }
        
        try:
            # Create book-specific output directory
            output_dir = Path(f"output/{book_name}")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 1. Download PDF
            print(f"\n📥 1. Telechajman PDF / Downloading PDF...")
            local_pdf = f"input/{book_name}.pdf"
            Path("input").mkdir(exist_ok=True)
            
            try:
                download_from_gcs(input_pdf, local_pdf, self.bucket)
            except Exception as e:
                result['errors'].append(f"Download error: {e}")
                result['status'] = 'failed'
                return result
            
            # 2. Extract text
            print(f"\n📄 2. Ekstraksyon tèks / Extracting text...")
            try:
                text = extract_text_from_pdf(local_pdf)
                print(f"✅ Ekstré {len(text)} karaktè / Extracted {len(text)} characters")
            except Exception as e:
                result['errors'].append(f"Extraction error: {e}")
                result['status'] = 'failed'
                return result
            
            # 3. Translate
            print(f"\n🌍 3. Tradiksyon / Translation...")
            try:
                translated = translate_text(text, "ht")
                
                # Save translated text
                txt_path = output_dir / f"{book_name}_kreyol.txt"
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(translated)
                
                # Upload with metadata
                remote_txt = f"output/{book_name}/{book_name}_kreyol.txt"
                url_txt = upload_to_gcs(str(txt_path), remote_txt, self.bucket)
                result['urls']['text'] = url_txt
                
            except Exception as e:
                result['errors'].append(f"Translation error: {e}")
                result['status'] = 'partial'
            
            # 4. Generate audiobook
            print(f"\n🎧 4. Kreyasyon audiobook / Creating audiobook...")
            try:
                audio_path = output_dir / f"{book_name}_audio.mp3"
                generate_audio(translated, str(audio_path), language="ht")
                
                # Upload
                remote_audio = f"output/{book_name}/{book_name}_audio.mp3"
                url_audio = upload_to_gcs(str(audio_path), remote_audio, self.bucket)
                result['urls']['audio'] = url_audio
                
            except Exception as e:
                result['errors'].append(f"Audio error: {e}")
                result['status'] = 'partial'
            
            # 5. Create podcast
            print(f"\n🎙️ 5. Kreyasyon podcast / Creating podcast...")
            try:
                podcast_path = output_dir / f"{book_name}_podcast.mp3"
                mix_voices([str(audio_path)], str(podcast_path))
                
                # Upload
                remote_podcast = f"output/{book_name}/{book_name}_podcast.mp3"
                url_podcast = upload_to_gcs(str(podcast_path), remote_podcast, self.bucket)
                result['urls']['podcast'] = url_podcast
                
            except Exception as e:
                result['errors'].append(f"Podcast error: {e}")
                result['status'] = 'partial'
            
            # Mark as complete if no errors
            if not result['errors']:
                result['status'] = 'completed'
            
            result['end_time'] = datetime.now().isoformat()
            
            # Print results
            print(f"\n✅ Fini avèk liv: {book_name}")
            if result['urls']:
                print(f"\n🔗 Lyen pou {book_name}:")
                for key, url in result['urls'].items():
                    print(f"   {key}: {url}")
                
                # Send email notification for completed book
                if self.email_notifier and self.email_notifier.enabled:
                    print(f"\n📧 Voye notifikasyon / Sending notification...")
                    self.email_notifier.notify_book_complete(book_name, result['urls'])
            
            return result
            
        except Exception as e:
            result['errors'].append(f"Unexpected error: {e}")
            result['status'] = 'failed'
            result['end_time'] = datetime.now().isoformat()
            return result
    
    def process_batch(self, books: List[Dict]) -> List[Dict]:
        """
        Trete plizyè liv / Process multiple books
        
        Args:
            books: List of book configs
        
        Returns:
            List of results
        """
        self.start_time = datetime.now()
        print(f"\n{'='*60}")
        print(f"🚀 BATCH PROCESSING - {len(books)} LIV")
        print(f"{'='*60}")
        
        for i, book in enumerate(books, 1):
            print(f"\n📖 Liv {i}/{len(books)}")
            result = self.process_book(book)
            self.results.append(result)
        
        self.end_time = datetime.now()
        
        # Save results
        self.save_results()
        
        # Print summary
        self.print_summary()
        
        return self.results
    
    def save_results(self):
        """Sove rezilta yo / Save results"""
        results_dir = Path("output/batch_results")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = results_dir / f"batch_results_{timestamp}.json"
        
        batch_data = {
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'duration_seconds': (self.end_time - self.start_time).total_seconds(),
            'total_books': len(self.results),
            'completed': len([r for r in self.results if r['status'] == 'completed']),
            'partial': len([r for r in self.results if r['status'] == 'partial']),
            'failed': len([r for r in self.results if r['status'] == 'failed']),
            'results': self.results
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(batch_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Rezilta sove nan / Results saved to: {results_file}")
        
        # Upload to GCS
        try:
            upload_to_gcs(
                str(results_file),
                f"batch_results/batch_results_{timestamp}.json",
                self.bucket,
                make_public=False
            )
        except Exception as e:
            print(f"⚠️  Could not upload results: {e}")
    
    def print_summary(self):
        """Afiche rezime / Print summary"""
        duration = (self.end_time - self.start_time).total_seconds()
        
        completed = [r for r in self.results if r['status'] == 'completed']
        partial = [r for r in self.results if r['status'] == 'partial']
        failed = [r for r in self.results if r['status'] == 'failed']
        
        print(f"\n{'='*60}")
        print(f"📊 REZIME BATCH / BATCH SUMMARY")
        print(f"{'='*60}")
        print(f"⏱️  Dire / Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
        print(f"📚 Total liv / Total books: {len(self.results)}")
        print(f"✅ Konple / Completed: {len(completed)}")
        print(f"⚠️  Pasyèl / Partial: {len(partial)}")
        print(f"❌ Echwe / Failed: {len(failed)}")
        
        if completed:
            print(f"\n✅ Liv konple / Completed books:")
            for r in completed:
                print(f"   • {r['name']}")
                if r['urls']:
                    for key, url in r['urls'].items():
                        print(f"     - {key}: {url}")
        
        if partial:
            print(f"\n⚠️  Liv pasyèl / Partial books:")
            for r in partial:
                print(f"   • {r['name']}")
                print(f"     Errors: {', '.join(r['errors'])}")
        
        if failed:
            print(f"\n❌ Liv echwe / Failed books:")
            for r in failed:
                print(f"   • {r['name']}")
                print(f"     Errors: {', '.join(r['errors'])}")
        
        print(f"{'='*60}")
        
        # Send batch completion email
        if self.email_notifier and self.email_notifier.enabled:
            print(f"\n📧 Voye notifikasyon batch / Sending batch notification...")
            self.email_notifier.notify_batch_complete(self.results, duration)


def main():
    """Main function"""
    
    # Check bucket
    bucket = os.getenv("GCS_BUCKET_NAME")
    if not bucket:
        print("❌ GCS_BUCKET_NAME pa defini / not defined")
        exit(1)
    
    # Example: Define books to process
    books = [
        {
            'name': 'liv1',
            'input_pdf': 'input/liv1.pdf',
            'metadata': {
                'title': 'Premye Liv',
                'author': 'Unknown',
                'language': 'fr'
            }
        },
        {
            'name': 'liv2',
            'input_pdf': 'input/liv2.pdf',
            'metadata': {
                'title': 'Dezyèm Liv',
                'author': 'Unknown',
                'language': 'fr'
            }
        },
        # Add more books here...
    ]
    
    # Process batch
    processor = BatchProcessor(bucket)
    results = processor.process_batch(books)
    
    print("\n🎉 Batch processing fini / completed!")


if __name__ == "__main__":
    main()

