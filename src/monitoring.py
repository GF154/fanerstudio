#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitoring Module
Application monitoring and metrics collection
"""

import time
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from functools import wraps
from pathlib import Path
import json


logger = logging.getLogger('KreyolAI.Monitoring')


class PerformanceMonitor:
    """
    Monitor application performance and collect metrics
    """
    
    def __init__(self, metrics_file: str = "metrics.json"):
        """
        Initialize performance monitor
        
        Args:
            metrics_file: File to store metrics
        """
        self.metrics_file = Path(metrics_file)
        self.metrics = {
            "requests": [],
            "translations": [],
            "audio_generations": [],
            "errors": []
        }
        self._load_metrics()
    
    def _load_metrics(self):
        """Load metrics from file"""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    self.metrics = json.load(f)
                logger.info(f"Metrics loaded from {self.metrics_file}")
            except Exception as e:
                logger.warning(f"Could not load metrics: {e}")
    
    def _save_metrics(self):
        """Save metrics to file"""
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save metrics: {e}")
    
    def record_request(
        self,
        endpoint: str,
        method: str,
        status_code: int,
        duration: float,
        user_agent: Optional[str] = None
    ):
        """
        Record API request metrics
        
        Args:
            endpoint: API endpoint
            method: HTTP method
            status_code: Response status code
            duration: Request duration in seconds
            user_agent: User agent string
        """
        metric = {
            "timestamp": datetime.now().isoformat(),
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "duration": duration,
            "user_agent": user_agent
        }
        
        self.metrics["requests"].append(metric)
        
        # Keep only last 1000 requests
        if len(self.metrics["requests"]) > 1000:
            self.metrics["requests"] = self.metrics["requests"][-1000:]
        
        self._save_metrics()
        
        logger.info(f"Request recorded: {method} {endpoint} - {status_code} ({duration:.3f}s)")
    
    def record_translation(
        self,
        text_length: int,
        translation_length: int,
        duration: float,
        source_lang: str,
        target_lang: str,
        cache_hit: bool = False
    ):
        """
        Record translation metrics
        
        Args:
            text_length: Length of input text
            translation_length: Length of translated text
            duration: Translation duration in seconds
            source_lang: Source language code
            target_lang: Target language code
            cache_hit: Whether translation was from cache
        """
        metric = {
            "timestamp": datetime.now().isoformat(),
            "text_length": text_length,
            "translation_length": translation_length,
            "duration": duration,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "cache_hit": cache_hit,
            "chars_per_second": text_length / duration if duration > 0 else 0
        }
        
        self.metrics["translations"].append(metric)
        
        if len(self.metrics["translations"]) > 500:
            self.metrics["translations"] = self.metrics["translations"][-500:]
        
        self._save_metrics()
        
        logger.info(f"Translation recorded: {text_length} chars in {duration:.2f}s (cache_hit={cache_hit})")
    
    def record_audio_generation(
        self,
        text_length: int,
        audio_size_mb: float,
        duration: float,
        language: str
    ):
        """
        Record audio generation metrics
        
        Args:
            text_length: Length of input text
            audio_size_mb: Size of generated audio in MB
            duration: Generation duration in seconds
            language: Audio language code
        """
        metric = {
            "timestamp": datetime.now().isoformat(),
            "text_length": text_length,
            "audio_size_mb": audio_size_mb,
            "duration": duration,
            "language": language
        }
        
        self.metrics["audio_generations"].append(metric)
        
        if len(self.metrics["audio_generations"]) > 500:
            self.metrics["audio_generations"] = self.metrics["audio_generations"][-500:]
        
        self._save_metrics()
        
        logger.info(f"Audio generation recorded: {text_length} chars → {audio_size_mb:.2f}MB in {duration:.2f}s")
    
    def record_error(
        self,
        error_type: str,
        error_message: str,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Record error metrics
        
        Args:
            error_type: Type of error
            error_message: Error message
            context: Additional context
        """
        metric = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "error_message": error_message,
            "context": context
        }
        
        self.metrics["errors"].append(metric)
        
        if len(self.metrics["errors"]) > 500:
            self.metrics["errors"] = self.metrics["errors"][-500:]
        
        self._save_metrics()
        
        logger.error(f"Error recorded: {error_type} - {error_message}")
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get metrics summary
        
        Returns:
            Dictionary with summary statistics
        """
        total_requests = len(self.metrics["requests"])
        total_translations = len(self.metrics["translations"])
        total_audio = len(self.metrics["audio_generations"])
        total_errors = len(self.metrics["errors"])
        
        # Calculate average durations
        avg_request_duration = 0
        if total_requests > 0:
            avg_request_duration = sum(
                r["duration"] for r in self.metrics["requests"]
            ) / total_requests
        
        avg_translation_duration = 0
        if total_translations > 0:
            avg_translation_duration = sum(
                t["duration"] for t in self.metrics["translations"]
            ) / total_translations
        
        avg_audio_duration = 0
        if total_audio > 0:
            avg_audio_duration = sum(
                a["duration"] for a in self.metrics["audio_generations"]
            ) / total_audio
        
        # Cache hit rate
        cache_hits = sum(
            1 for t in self.metrics["translations"] if t.get("cache_hit", False)
        )
        cache_hit_rate = (cache_hits / total_translations * 100) if total_translations > 0 else 0
        
        # Recent errors
        recent_errors = self.metrics["errors"][-10:]
        
        return {
            "total_requests": total_requests,
            "total_translations": total_translations,
            "total_audio_generations": total_audio,
            "total_errors": total_errors,
            "avg_request_duration": round(avg_request_duration, 3),
            "avg_translation_duration": round(avg_translation_duration, 3),
            "avg_audio_duration": round(avg_audio_duration, 3),
            "cache_hit_rate": round(cache_hit_rate, 2),
            "recent_errors": recent_errors
        }
    
    def get_uptime_stats(self, start_time: datetime) -> Dict[str, Any]:
        """
        Get uptime statistics
        
        Args:
            start_time: Application start time
        
        Returns:
            Dictionary with uptime stats
        """
        uptime = datetime.now() - start_time
        uptime_seconds = uptime.total_seconds()
        
        uptime_hours = int(uptime_seconds // 3600)
        uptime_minutes = int((uptime_seconds % 3600) // 60)
        uptime_seconds_remaining = int(uptime_seconds % 60)
        
        return {
            "uptime": f"{uptime_hours}h {uptime_minutes}m {uptime_seconds_remaining}s",
            "uptime_seconds": int(uptime_seconds),
            "start_time": start_time.isoformat()
        }
    
    def clear_metrics(self):
        """Clear all metrics"""
        self.metrics = {
            "requests": [],
            "translations": [],
            "audio_generations": [],
            "errors": []
        }
        self._save_metrics()
        logger.info("Metrics cleared")


# Decorator for timing functions
def time_it(metric_type: str = "operation"):
    """
    Decorator to time function execution
    
    Args:
        metric_type: Type of metric to record
    
    Returns:
        Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(f"{func.__name__} completed in {duration:.3f}s")
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"{func.__name__} failed after {duration:.3f}s: {e}")
                raise
        return wrapper
    return decorator


# Global monitor instance
_monitor = None


def get_monitor() -> PerformanceMonitor:
    """Get global monitor instance"""
    global _monitor
    if _monitor is None:
        _monitor = PerformanceMonitor()
    return _monitor

