#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prometheus Metrics Module
Application metrics for monitoring and observability
"""

import time
import logging
from functools import wraps
from typing import Callable
from prometheus_client import (
    Counter, Histogram, Gauge, Info,
    generate_latest, CONTENT_TYPE_LATEST
)
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger('KreyolAI.Metrics')


# ============================================================
# METRICS DEFINITIONS
# ============================================================

# Request metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

REQUEST_IN_PROGRESS = Gauge(
    'http_requests_in_progress',
    'HTTP requests currently being processed',
    ['method', 'endpoint']
)

# Translation metrics
TRANSLATION_COUNT = Counter(
    'translations_total',
    'Total translations performed',
    ['source_lang', 'target_lang', 'status']
)

TRANSLATION_DURATION = Histogram(
    'translation_duration_seconds',
    'Translation processing time',
    ['source_lang', 'target_lang']
)

TRANSLATION_CHARS = Histogram(
    'translation_characters',
    'Number of characters translated',
    buckets=[100, 500, 1000, 5000, 10000, 50000, 100000]
)

# Audio generation metrics
AUDIO_GENERATION_COUNT = Counter(
    'audio_generations_total',
    'Total audio generations',
    ['voice_type', 'status']
)

AUDIO_GENERATION_DURATION = Histogram(
    'audio_generation_duration_seconds',
    'Audio generation time'
)

AUDIO_DURATION_SECONDS = Histogram(
    'audio_output_duration_seconds',
    'Duration of generated audio in seconds',
    buckets=[10, 30, 60, 120, 300, 600, 1800, 3600]
)

# File processing metrics
FILE_UPLOAD_SIZE = Histogram(
    'file_upload_size_bytes',
    'Size of uploaded files',
    buckets=[1024, 10240, 102400, 1048576, 10485760, 52428800]
)

FILE_PROCESSING_DURATION = Histogram(
    'file_processing_duration_seconds',
    'File processing time',
    ['file_type']
)

PDF_PAGES_PROCESSED = Histogram(
    'pdf_pages_processed',
    'Number of pages in processed PDFs',
    buckets=[1, 5, 10, 20, 50, 100, 200, 500]
)

# Cache metrics
CACHE_HITS = Counter(
    'cache_hits_total',
    'Total cache hits',
    ['cache_type']
)

CACHE_MISSES = Counter(
    'cache_misses_total',
    'Total cache misses',
    ['cache_type']
)

# Error metrics
ERROR_COUNT = Counter(
    'errors_total',
    'Total errors',
    ['error_type', 'endpoint']
)

# System metrics
ACTIVE_USERS = Gauge(
    'active_users',
    'Number of active users'
)

TASKS_IN_QUEUE = Gauge(
    'tasks_in_queue',
    'Number of tasks waiting in queue',
    ['task_type']
)

# Application info
APP_INFO = Info(
    'kreyol_ia_app',
    'Application information'
)


# ============================================================
# METRICS MIDDLEWARE
# ============================================================

class PrometheusMiddleware(BaseHTTPMiddleware):
    """
    Middleware to collect HTTP metrics automatically
    """
    
    async def dispatch(self, request: Request, call_next: Callable):
        """Process request and collect metrics"""
        
        # Skip metrics endpoint itself
        if request.url.path == "/metrics":
            return await call_next(request)
        
        method = request.method
        endpoint = request.url.path
        
        # Track in-progress requests
        REQUEST_IN_PROGRESS.labels(method=method, endpoint=endpoint).inc()
        
        # Record start time
        start_time = time.time()
        
        try:
            # Process request
            response = await call_next(request)
            
            # Record metrics
            status = response.status_code
            duration = time.time() - start_time
            
            REQUEST_COUNT.labels(
                method=method,
                endpoint=endpoint,
                status=status
            ).inc()
            
            REQUEST_DURATION.labels(
                method=method,
                endpoint=endpoint
            ).observe(duration)
            
            return response
            
        except Exception as e:
            # Record error
            duration = time.time() - start_time
            
            REQUEST_COUNT.labels(
                method=method,
                endpoint=endpoint,
                status=500
            ).inc()
            
            REQUEST_DURATION.labels(
                method=method,
                endpoint=endpoint
            ).observe(duration)
            
            ERROR_COUNT.labels(
                error_type=type(e).__name__,
                endpoint=endpoint
            ).inc()
            
            raise
            
        finally:
            # Decrement in-progress counter
            REQUEST_IN_PROGRESS.labels(method=method, endpoint=endpoint).dec()


# ============================================================
# METRICS DECORATORS
# ============================================================

def track_translation(func):
    """
    Decorator to track translation metrics
    
    Usage:
        @track_translation
        async def translate(text, source_lang, target_lang):
            ...
    """
    @wraps(func)
    async def wrapper(text: str, source_lang: str = "auto", target_lang: str = "ht", *args, **kwargs):
        start_time = time.time()
        status = "success"
        
        try:
            # Call function
            result = await func(text, source_lang, target_lang, *args, **kwargs)
            
            # Record metrics
            duration = time.time() - start_time
            
            TRANSLATION_COUNT.labels(
                source_lang=source_lang,
                target_lang=target_lang,
                status=status
            ).inc()
            
            TRANSLATION_DURATION.labels(
                source_lang=source_lang,
                target_lang=target_lang
            ).observe(duration)
            
            TRANSLATION_CHARS.observe(len(text))
            
            return result
            
        except Exception as e:
            status = "error"
            TRANSLATION_COUNT.labels(
                source_lang=source_lang,
                target_lang=target_lang,
                status=status
            ).inc()
            raise
    
    return wrapper


def track_audio_generation(func):
    """
    Decorator to track audio generation metrics
    
    Usage:
        @track_audio_generation
        async def generate_audio(text, voice_type):
            ...
    """
    @wraps(func)
    async def wrapper(text: str, voice_type: str = "default", *args, **kwargs):
        start_time = time.time()
        status = "success"
        
        try:
            # Call function
            result = await func(text, voice_type, *args, **kwargs)
            
            # Record metrics
            duration = time.time() - start_time
            
            AUDIO_GENERATION_COUNT.labels(
                voice_type=voice_type,
                status=status
            ).inc()
            
            AUDIO_GENERATION_DURATION.observe(duration)
            
            return result
            
        except Exception as e:
            status = "error"
            AUDIO_GENERATION_COUNT.labels(
                voice_type=voice_type,
                status=status
            ).inc()
            raise
    
    return wrapper


def track_file_processing(file_type: str):
    """
    Decorator to track file processing metrics
    
    Usage:
        @track_file_processing("pdf")
        async def process_pdf(file):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(file, *args, **kwargs):
            start_time = time.time()
            
            try:
                # Record file size
                content = await file.read()
                FILE_UPLOAD_SIZE.observe(len(content))
                await file.seek(0)
                
                # Call function
                result = await func(file, *args, **kwargs)
                
                # Record processing time
                duration = time.time() - start_time
                FILE_PROCESSING_DURATION.labels(file_type=file_type).observe(duration)
                
                return result
                
            except Exception as e:
                logger.error(f"File processing error: {e}")
                raise
        
        return wrapper
    return decorator


# ============================================================
# METRICS HELPERS
# ============================================================

def record_cache_hit(cache_type: str = "default"):
    """Record a cache hit"""
    CACHE_HITS.labels(cache_type=cache_type).inc()


def record_cache_miss(cache_type: str = "default"):
    """Record a cache miss"""
    CACHE_MISSES.labels(cache_type=cache_type).inc()


def record_error(error_type: str, endpoint: str = "unknown"):
    """Record an error"""
    ERROR_COUNT.labels(error_type=error_type, endpoint=endpoint).inc()


def set_active_users(count: int):
    """Set number of active users"""
    ACTIVE_USERS.set(count)


def set_tasks_in_queue(task_type: str, count: int):
    """Set number of tasks in queue"""
    TASKS_IN_QUEUE.labels(task_type=task_type).set(count)


def record_pdf_pages(page_count: int):
    """Record number of PDF pages processed"""
    PDF_PAGES_PROCESSED.observe(page_count)


def record_audio_duration(duration_seconds: float):
    """Record duration of generated audio"""
    AUDIO_DURATION_SECONDS.observe(duration_seconds)


def initialize_app_info(app_name: str, version: str, environment: str):
    """
    Initialize application info metric
    
    Args:
        app_name: Application name
        version: Application version
        environment: Deployment environment
    """
    APP_INFO.info({
        'app_name': app_name,
        'version': version,
        'environment': environment
    })
    logger.info(f"Metrics initialized: {app_name} v{version} ({environment})")


def get_metrics() -> str:
    """
    Get current metrics in Prometheus format
    
    Returns:
        Prometheus-formatted metrics string
    """
    return generate_latest()


def get_metrics_content_type() -> str:
    """Get Prometheus content type"""
    return CONTENT_TYPE_LATEST


# ============================================================
# METRICS ENDPOINT
# ============================================================

async def metrics_endpoint():
    """
    FastAPI endpoint for Prometheus metrics
    
    Usage:
        @app.get("/metrics")
        async def metrics():
            return await metrics_endpoint()
    """
    metrics_data = get_metrics()
    return Response(
        content=metrics_data,
        media_type=get_metrics_content_type()
    )


# ============================================================
# METRICS SUMMARY
# ============================================================

def get_metrics_summary() -> dict:
    """
    Get human-readable metrics summary
    
    Returns:
        Dictionary with metrics summary
    """
    # This is a simplified summary - in production, you'd query the actual metrics
    return {
        "requests": {
            "total": "See Prometheus",
            "in_progress": "See Prometheus"
        },
        "translations": {
            "total": "See Prometheus",
            "avg_duration": "See Prometheus"
        },
        "audio": {
            "total": "See Prometheus",
            "avg_duration": "See Prometheus"
        },
        "cache": {
            "hit_rate": "See Prometheus"
        },
        "errors": {
            "total": "See Prometheus"
        }
    }


if __name__ == "__main__":
    """Test metrics"""
    print("=" * 60)
    print("📊 Prometheus Metrics - Test")
    print("=" * 60)
    print()
    
    # Initialize
    initialize_app_info("Kreyòl IA", "2.0.0", "development")
    
    # Simulate some metrics
    print("Simulating metrics...")
    
    REQUEST_COUNT.labels(method="GET", endpoint="/api/health", status=200).inc()
    REQUEST_COUNT.labels(method="POST", endpoint="/api/translate", status=200).inc()
    TRANSLATION_COUNT.labels(source_lang="fr", target_lang="ht", status="success").inc()
    
    record_cache_hit("translation")
    record_cache_miss("translation")
    
    print("\n✅ Metrics recorded")
    print("\nMetrics would be available at: /metrics")
    print("Format: Prometheus text format")

