#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Metadata Manager - Jesyon metadone pou liv yo
Manage metadata for books
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from google.cloud import storage


class MetadataManager:
    """Klas pou jere metadone / Class for managing metadata"""
    
    def __init__(self, bucket_name: Optional[str] = None):
        """
        Initialize metadata manager
        
        Args:
            bucket_name: GCS bucket name (optional)
        """
        self.bucket_name = bucket_name or os.getenv("GCS_BUCKET_NAME")
        self.local_metadata_dir = Path("output/metadata")
        self.local_metadata_dir.mkdir(parents=True, exist_ok=True)
    
    def create_metadata(
        self,
        book_name: str,
        title: str,
        author: str,
        **kwargs
    ) -> Dict:
        """
        Kreye metadone pou yon liv / Create metadata for a book
        
        Args:
            book_name: Unique book identifier
            title: Book title
            author: Author name
            **kwargs: Additional metadata fields
        
        Returns:
            Metadata dictionary
        """
        metadata = {
            'book_name': book_name,
            'title': title,
            'author': author,
            'created_at': datetime.now().isoformat(),
            'version': '1.0',
            'language': {
                'source': kwargs.get('source_language', 'fr'),
                'target': kwargs.get('target_language', 'ht')
            },
            'files': {},
            'processing': {
                'status': 'pending',
                'steps_completed': [],
                'errors': []
            },
            'statistics': {},
            'custom_fields': {}
        }
        
        # Add any additional fields
        for key, value in kwargs.items():
            if key not in ['source_language', 'target_language']:
                metadata['custom_fields'][key] = value
        
        return metadata
    
    def save_metadata(self, metadata: Dict, book_name: str) -> Path:
        """
        Sove metadone lokalman / Save metadata locally
        
        Args:
            metadata: Metadata dictionary
            book_name: Book name
        
        Returns:
            Path to saved metadata file
        """
        metadata_file = self.local_metadata_dir / f"{book_name}_metadata.json"
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Metadone sove / Metadata saved: {metadata_file}")
        return metadata_file
    
    def load_metadata(self, book_name: str) -> Optional[Dict]:
        """
        Chaje metadone / Load metadata
        
        Args:
            book_name: Book name
        
        Returns:
            Metadata dictionary or None
        """
        metadata_file = self.local_metadata_dir / f"{book_name}_metadata.json"
        
        if not metadata_file.exists():
            return None
        
        with open(metadata_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def update_metadata(
        self,
        book_name: str,
        updates: Dict
    ) -> Dict:
        """
        Mete metadone ajou / Update metadata
        
        Args:
            book_name: Book name
            updates: Dictionary of fields to update
        
        Returns:
            Updated metadata
        """
        metadata = self.load_metadata(book_name) or {}
        
        # Deep merge
        for key, value in updates.items():
            if isinstance(value, dict) and key in metadata and isinstance(metadata[key], dict):
                metadata[key].update(value)
            else:
                metadata[key] = value
        
        metadata['updated_at'] = datetime.now().isoformat()
        
        self.save_metadata(metadata, book_name)
        return metadata
    
    def add_file_metadata(
        self,
        book_name: str,
        file_type: str,
        file_path: str,
        file_url: Optional[str] = None,
        file_size: Optional[int] = None
    ) -> Dict:
        """
        Ajoute metadone pou yon fichye / Add file metadata
        
        Args:
            book_name: Book name
            file_type: Type of file (text, audio, podcast, etc.)
            file_path: Local file path
            file_url: Public URL (if uploaded)
            file_size: File size in bytes
        
        Returns:
            Updated metadata
        """
        file_path = Path(file_path)
        
        if file_size is None and file_path.exists():
            file_size = file_path.stat().st_size
        
        file_info = {
            'path': str(file_path),
            'url': file_url,
            'size_bytes': file_size,
            'size_mb': round(file_size / (1024 * 1024), 2) if file_size else None,
            'created_at': datetime.now().isoformat()
        }
        
        return self.update_metadata(book_name, {
            'files': {file_type: file_info}
        })
    
    def add_processing_step(
        self,
        book_name: str,
        step_name: str,
        status: str = 'completed',
        details: Optional[Dict] = None
    ) -> Dict:
        """
        Ajoute yon etap pwosesis / Add processing step
        
        Args:
            book_name: Book name
            step_name: Name of the step
            status: Status (completed, failed, etc.)
            details: Additional details
        
        Returns:
            Updated metadata
        """
        metadata = self.load_metadata(book_name) or {}
        
        if 'processing' not in metadata:
            metadata['processing'] = {
                'status': 'in_progress',
                'steps_completed': [],
                'errors': []
            }
        
        step_info = {
            'name': step_name,
            'status': status,
            'timestamp': datetime.now().isoformat()
        }
        
        if details:
            step_info['details'] = details
        
        metadata['processing']['steps_completed'].append(step_info)
        
        # Update overall status
        if status == 'failed':
            metadata['processing']['status'] = 'failed'
        elif all(s['status'] == 'completed' for s in metadata['processing']['steps_completed']):
            metadata['processing']['status'] = 'completed'
        
        return self.update_metadata(book_name, metadata)
    
    def add_statistics(
        self,
        book_name: str,
        stats: Dict
    ) -> Dict:
        """
        Ajoute estatistik / Add statistics
        
        Args:
            book_name: Book name
            stats: Statistics dictionary
        
        Returns:
            Updated metadata
        """
        return self.update_metadata(book_name, {
            'statistics': stats
        })
    
    def upload_metadata_to_gcs(self, book_name: str) -> Optional[str]:
        """
        Upload metadone nan GCS / Upload metadata to GCS
        
        Args:
            book_name: Book name
        
        Returns:
            Public URL or None
        """
        if not self.bucket_name:
            print("⚠️  No bucket configured")
            return None
        
        metadata_file = self.local_metadata_dir / f"{book_name}_metadata.json"
        
        if not metadata_file.exists():
            print(f"❌ Metadata file not found: {metadata_file}")
            return None
        
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            
            remote_path = f"metadata/{book_name}_metadata.json"
            blob = bucket.blob(remote_path)
            
            blob.upload_from_filename(str(metadata_file))
            
            # Set content type
            blob.content_type = 'application/json'
            blob.patch()
            
            # Make public
            blob.make_public()
            
            url = blob.public_url
            print(f"✅ Metadata uploaded: {url}")
            
            # Update metadata with its own URL
            self.update_metadata(book_name, {
                'metadata_url': url
            })
            
            return url
            
        except Exception as e:
            print(f"❌ Error uploading metadata: {e}")
            return None
    
    def get_all_metadata(self) -> List[Dict]:
        """
        Jwenn tout metadone / Get all metadata
        
        Returns:
            List of all metadata dictionaries
        """
        all_metadata = []
        
        for metadata_file in self.local_metadata_dir.glob("*_metadata.json"):
            with open(metadata_file, 'r', encoding='utf-8') as f:
                all_metadata.append(json.load(f))
        
        return all_metadata
    
    def search_metadata(
        self,
        author: Optional[str] = None,
        title: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict]:
        """
        Chèche metadone / Search metadata
        
        Args:
            author: Filter by author
            title: Filter by title (partial match)
            status: Filter by processing status
        
        Returns:
            List of matching metadata
        """
        all_metadata = self.get_all_metadata()
        results = []
        
        for metadata in all_metadata:
            match = True
            
            if author and metadata.get('author', '').lower() != author.lower():
                match = False
            
            if title and title.lower() not in metadata.get('title', '').lower():
                match = False
            
            if status and metadata.get('processing', {}).get('status') != status:
                match = False
            
            if match:
                results.append(metadata)
        
        return results
    
    def generate_metadata_report(self, book_name: str) -> str:
        """
        Jenere rapò metadone / Generate metadata report
        
        Args:
            book_name: Book name
        
        Returns:
            Formatted report string
        """
        metadata = self.load_metadata(book_name)
        
        if not metadata:
            return f"❌ No metadata found for: {book_name}"
        
        report = f"""
╔══════════════════════════════════════════════════════════╗
║                  METADATA REPORT                         ║
║                  RAPÒ METADONE                           ║
╚══════════════════════════════════════════════════════════╝

📚 BOOK INFORMATION / ENFÒMASYON LIV
────────────────────────────────────────────────────────────
Book Name:    {metadata.get('book_name')}
Title:        {metadata.get('title')}
Author:       {metadata.get('author')}
Created:      {metadata.get('created_at', 'N/A')[:19]}
Version:      {metadata.get('version', '1.0')}

🌍 LANGUAGE / LANG
────────────────────────────────────────────────────────────
Source:       {metadata.get('language', {}).get('source', 'N/A')}
Target:       {metadata.get('language', {}).get('target', 'N/A')}

📁 FILES / FICHYE
────────────────────────────────────────────────────────────
"""
        
        files = metadata.get('files', {})
        for file_type, file_info in files.items():
            report += f"\n{file_type.upper()}:\n"
            report += f"  Path: {file_info.get('path', 'N/A')}\n"
            report += f"  Size: {file_info.get('size_mb', 'N/A')} MB\n"
            if file_info.get('url'):
                report += f"  URL:  {file_info['url']}\n"
        
        report += f"""
⚙️  PROCESSING / PWOSESIS
────────────────────────────────────────────────────────────
Status: {metadata.get('processing', {}).get('status', 'N/A')}

Steps Completed:
"""
        
        for step in metadata.get('processing', {}).get('steps_completed', []):
            status_icon = "✅" if step['status'] == 'completed' else "❌"
            report += f"  {status_icon} {step['name']} ({step['timestamp'][:19]})\n"
        
        if metadata.get('statistics'):
            report += f"""
📊 STATISTICS / ESTATISTIK
────────────────────────────────────────────────────────────
"""
            for key, value in metadata['statistics'].items():
                report += f"  {key}: {value}\n"
        
        report += "\n" + "="*60 + "\n"
        
        return report


# For testing
if __name__ == "__main__":
    manager = MetadataManager()
    
    # Example: Create metadata
    metadata = manager.create_metadata(
        book_name="test_book",
        title="Test Book Title",
        author="Test Author",
        year=2024,
        genre="Fiction"
    )
    
    manager.save_metadata(metadata, "test_book")
    
    # Add processing steps
    manager.add_processing_step("test_book", "extraction", "completed")
    manager.add_processing_step("test_book", "translation", "completed")
    
    # Add file metadata
    manager.add_file_metadata(
        "test_book",
        "text",
        "output/test_book/text.txt",
        "https://example.com/text.txt",
        1024
    )
    
    # Generate report
    print(manager.generate_metadata_report("test_book"))

