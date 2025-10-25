"""
Simple text extraction wrapper
"""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pdf_extractor import PDFExtractor
from src.config import Config


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Ekstrè tèks nan PDF / Extract text from PDF
    
    Args:
        pdf_path: Path to PDF file
    
    Returns:
        Extracted text
    """
    # Create minimal config
    config = Config()
    extractor = PDFExtractor(config)
    
    # Extract text
    text = extractor.extract(Path(pdf_path), show_progress=True)
    return text

