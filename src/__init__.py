#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pwojè Kreyòl IA - Modil / Modules
Haitian Creole AI Project - Modules
"""

__version__ = "2.0.0"
__author__ = "Projet Kreyòl IA Team"

from .config import Config
from .pdf_extractor import PDFExtractor
from .text_extractor import TextExtractor
from .translator import CreoleTranslator
from .audio_generator import AudiobookGenerator
from .utils import setup_logging, smart_chunk_text

__all__ = [
    'Config',
    'PDFExtractor',
    'TextExtractor',
    'CreoleTranslator',
    'AudiobookGenerator',
    'setup_logging',
    'smart_chunk_text',
]

