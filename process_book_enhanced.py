#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Book Processor - Pwosesis amelyore ak tout fonksyonalite
Enhanced processing with all features: metadata, notifications, cloud storage
"""

import os
from pathlib import Path
from datetime import datetime
from utils.cloud_storage import upload_to_gcs, download_from_gcs
from utils.text_extraction import extract_text_from_pdf
from utils.translate import translate_text
from utils.audio_gen import generate_audio
from utils.podcast_mix import mix_voices
from utils.metadata_manager import MetadataManager
from utils.email_notifier import EmailNotifier


class EnhancedBookProcessor:
    """Klas amelyore pou trete liv / Enhanced class for book processing"""
    
    def __init__(self, bucket_name: str):
        """Initialize processor"""
        self.bucket = bucket_name
        self.metadata_manager = MetadataManager(bucket_name)
        self.email_notifier = EmailNotifier()
        
        # Create directories
        Path("input").mkdir(exist_ok=True)
        Path("output").mkdir(exist_ok=True)
    
    def process_book(
        self,
        book_name: str,
        input_pdf_remote: str,
        title: str,
        author: str,
        **kwargs
    ) -> dict:
        """
        Trete yon liv konplètman / Process a book completely
        
        Args:
            book_name: Unique book identifier
            input_pdf_remote: Remote path to PDF in GCS
            title: Book title
            author: Author name
            **kwargs: Additional metadata
        
        Returns:
            Processing results dictionary
        """
        
        print("=" * 60)
        print(f"🚀 PWOSESIS LIV / PROCESSING BOOK: {book_name}")
        print("=" * 60)
        
        start_time = datetime.now()
        
        # 1. Create metadata
        print("\n📝 Kreyasyon metadone / Creating metadata...")
        metadata = self.metadata_manager.create_metadata(
            book_name=book_name,
            title=title,
            author=author,
            **kwargs
        )
        self.metadata_manager.save_metadata(metadata, book_name)
        
        results = {
            'book_name': book_name,
            'status': 'processing',
            'start_time': start_time.isoformat(),
            'urls': {},
            'errors': []
        }
        
        try:
            # 2. Download PDF
            print("\n📥 ETAP 1: Telechajman PDF / Downloading PDF")
            print("-" * 60)
            
            local_pdf = f"input/{book_name}.pdf"
            download_from_gcs(input_pdf_remote, local_pdf, self.bucket)
            
            self.metadata_manager.add_processing_step(
                book_name, "download", "completed",
                {'remote_path': input_pdf_remote}
            )
            
            # 3. Extract text
            print("\n📄 ETAP 2: Ekstraksyon tèks / Text extraction")
            print("-" * 60)
            
            text = extract_text_from_pdf(local_pdf)
            
            self.metadata_manager.add_processing_step(
                book_name, "extraction", "completed",
                {'characters': len(text)}
            )
            
            self.metadata_manager.add_statistics(book_name, {
                'original_characters': len(text),
                'original_words': len(text.split())
            })
            
            # 4. Translate
            print("\n🌍 ETAP 3: Tradiksyon / Translation")
            print("-" * 60)
            
            translated = translate_text(text, "ht")
            
            # Save and upload translation
            output_dir = Path(f"output/{book_name}")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            txt_path = output_dir / f"{book_name}_kreyol.txt"
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(translated)
            
            remote_txt = f"output/{book_name}/{book_name}_kreyol.txt"
            url_txt = upload_to_gcs(str(txt_path), remote_txt, self.bucket)
            results['urls']['text'] = url_txt
            
            self.metadata_manager.add_processing_step(
                book_name, "translation", "completed",
                {'characters': len(translated)}
            )
            
            self.metadata_manager.add_file_metadata(
                book_name, "text", str(txt_path), url_txt
            )
            
            self.metadata_manager.add_statistics(book_name, {
                'translated_characters': len(translated),
                'translated_words': len(translated.split())
            })
            
            # 5. Generate audiobook
            print("\n🎧 ETAP 4: Kreyasyon audiobook / Audiobook generation")
            print("-" * 60)
            
            audio_path = output_dir / f"{book_name}_audio.mp3"
            generate_audio(translated, str(audio_path), language="ht")
            
            remote_audio = f"output/{book_name}/{book_name}_audio.mp3"
            url_audio = upload_to_gcs(str(audio_path), remote_audio, self.bucket)
            results['urls']['audio'] = url_audio
            
            self.metadata_manager.add_processing_step(
                book_name, "audio_generation", "completed"
            )
            
            self.metadata_manager.add_file_metadata(
                book_name, "audio", str(audio_path), url_audio
            )
            
            # 6. Create podcast
            print("\n🎙️ ETAP 5: Kreyasyon podcast / Podcast creation")
            print("-" * 60)
            
            podcast_path = output_dir / f"{book_name}_podcast.mp3"
            mix_voices([str(audio_path)], str(podcast_path))
            
            remote_podcast = f"output/{book_name}/{book_name}_podcast.mp3"
            url_podcast = upload_to_gcs(str(podcast_path), remote_podcast, self.bucket)
            results['urls']['podcast'] = url_podcast
            
            self.metadata_manager.add_processing_step(
                book_name, "podcast_creation", "completed"
            )
            
            self.metadata_manager.add_file_metadata(
                book_name, "podcast", str(podcast_path), url_podcast
            )
            
            # 7. Upload metadata
            print("\n☁️ Upload metadone / Uploading metadata...")
            metadata_url = self.metadata_manager.upload_metadata_to_gcs(book_name)
            if metadata_url:
                results['urls']['metadata'] = metadata_url
            
            # Calculate duration
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.metadata_manager.add_statistics(book_name, {
                'processing_duration_seconds': duration,
                'processing_duration_minutes': round(duration / 60, 2)
            })
            
            # Update final status
            results['status'] = 'completed'
            results['end_time'] = end_time.isoformat()
            results['duration'] = duration
            
            # 8. Send notification
            if self.email_notifier.enabled:
                print("\n📧 Voye notifikasyon / Sending notification...")
                self.email_notifier.notify_book_complete(book_name, results['urls'])
            
            # Print summary
            print("\n" + "=" * 60)
            print("🎉 SIKSÈ! / SUCCESS!")
            print("=" * 60)
            print(f"\n📚 Liv: {book_name}")
            print(f"⏱️  Dire / Duration: {duration:.1f}s ({duration/60:.1f} min)")
            print(f"\n🔗 LYEN PIBLIK YO / PUBLIC LINKS:")
            for key, url in results['urls'].items():
                print(f"   {key}: {url}")
            
            # Print metadata report
            print("\n" + self.metadata_manager.generate_metadata_report(book_name))
            
            return results
            
        except Exception as e:
            results['status'] = 'failed'
            results['errors'].append(str(e))
            results['end_time'] = datetime.now().isoformat()
            
            self.metadata_manager.add_processing_step(
                book_name, "error", "failed",
                {'error': str(e)}
            )
            
            if self.email_notifier.enabled:
                self.email_notifier.notify_error(book_name, str(e))
            
            print(f"\n❌ ERÈR / ERROR: {e}")
            
            return results


def main():
    """Main function"""
    
    # Check bucket
    bucket = os.getenv("GCS_BUCKET_NAME")
    if not bucket:
        print("❌ GCS_BUCKET_NAME pa defini / not defined")
        exit(1)
    
    # Create processor
    processor = EnhancedBookProcessor(bucket)
    
    # Example: Process a book
    result = processor.process_book(
        book_name="liv1",
        input_pdf_remote="input/liv1.pdf",
        title="Premye Liv",
        author="Otè Enkonni",
        year=2024,
        genre="Education",
        description="Premye liv nan seri Kreyòl IA"
    )
    
    print("\n✅ Fini! / Done!")


if __name__ == "__main__":
    main()

