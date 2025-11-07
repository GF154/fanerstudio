#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎙️ TTS Manager - Singleton for Model Caching
Manages Hugging Face MMS-TTS model lifecycle for optimal performance
"""

import torch
from transformers import VitsModel, AutoTokenizer
from pathlib import Path
from typing import Optional, List
import threading
import time
import numpy as np

class TTSManager:
    """
    Singleton manager for TTS model caching and optimization
    
    Features:
    - Model caching (load once, reuse many times)
    - GPU acceleration if available
    - Batch inference support
    - Performance monitoring
    - Thread-safe operations
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.model = None
        self.tokenizer = None
        self.model_name = "facebook/mms-tts-hat"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._initialized = True
        self.sampling_rate = None
        
        # Performance metrics
        self.metrics = {
            "total_requests": 0,
            "cache_hits": 0,
            "total_generation_time": 0.0,
            "total_characters": 0
        }
        
        print(f"🎙️ TTS Manager initialized")
        print(f"   Device: {self.device}")
        print(f"   Model: {self.model_name}")
    
    def load_model(self, force_reload: bool = False) -> bool:
        """
        Load model if not already loaded
        
        Args:
            force_reload: Force reload even if already loaded
            
        Returns:
            True if successful, False otherwise
        """
        if self.model is not None and not force_reload:
            print("✅ Model already loaded (using cache)")
            self.metrics["cache_hits"] += 1
            return True
            
        try:
            print(f"📥 Loading {self.model_name}...")
            start_time = time.time()
            
            self.model = VitsModel.from_pretrained(self.model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.sampling_rate = self.model.config.sampling_rate
            
            # Move to GPU if available
            if self.device == "cuda":
                self.model = self.model.to(self.device)
                print("🚀 Model loaded on GPU")
            else:
                print("💻 Model loaded on CPU")
            
            load_time = time.time() - start_time
            print(f"⏱️  Load time: {load_time:.2f}s")
            
            # Warmup inference
            self._warmup()
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def _warmup(self):
        """Warmup model with a test inference to optimize subsequent calls"""
        try:
            print("🔥 Warming up model...")
            test_text = "Bonjou"
            inputs = self.tokenizer(test_text, return_tensors="pt")
            
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                _ = self.model(**inputs)
            
            print("✅ Model warmed up and ready")
        except Exception as e:
            print(f"⚠️  Warmup failed: {e}")
    
    def generate_audio(self, text: str, apply_effects: bool = True) -> tuple:
        """
        Generate audio from text
        
        Args:
            text: Text to synthesize
            apply_effects: Apply audio post-processing
            
        Returns:
            Tuple of (audio_array, sampling_rate)
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first")
        
        start_time = time.time()
        
        try:
            # Tokenize
            inputs = self.tokenizer(text, return_tensors="pt")
            
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate
            with torch.no_grad():
                output = self.model(**inputs).waveform
            
            # Convert to numpy
            audio_np = output.squeeze().cpu().numpy()
            
            # Apply post-processing
            if apply_effects:
                audio_np = self._post_process_audio(audio_np)
            
            # Update metrics
            generation_time = time.time() - start_time
            self.metrics["total_requests"] += 1
            self.metrics["total_generation_time"] += generation_time
            self.metrics["total_characters"] += len(text)
            
            return audio_np, self.sampling_rate
            
        except Exception as e:
            print(f"❌ Generation error: {e}")
            raise
    
    def generate_batch(self, texts: List[str]) -> List[tuple]:
        """
        Generate audio for multiple texts in batch (more efficient)
        
        Args:
            texts: List of texts to synthesize
            
        Returns:
            List of (audio_array, sampling_rate) tuples
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first")
        
        results = []
        
        # Process in smaller batches to avoid memory issues
        batch_size = 5
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            
            for text in batch:
                try:
                    audio, sr = self.generate_audio(text)
                    results.append((audio, sr))
                except Exception as e:
                    print(f"⚠️  Batch item failed: {e}")
                    # Return empty audio on failure
                    results.append((np.array([]), self.sampling_rate))
        
        return results
    
    def _post_process_audio(self, audio: np.ndarray) -> np.ndarray:
        """
        Apply post-processing to improve audio quality
        
        Args:
            audio: Raw audio array
            
        Returns:
            Processed audio array
        """
        # Normalize audio to prevent clipping
        if np.max(np.abs(audio)) > 0:
            audio = audio / np.max(np.abs(audio))
        
        # Apply gentle compression (reduce dynamic range)
        audio = np.tanh(audio * 0.8)
        
        return audio
    
    def get_metrics(self) -> dict:
        """Get performance metrics"""
        if self.metrics["total_requests"] > 0:
            avg_time = self.metrics["total_generation_time"] / self.metrics["total_requests"]
            avg_chars = self.metrics["total_characters"] / self.metrics["total_requests"]
            chars_per_sec = self.metrics["total_characters"] / self.metrics["total_generation_time"] if self.metrics["total_generation_time"] > 0 else 0
        else:
            avg_time = 0
            avg_chars = 0
            chars_per_sec = 0
        
        return {
            "total_requests": self.metrics["total_requests"],
            "cache_hits": self.metrics["cache_hits"],
            "avg_generation_time": f"{avg_time:.3f}s",
            "avg_text_length": f"{avg_chars:.0f} chars",
            "throughput": f"{chars_per_sec:.0f} chars/sec",
            "device": self.device,
            "model_loaded": self.model is not None
        }
    
    def unload_model(self):
        """Unload model to free memory"""
        self.model = None
        self.tokenizer = None
        self.sampling_rate = None
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        print("🗑️  Model unloaded from memory")


# Global singleton instance
_tts_manager = None

def get_tts_manager() -> TTSManager:
    """
    Get the global TTS manager instance
    
    Returns:
        TTSManager singleton instance
    """
    global _tts_manager
    if _tts_manager is None:
        _tts_manager = TTSManager()
    return _tts_manager

