#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translator Module with Caching
Translate text to Haitian Creole with intelligent caching
"""

import hashlib
import json
import logging
from pathlib import Path
from typing import Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed
from transformers import pipeline
from langdetect import detect, LangDetectException
from tqdm import tqdm

from .config import Config
from .utils import smart_chunk_text


logger = logging.getLogger('KreyolAI.Translator')


class TranslationCache:
    """Sistèm cache pou tradiksyon / Translation cache system"""
    
    def __init__(self, cache_dir: Path):
        """
        Initialize cache
        
        Args:
            cache_dir: Directory for cache files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.hits = 0
        self.misses = 0
        logger.info(f"Translation cache initialized: {cache_dir}")
    
    def _get_cache_key(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """Generate unique cache key"""
        content = f"{text}_{src_lang}_{tgt_lang}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def get(self, text: str, src_lang: str, tgt_lang: str) -> Optional[str]:
        """
        Get translation from cache
        
        Args:
            text: Source text
            src_lang: Source language
            tgt_lang: Target language
        
        Returns:
            Cached translation or None
        """
        cache_key = self._get_cache_key(text, src_lang, tgt_lang)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.hits += 1
                logger.debug(f"Cache hit: {cache_key[:8]}...")
                return data['translation']
            except Exception as e:
                logger.warning(f"Cache read error: {e}")
                return None
        
        self.misses += 1
        return None
    
    def set(self, text: str, translation: str, src_lang: str, tgt_lang: str) -> None:
        """
        Save translation to cache
        
        Args:
            text: Source text
            translation: Translated text
            src_lang: Source language
            tgt_lang: Target language
        """
        cache_key = self._get_cache_key(text, src_lang, tgt_lang)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            data = {
                'text': text[:200],  # Store only preview
                'translation': translation,
                'src_lang': src_lang,
                'tgt_lang': tgt_lang,
                'length': len(text),
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.debug(f"Cache saved: {cache_key[:8]}...")
        except Exception as e:
            logger.warning(f"Cache write error: {e}")
    
    def clear(self) -> int:
        """Clear all cache files"""
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
            count += 1
        logger.info(f"Cache cleared: {count} files removed")
        return count
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'files': len(cache_files),
            'size_mb': total_size / (1024 * 1024),
        }


class CreoleTranslator:
    """Klas pou tradui an Kreyòl / Class for Creole translation"""
    
    def __init__(self, config: Config):
        """
        Initialize translator
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.translator = None  # Lazy loading
        self.cache = TranslationCache(config.cache_dir) if config.enable_cache else None
        logger.info(f"Translator initialized (cache: {config.enable_cache})")
    
    def _load_model(self) -> None:
        """Load translation model (lazy loading)"""
        if self.translator is None:
            logger.info(f"Loading translation model: {self.config.translation_model}")
            print(f"🧠 Ap chaje modèl / Loading model: {self.config.translation_model}")
            self.translator = pipeline("translation", model=self.config.translation_model)
            logger.info("Model loaded successfully")
    
    def detect_language(self, text: str) -> str:
        """
        Detekte lang / Detect language
        
        Args:
            text: Text to analyze
        
        Returns:
            Language code (e.g., 'fr', 'en')
        """
        try:
            # Use first 500 chars for detection
            sample = text[:500]
            lang = detect(sample)
            logger.info(f"Detected language: {lang}")
            return lang
        except LangDetectException:
            logger.warning("Language detection failed, assuming French")
            return self.config.source_language or "fr"
    
    def translate_chunk(
        self,
        chunk: str,
        src_lang: str,
        use_cache: bool = True
    ) -> str:
        """
        Translate a single chunk
        
        Args:
            chunk: Text chunk to translate
            src_lang: Source language
            use_cache: Use cache if available
        
        Returns:
            Translated text
        """
        # Check cache first
        if use_cache and self.cache:
            cached = self.cache.get(chunk, src_lang, self.config.target_language)
            if cached:
                return cached
        
        # Translate
        self._load_model()
        
        try:
            result = self.translator(
                chunk,
                src_lang=src_lang,
                tgt_lang=self.config.target_language
            )
            translation = result[0]['translation_text']
            
            # Save to cache
            if use_cache and self.cache:
                self.cache.set(chunk, translation, src_lang, self.config.target_language)
            
            return translation
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            # Return original on error
            return chunk
    
    def translate(
        self,
        text: str,
        src_lang: Optional[str] = None,
        show_progress: bool = True
    ) -> str:
        """
        Tradui tèks / Translate text
        
        Args:
            text: Text to translate
            src_lang: Source language (auto-detect if None)
            show_progress: Show progress bar
        
        Returns:
            Translated text
        """
        if not text or not text.strip():
            raise ValueError("Text is empty")
        
        # Detect language if not provided
        if src_lang is None:
            src_lang = self.detect_language(text)
        
        print(f"🌍 Lang / Language: {src_lang} → {self.config.target_language}")
        logger.info(f"Translation: {src_lang} → {self.config.target_language}")
        
        # Chunk text
        chunks = smart_chunk_text(text, max_size=self.config.chunk_size)
        print(f"  📊 {len(chunks)} moso / chunks")
        logger.info(f"Split into {len(chunks)} chunks")
        
        # Translate with parallel processing if enabled
        if self.config.enable_parallel and len(chunks) > 3:
            translated = self._translate_parallel(chunks, src_lang, show_progress)
        else:
            translated = self._translate_sequential(chunks, src_lang, show_progress)
        
        result = "\n\n".join(translated)
        
        # Show cache stats
        if self.cache:
            stats = self.cache.get_stats()
            logger.info(f"Cache stats: {stats['hits']} hits, {stats['misses']} misses ({stats['hit_rate']:.1f}%)")
            print(f"  💾 Cache: {stats['hits']} hits, {stats['misses']} misses ({stats['hit_rate']:.1f}%)")
        
        logger.info(f"Translation completed: {len(result)} characters")
        return result
    
    def _translate_sequential(
        self,
        chunks: List[str],
        src_lang: str,
        show_progress: bool
    ) -> List[str]:
        """Translate chunks sequentially"""
        translated = []
        iterator = tqdm(chunks, desc="Tradiksyon", disable=not show_progress)
        
        for chunk in iterator:
            trans = self.translate_chunk(chunk, src_lang)
            translated.append(trans)
        
        return translated
    
    def _translate_parallel(
        self,
        chunks: List[str],
        src_lang: str,
        show_progress: bool
    ) -> List[str]:
        """Translate chunks in parallel"""
        logger.info(f"Parallel translation with {self.config.max_workers} workers")
        print(f"  ⚡ Tradiksyon paralèl / Parallel translation ({self.config.max_workers} workers)")
        
        translated = [None] * len(chunks)
        
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            # Submit all tasks
            future_to_idx = {
                executor.submit(self.translate_chunk, chunk, src_lang): i
                for i, chunk in enumerate(chunks)
            }
            
            # Process results with progress bar
            iterator = tqdm(
                as_completed(future_to_idx),
                total=len(chunks),
                desc="Tradiksyon paralèl",
                disable=not show_progress
            )
            
            for future in iterator:
                idx = future_to_idx[future]
                try:
                    translated[idx] = future.result()
                except Exception as e:
                    logger.error(f"Chunk {idx} failed: {e}")
                    translated[idx] = chunks[idx]  # Fallback to original
        
        return translated
    
    def translate_and_save(
        self,
        text: str,
        output_path: Optional[Path] = None,
        src_lang: Optional[str] = None,
        show_progress: bool = True
    ) -> str:
        """
        Translate text and save to file
        
        Args:
            text: Text to translate
            output_path: Output file path
            src_lang: Source language
            show_progress: Show progress bar
        
        Returns:
            Translated text
        """
        translated = self.translate(text, src_lang=src_lang, show_progress=show_progress)
        
        # Save to file
        if output_path is None:
            output_path = self.config.output_translation_path
        
        output_path = Path(output_path)
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated)
        
        logger.info(f"Translation saved to: {output_path}")
        print(f"✅ Tradiksyon sove nan / Translation saved to: {output_path}")
        
        return translated

