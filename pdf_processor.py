#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📄 PDF & Document Processor for Audiobook Generation
Pwosese PDF ak dokiman pou jenere audiobook
"""

import io
import tempfile
import os
from typing import Optional, BinaryIO
from pathlib import Path

# PDF Processing
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️ PyPDF2 not available - install with: pip install PyPDF2")

# DOCX Processing
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    print("⚠️ python-docx not available - install with: pip install python-docx")

# EPUB Processing
try:
    import ebooklib
    from ebooklib import epub
    from bs4 import BeautifulSoup
    EPUB_AVAILABLE = True
except ImportError:
    EPUB_AVAILABLE = False
    print("⚠️ ebooklib not available - install with: pip install ebooklib beautifulsoup4")


class DocumentProcessor:
    """Process various document formats to extract text"""
    
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """
        Extract text from PDF file
        
        Args:
            file_content: PDF file as bytes
            
        Returns:
            Extracted text
        """
        if not PDF_AVAILABLE:
            raise ImportError("PyPDF2 not installed. Install with: pip install PyPDF2")
        
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n\n"
            
            return text.strip()
        
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """
        Extract text from DOCX file
        
        Args:
            file_content: DOCX file as bytes
            
        Returns:
            Extracted text
        """
        if not DOCX_AVAILABLE:
            raise ImportError("python-docx not installed. Install with: pip install python-docx")
        
        try:
            # Save to temp file (python-docx requires file path)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
                tmp_file.write(file_content)
                tmp_path = tmp_file.name
            
            # Extract text
            doc = Document(tmp_path)
            text = "\n\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text])
            
            # Cleanup
            os.unlink(tmp_path)
            
            return text.strip()
        
        except Exception as e:
            raise Exception(f"Error processing DOCX: {str(e)}")
    
    @staticmethod
    def extract_text_from_txt(file_content: bytes) -> str:
        """
        Extract text from TXT file
        
        Args:
            file_content: TXT file as bytes
            
        Returns:
            Extracted text
        """
        try:
            # Try UTF-8 first
            try:
                text = file_content.decode('utf-8')
            except UnicodeDecodeError:
                # Fallback to latin-1
                text = file_content.decode('latin-1')
            
            return text.strip()
        
        except Exception as e:
            raise Exception(f"Error processing TXT: {str(e)}")
    
    @staticmethod
    def extract_text_from_epub(file_content: bytes) -> str:
        """
        Extract text from EPUB file
        
        Args:
            file_content: EPUB file as bytes
            
        Returns:
            Extracted text
        """
        if not EPUB_AVAILABLE:
            raise ImportError("ebooklib not installed. Install with: pip install ebooklib beautifulsoup4")
        
        try:
            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.epub') as tmp_file:
                tmp_file.write(file_content)
                tmp_path = tmp_file.name
            
            # Read EPUB
            book = epub.read_epub(tmp_path)
            
            text = ""
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    content = item.get_content()
                    soup = BeautifulSoup(content, 'html.parser')
                    text += soup.get_text() + "\n\n"
            
            # Cleanup
            os.unlink(tmp_path)
            
            return text.strip()
        
        except Exception as e:
            raise Exception(f"Error processing EPUB: {str(e)}")
    
    @classmethod
    def process_document(cls, file_content: bytes, filename: str) -> str:
        """
        Process document based on file extension
        
        Args:
            file_content: File content as bytes
            filename: Original filename to determine format
            
        Returns:
            Extracted text
        """
        # Get file extension
        ext = Path(filename).suffix.lower()
        
        # Process based on extension
        if ext == '.pdf':
            return cls.extract_text_from_pdf(file_content)
        elif ext == '.docx':
            return cls.extract_text_from_docx(file_content)
        elif ext == '.txt':
            return cls.extract_text_from_txt(file_content)
        elif ext == '.epub':
            return cls.extract_text_from_epub(file_content)
        else:
            raise ValueError(f"Unsupported file format: {ext}. Supported: .pdf, .docx, .txt, .epub")
    
    @staticmethod
    def get_supported_formats():
        """Return list of supported formats with availability"""
        formats = {
            "pdf": PDF_AVAILABLE,
            "docx": DOCX_AVAILABLE,
            "txt": True,  # Always available
            "epub": EPUB_AVAILABLE
        }
        return formats
    
    @staticmethod
    def clean_text(text: str, max_length: Optional[int] = None) -> str:
        """
        Clean extracted text
        
        Args:
            text: Raw extracted text
            max_length: Maximum length (optional)
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = " ".join(text.split())
        
        # Remove special characters that might cause issues
        text = text.replace('\x00', '')
        
        # Truncate if needed
        if max_length and len(text) > max_length:
            text = text[:max_length] + "..."
        
        return text


# Quick test function
if __name__ == "__main__":
    processor = DocumentProcessor()
    
    print("📄 PDF & Document Processor")
    print("=" * 50)
    print("\n✅ Supported formats:")
    for fmt, available in processor.get_supported_formats().items():
        status = "✅" if available else "❌"
        print(f"  {status} .{fmt}")
    
    print("\n💡 Usage:")
    print("  from pdf_processor import DocumentProcessor")
    print('  text = DocumentProcessor.process_document(file_bytes, "file.pdf")')

