#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇭🇹 Faner Studio - Performance Utilities
Caching, rate limiting, and background tasks optimization
"""

from functools import wraps
from typing import Optional, Callable
import time
import hashlib
import json
from datetime import datetime, timedelta

# ============================================================
# IN-MEMORY CACHE (Simple LRU Cache)
# ============================================================

class SimpleCache:
    """Simple in-memory cache with TTL"""
    
    def __init__(self, default_ttl: int = 300):
        """
        Initialize cache
        
        Args:
            default_ttl: Default time-to-live in seconds (default: 5 minutes)
        """
        self.cache = {}
        self.default_ttl = default_ttl
    
    def set(self, key: str, value: any, ttl: Optional[int] = None):
        """Set cache value"""
        expire_at = time.time() + (ttl or self.default_ttl)
        self.cache[key] = {
            "value": value,
            "expire_at": expire_at
        }
    
    def get(self, key: str) -> Optional[any]:
        """Get cache value"""
        if key not in self.cache:
            return None
        
        item = self.cache[key]
        
        # Check if expired
        if time.time() > item["expire_at"]:
            del self.cache[key]
            return None
        
        return item["value"]
    
    def delete(self, key: str):
        """Delete cache key"""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        """Clear all cache"""
        self.cache = {}
    
    def cleanup(self):
        """Remove expired items"""
        current_time = time.time()
        expired_keys = [
            key for key, item in self.cache.items()
            if current_time > item["expire_at"]
        ]
        for key in expired_keys:
            del self.cache[key]
        return len(expired_keys)

# Global cache instance
cache = SimpleCache(default_ttl=300)  # 5 minutes default

# ============================================================
# CACHE DECORATORS
# ============================================================

def cached(ttl: int = 300, key_prefix: str = ""):
    """
    Cache decorator for functions
    
    Usage:
        @cached(ttl=600, key_prefix="translate")
        async def translate_text(text: str):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{_generate_cache_key(args, kwargs)}"
            
            # Check cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            cache.set(cache_key, result, ttl=ttl)
            
            return result
        
        return wrapper
    return decorator

def _generate_cache_key(args: tuple, kwargs: dict) -> str:
    """Generate cache key from function arguments"""
    key_data = {
        "args": args,
        "kwargs": kwargs
    }
    key_string = json.dumps(key_data, sort_keys=True, default=str)
    return hashlib.md5(key_string.encode()).hexdigest()

# ============================================================
# RATE LIMITING
# ============================================================

class RateLimiter:
    """Simple rate limiter"""
    
    def __init__(self):
        self.requests = {}
    
    def is_allowed(
        self,
        identifier: str,
        max_requests: int = 60,
        window_seconds: int = 60
    ) -> tuple[bool, Optional[int]]:
        """
        Check if request is allowed
        
        Returns:
            (is_allowed, retry_after_seconds)
        """
        now = time.time()
        window_start = now - window_seconds
        
        # Clean old requests
        if identifier in self.requests:
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > window_start
            ]
        else:
            self.requests[identifier] = []
        
        # Check limit
        if len(self.requests[identifier]) >= max_requests:
            # Calculate retry after
            oldest_request = min(self.requests[identifier])
            retry_after = int(oldest_request + window_seconds - now) + 1
            return False, retry_after
        
        # Add request
        self.requests[identifier].append(now)
        return True, None
    
    def cleanup(self, max_age_seconds: int = 3600):
        """Clean up old entries"""
        now = time.time()
        cutoff = now - max_age_seconds
        
        to_delete = []
        for identifier, requests in self.requests.items():
            # Remove old requests
            self.requests[identifier] = [
                req_time for req_time in requests
                if req_time > cutoff
            ]
            # Mark for deletion if empty
            if not self.requests[identifier]:
                to_delete.append(identifier)
        
        for identifier in to_delete:
            del self.requests[identifier]

# Global rate limiter
rate_limiter = RateLimiter()

# ============================================================
# BACKGROUND TASKS UTILITIES
# ============================================================

class BackgroundTaskQueue:
    """Simple background task queue (in-memory)"""
    
    def __init__(self):
        self.tasks = []
        self.completed_tasks = []
    
    def add_task(self, task_id: str, task_type: str, params: dict):
        """Add task to queue"""
        task = {
            "id": task_id,
            "type": task_type,
            "params": params,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "started_at": None,
            "completed_at": None,
            "result": None,
            "error": None
        }
        self.tasks.append(task)
        return task
    
    def get_task(self, task_id: str) -> Optional[dict]:
        """Get task by ID"""
        # Check pending tasks
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        
        # Check completed tasks
        for task in self.completed_tasks:
            if task["id"] == task_id:
                return task
        
        return None
    
    def update_task_status(self, task_id: str, status: str, **kwargs):
        """Update task status"""
        task = self.get_task(task_id)
        if task:
            task["status"] = status
            task.update(kwargs)
            
            if status == "completed" or status == "failed":
                task["completed_at"] = datetime.utcnow()
                # Move to completed
                if task in self.tasks:
                    self.tasks.remove(task)
                    self.completed_tasks.append(task)
    
    def cleanup_old_tasks(self, max_age_hours: int = 24):
        """Remove old completed tasks"""
        cutoff = datetime.utcnow() - timedelta(hours=max_age_hours)
        self.completed_tasks = [
            task for task in self.completed_tasks
            if task["completed_at"] and task["completed_at"] > cutoff
        ]

# Global task queue
task_queue = BackgroundTaskQueue()

# ============================================================
# PERFORMANCE MONITORING
# ============================================================

class PerformanceMonitor:
    """Monitor API performance"""
    
    def __init__(self):
        self.metrics = {}
    
    def record_request(self, endpoint: str, duration_ms: float, status_code: int):
        """Record request metrics"""
        if endpoint not in self.metrics:
            self.metrics[endpoint] = {
                "count": 0,
                "total_time": 0.0,
                "min_time": float('inf'),
                "max_time": 0.0,
                "errors": 0
            }
        
        metrics = self.metrics[endpoint]
        metrics["count"] += 1
        metrics["total_time"] += duration_ms
        metrics["min_time"] = min(metrics["min_time"], duration_ms)
        metrics["max_time"] = max(metrics["max_time"], duration_ms)
        
        if status_code >= 400:
            metrics["errors"] += 1
    
    def get_stats(self, endpoint: Optional[str] = None) -> dict:
        """Get performance stats"""
        if endpoint:
            if endpoint not in self.metrics:
                return None
            
            metrics = self.metrics[endpoint]
            return {
                "endpoint": endpoint,
                "requests": metrics["count"],
                "avg_time_ms": metrics["total_time"] / metrics["count"] if metrics["count"] > 0 else 0,
                "min_time_ms": metrics["min_time"],
                "max_time_ms": metrics["max_time"],
                "error_rate": metrics["errors"] / metrics["count"] if metrics["count"] > 0 else 0
            }
        
        # Return all stats
        return {
            endpoint: self.get_stats(endpoint)
            for endpoint in self.metrics.keys()
        }

# Global performance monitor
perf_monitor = PerformanceMonitor()

# ============================================================
# UTILITIES
# ============================================================

def format_bytes(bytes_size: int) -> str:
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def format_duration(seconds: float) -> str:
    """Format duration to human readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"

# ============================================================
# HEALTH CHECK UTILITIES
# ============================================================

def get_system_stats() -> dict:
    """Get system statistics"""
    import psutil
    
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_used_mb": memory.used / (1024 * 1024),
            "memory_total_mb": memory.total / (1024 * 1024),
            "disk_percent": disk.percent,
            "disk_used_gb": disk.used / (1024 * 1024 * 1024),
            "disk_total_gb": disk.total / (1024 * 1024 * 1024)
        }
    except:
        return {
            "cpu_percent": 0,
            "memory_percent": 0,
            "memory_used_mb": 0,
            "memory_total_mb": 0,
            "disk_percent": 0,
            "disk_used_gb": 0,
            "disk_total_gb": 0,
            "note": "psutil not available"
        }

