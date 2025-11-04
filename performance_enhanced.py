#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ Enhanced Performance Module
Advanced caching, rate limiting, and monitoring
"""

import time
import psutil
from pathlib import Path
from typing import Dict, Optional, Callable
from functools import wraps
from datetime import datetime, timedelta
import json
import hashlib


class PersistentCache:
    """
    File-based cache that persists between restarts
    Cache avèk dosye ki rete apre restart
    """
    
    def __init__(self, cache_dir: Path = None, ttl: int = 3600):
        self.cache_dir = cache_dir or Path("cache")
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        self.ttl = ttl  # Time to live in seconds
        self.memory_cache = {}  # Fast in-memory cache
    
    def _get_cache_path(self, key: str) -> Path:
        """Get file path for cache key"""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.cache"
    
    def get(self, key: str) -> Optional[any]:
        """Get cached value"""
        # Check memory cache first
        if key in self.memory_cache:
            value, expiry = self.memory_cache[key]
            if time.time() < expiry:
                return value
            else:
                del self.memory_cache[key]
        
        # Check file cache
        cache_file = self._get_cache_path(key)
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if time.time() < data['expiry']:
                    # Load into memory cache
                    self.memory_cache[key] = (data['value'], data['expiry'])
                    return data['value']
                else:
                    # Expired, delete file
                    cache_file.unlink()
            except Exception:
                pass
        
        return None
    
    def set(self, key: str, value: any, ttl: Optional[int] = None):
        """Set cached value"""
        ttl = ttl or self.ttl
        expiry = time.time() + ttl
        
        # Save to memory cache
        self.memory_cache[key] = (value, expiry)
        
        # Save to file cache
        cache_file = self._get_cache_path(key)
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'value': value,
                    'expiry': expiry,
                    'created': time.time()
                }, f)
        except Exception:
            pass
    
    def delete(self, key: str):
        """Delete cached value"""
        # Delete from memory
        if key in self.memory_cache:
            del self.memory_cache[key]
        
        # Delete file
        cache_file = self._get_cache_path(key)
        if cache_file.exists():
            cache_file.unlink()
    
    def clear(self):
        """Clear all cache"""
        self.memory_cache.clear()
        
        # Delete all cache files
        for cache_file in self.cache_dir.glob("*.cache"):
            try:
                cache_file.unlink()
            except Exception:
                pass
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        cache_files = list(self.cache_dir.glob("*.cache"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            "memory_items": len(self.memory_cache),
            "disk_items": len(cache_files),
            "disk_size_mb": total_size / (1024 * 1024),
            "cache_dir": str(self.cache_dir)
        }


class SmartRateLimiter:
    """
    Advanced rate limiter with burst allowance
    Rate limiter avanse ak tòlerans pou burst
    """
    
    def __init__(self, max_requests: int = 100, window: int = 60, burst_factor: float = 1.5):
        self.max_requests = max_requests
        self.window = window
        self.burst_factor = burst_factor
        self.requests = {}  # {identifier: [(timestamp, count)]}
    
    def is_allowed(self, identifier: str) -> tuple[bool, Dict]:
        """
        Check if request is allowed
        
        Returns:
            (allowed, info_dict)
        """
        now = time.time()
        
        # Clean old requests
        if identifier in self.requests:
            self.requests[identifier] = [
                (ts, count) for ts, count in self.requests[identifier]
                if now - ts < self.window
            ]
        else:
            self.requests[identifier] = []
        
        # Count requests in window
        total_requests = sum(count for _, count in self.requests[identifier])
        
        # Calculate limit with burst allowance
        max_allowed = int(self.max_requests * self.burst_factor)
        
        # Check if allowed
        allowed = total_requests < max_allowed
        
        if allowed:
            self.requests[identifier].append((now, 1))
        
        # Calculate remaining
        remaining = max(0, max_allowed - total_requests - (1 if allowed else 0))
        
        # Calculate reset time
        if self.requests[identifier]:
            oldest = min(ts for ts, _ in self.requests[identifier])
            reset_time = oldest + self.window
        else:
            reset_time = now + self.window
        
        return allowed, {
            "allowed": allowed,
            "limit": max_allowed,
            "remaining": remaining,
            "reset": reset_time,
            "retry_after": reset_time - now if not allowed else 0
        }


class AdvancedMonitor:
    """
    Advanced performance monitor with detailed metrics
    Monitè pèfòmans avanse ak metrik detaye
    """
    
    def __init__(self):
        self.metrics = {}
        self.start_time = time.time()
    
    def track_request(self, endpoint: str, duration: float, status: int):
        """Track API request"""
        if endpoint not in self.metrics:
            self.metrics[endpoint] = {
                "count": 0,
                "total_duration": 0,
                "min_duration": float('inf'),
                "max_duration": 0,
                "errors": 0,
                "success": 0
            }
        
        metric = self.metrics[endpoint]
        metric["count"] += 1
        metric["total_duration"] += duration
        metric["min_duration"] = min(metric["min_duration"], duration)
        metric["max_duration"] = max(metric["max_duration"], duration)
        
        if status >= 400:
            metric["errors"] += 1
        else:
            metric["success"] += 1
    
    def get_stats(self, endpoint: Optional[str] = None) -> Dict:
        """Get performance statistics"""
        if endpoint:
            if endpoint in self.metrics:
                metric = self.metrics[endpoint]
                return {
                    "endpoint": endpoint,
                    "total_requests": metric["count"],
                    "avg_duration": metric["total_duration"] / metric["count"] if metric["count"] > 0 else 0,
                    "min_duration": metric["min_duration"],
                    "max_duration": metric["max_duration"],
                    "success_rate": (metric["success"] / metric["count"] * 100) if metric["count"] > 0 else 0,
                    "error_rate": (metric["errors"] / metric["count"] * 100) if metric["count"] > 0 else 0
                }
            return {}
        
        # Return all stats
        return {
            endpoint: {
                "total_requests": metric["count"],
                "avg_duration": metric["total_duration"] / metric["count"] if metric["count"] > 0 else 0,
                "success_rate": (metric["success"] / metric["count"] * 100) if metric["count"] > 0 else 0
            }
            for endpoint, metric in self.metrics.items()
        }
    
    def get_system_stats(self) -> Dict:
        """Get system statistics"""
        uptime = time.time() - self.start_time
        
        return {
            "uptime_seconds": uptime,
            "uptime_formatted": format_duration(uptime),
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_used_mb": psutil.virtual_memory().used / (1024 * 1024),
            "memory_total_mb": psutil.virtual_memory().total / (1024 * 1024),
            "disk_percent": psutil.disk_usage('/').percent,
            "requests_total": sum(m["count"] for m in self.metrics.values())
        }


# Utility functions
def format_bytes(bytes: int) -> str:
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"


def format_duration(seconds: float) -> str:
    """Format duration to human readable"""
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        return f"{seconds/60:.2f}m"
    elif seconds < 86400:
        return f"{seconds/3600:.2f}h"
    else:
        return f"{seconds/86400:.2f}d"


# Decorators
def cached(ttl: int = 3600):
    """Decorator for caching function results"""
    def decorator(func: Callable) -> Callable:
        cache = PersistentCache(ttl=ttl)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Check cache
            cached_result = cache.get(key)
            if cached_result is not None:
                return cached_result
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Cache result
            cache.set(key, result, ttl=ttl)
            
            return result
        
        return wrapper
    return decorator


# Global instances
persistent_cache = PersistentCache()
smart_rate_limiter = SmartRateLimiter()
advanced_monitor = AdvancedMonitor()

# Legacy compatibility
cache = persistent_cache
rate_limiter = smart_rate_limiter
perf_monitor = advanced_monitor


def get_system_stats() -> Dict:
    """Get system statistics (legacy)"""
    return advanced_monitor.get_system_stats()

