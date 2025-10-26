#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Extractor Module
Extract text from various file formats (PDF, TXT, DOCX)
"""

import logging
from pathlib import Path
from typing import Optional
from pypdf import PdfReader
from pypdf.errors import PdfReadError

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

from .config import Config


logger = logging.getLogger('KreyolAI.TextExtractor')


class TextExtractor:
    """
    Klas pou ekstrè tèks nan divès fòma / 
    Class for extracting text from various formats
    """
    
    def __init__(self, config: Config):
        """
        Initialize text extractor
        
        Args:
            config: Configuration object
        """
        self.config = config
        logger.info("Text Extractor initialized")
    
    def detect_format(self, file_path: Path) -> str:
        """
        Detekte fòma fichye / Detect file format
        
        Args:
            file_path: Path to file
        
        Returns:
            Format string: 'pdf', 'txt', 'docx', or 'unknown'
        """
        suffix = file_path.suffix.lower()
        
        if suffix == '.pdf':
            return 'pdf'
        elif suffix in ['.txt', '.text']:
            return 'txt'
        elif suffix in ['.docx', '.doc']:
            return 'docx'
        else:
            return 'unknown'
    
    def extract(self, file_path: Path, file_format: Optional[str] = None) -> str:
        """
        Ekstrè tèks selon fòma / Extract text based on format
        
        Args:
            file_path: Path to file
            file_format: Format override (auto-detect if None)
        
        Returns:
            Extracted text
        
        Raises:
            ValueError: If format is not supported
            FileNotFoundError: If file doesn't exist
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Fichye pa jwenn / File not found: {file_path}")
        
        # Auto-detect format if not provided
        if file_format is None:
            file_format = self.detect_format(file_path)
        
        logger.info(f"Extracting text from {file_format}: {file_path}")
        
        # Extract based on format
        if file_format == 'pdf':
            return self._extract_pdf(file_path)
        elif file_format == 'txt':
            return self._extract_txt(file_path)
        elif file_format == 'docx':
            return self._extract_docx(file_path)
        else:
            raise ValueError(
                f"Fòma pa sipòte / Format not supported: {file_format}\n"
                f"Sipòte: PDF, TXT, DOCX"
            )
    
    def _extract_pdf(self, file_path: Path) -> str:
        """Extract text from PDF"""
        try:
            reader = PdfReader(str(file_path))
            text = ""
            
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
            
            return text.strip()
            
        except PdfReadError as e:
            raise ValueError(f"PDF koronpi / PDF corrupted: {e}")
    
    def _extract_txt(self, file_path: Path) -> str:
        """Extract text from TXT file"""
        try:
            # Try different encodings
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        return f.read()
                except UnicodeDecodeError:
                    continue
            
            raise ValueError("Pa ka li fichye / Cannot read file with supported encodings")
            
        except Exception as e:
            raise ValueError(f"Erè lekti TXT / TXT read error: {e}")
    
    def _extract_docx(self, file_path: Path) -> str:
        """Extract text from DOCX file"""
        if not DOCX_AVAILABLE:
            raise ValueError(
                "python-docx pa enstale / python-docx not installed\n"
                "Enstale: pip install python-docx"
            )
        
        try:
            doc = Document(file_path)
            text = ""
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text += paragraph.text + "\n\n"
            
            return text.strip()
            
        except Exception as e:
            raise ValueError(f"Erè lekti DOCX / DOCX read error: {e}")
    
    def extract_and_save(
        self,
        file_path: Path,
        output_path: Optional[Path] = None,
        file_format: Optional[str] = None
    ) -> str:
        """
        Extract text and save to file
        
        Args:
            file_path: Path to input file
            output_path: Output file path (default: config.output_text_path)
            file_format: Format override
        
        Returns:
            Extracted text
        """
        text = self.extract(file_path, file_format=file_format)
        
        # Validate text
        if not text or len(text.strip()) < 50:
            raise ValueError(
                f"Tèks twò kout / Text too short: {len(text)} characters"
            )
        
        # Save to file
        if output_path is None:
            output_path = self.config.output_text_path
        
        output_path = Path(output_path)
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        logger.info(f"Text saved to: {output_path}")
        print(f"✅ Tèks sove nan / Text saved to: {output_path}")
        print(f"   📊 Total karaktè / characters: {len(text)}")
        
        return text
    
    def get_file_info(self, file_path: Path) -> dict:
        """
        Get file information
        
        Args:
            file_path: Path to file
        
        Returns:
            Dictionary with file info
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            return {'exists': False}
        
        try:
            file_format = self.detect_format(file_path)
            size_mb = file_path.stat().st_size / (1024 * 1024)
            
            return {
                'path': str(file_path),
                'name': file_path.name,
                'format': file_format,
                'size_mb': round(size_mb, 2),
                'exists': True,
            }
        except Exception as e:
            logger.warning(f"Could not get file info: {e}")
            return {'exists': False}

