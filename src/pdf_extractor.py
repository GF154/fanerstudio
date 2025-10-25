#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Extractor Module
Extract text from PDF files with validation
"""

import logging
from pathlib import Path
from typing import Optional
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from tqdm import tqdm

from .config import Config


logger = logging.getLogger('KreyolAI.PDFExtractor')


class PDFExtractor:
    """Klas pou ekstrè tèks nan PDF / Class for PDF text extraction"""
    
    def __init__(self, config: Config):
        """
        Initialize PDF extractor
        
        Args:
            config: Configuration object
        """
        self.config = config
        logger.info("PDF Extractor initialized")
    
    def validate_pdf(self, pdf_path: Path) -> None:
        """
        Valide fichye PDF / Validate PDF file
        
        Args:
            pdf_path: Path to PDF file
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is invalid or too large
        """
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(
                f"Fichye pa jwenn / File not found: {pdf_path}"
            )
        
        if not pdf_path.suffix.lower() == '.pdf':
            raise ValueError(
                f"Dwe yon fichye PDF / Must be a PDF file: {pdf_path}"
            )
        
        # Check file size
        size_mb = pdf_path.stat().st_size / (1024 * 1024)
        if size_mb > self.config.max_pdf_size_mb:
            raise ValueError(
                f"PDF twò gwo: {size_mb:.1f}MB (max: {self.config.max_pdf_size_mb}MB)\n"
                f"PDF too large: {size_mb:.1f}MB (max: {self.config.max_pdf_size_mb}MB)"
            )
        
        logger.info(f"PDF validated: {pdf_path.name} ({size_mb:.1f}MB)")
    
    def extract(self, pdf_path: Path, show_progress: bool = True) -> str:
        """
        Ekstrè tèks nan PDF / Extract text from PDF
        
        Args:
            pdf_path: Path to PDF file
            show_progress: Show progress bar
        
        Returns:
            Extracted text
        
        Raises:
            PdfReadError: If PDF is corrupted or encrypted
            ValueError: If PDF has too many pages or no text
        """
        try:
            pdf_path = Path(pdf_path)
            logger.info(f"Starting extraction: {pdf_path}")
            
            # Validate first
            self.validate_pdf(pdf_path)
            
            # Read PDF
            reader = PdfReader(str(pdf_path))
            total_pages = len(reader.pages)
            
            # Check page limit
            if total_pages > self.config.max_pdf_pages:
                raise ValueError(
                    f"PDF gen twòp paj: {total_pages} (max: {self.config.max_pdf_pages})\n"
                    f"PDF has too many pages: {total_pages} (max: {self.config.max_pdf_pages})"
                )
            
            logger.info(f"PDF has {total_pages} pages")
            
            # Extract text
            text = ""
            pages = tqdm(reader.pages, desc="Extraction", unit="page", disable=not show_progress)
            
            for i, page in enumerate(pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
                except Exception as e:
                    logger.warning(f"Error extracting page {i}: {e}")
                    continue
            
            # Validate extracted text
            if not text or len(text.strip()) < 50:
                raise ValueError(
                    f"Tèks twò kout oswa vid / Text too short or empty: {len(text)} characters"
                )
            
            logger.info(f"Extraction successful: {len(text)} characters from {total_pages} pages")
            return text.strip()
            
        except PdfReadError as e:
            logger.error(f"PDF read error: {e}")
            raise ValueError(
                f"PDF koronpi oswa pwoteje / PDF corrupted or encrypted: {e}"
            )
        except Exception as e:
            logger.error(f"Extraction error: {e}")
            raise
    
    def extract_and_save(
        self,
        pdf_path: Path,
        output_path: Optional[Path] = None,
        show_progress: bool = True
    ) -> str:
        """
        Extract text and save to file
        
        Args:
            pdf_path: Path to PDF file
            output_path: Output file path (default: config.output_text_path)
            show_progress: Show progress bar
        
        Returns:
            Extracted text
        """
        text = self.extract(pdf_path, show_progress=show_progress)
        
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
    
    def get_pdf_info(self, pdf_path: Path) -> dict:
        """
        Get PDF metadata
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            Dictionary with PDF info
        """
        try:
            reader = PdfReader(str(pdf_path))
            info = {
                'pages': len(reader.pages),
                'size_mb': pdf_path.stat().st_size / (1024 * 1024),
                'encrypted': reader.is_encrypted,
            }
            
            # Try to get metadata
            if reader.metadata:
                info.update({
                    'author': reader.metadata.get('/Author', 'Unknown'),
                    'title': reader.metadata.get('/Title', 'Unknown'),
                    'subject': reader.metadata.get('/Subject', 'Unknown'),
                })
            
            return info
        except Exception as e:
            logger.warning(f"Could not get PDF info: {e}")
            return {}

