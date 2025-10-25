#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💾 Redis Cache System
Sistèm kachaj distribiye ak Redis (100x pi rapid ke file cache!)
"""

import redis
import json
import os
import hashlib
from typing import Optional, Any, Callable
from datetime import timedelta

class RedisCache:
    """
    Sistèm kachaj distribiye ak Redis
    
    Avantaj sou file cache:
    - 100x pi rapid (0.1ms vs 10ms)
    - Distribiye (shared between instances)
    - Auto-expiration
    - Atomic operations
    - Memory efficient
    """
    
    def __init__(
        self,
        host: str = None,
        port: int = None,
        db: int = 0,
        ttl_hours: int = 24,
        prefix: str = ""
    ):
        """
        Inisyalize Redis cache
        
        Args:
            host: Redis host (default: localhost oswa REDIS_HOST env)
            port: Redis port (default: 6379 oswa REDIS_PORT env)
            db: Redis database number
            ttl_hours: Time-to-live an è
            prefix: Prefix pou tout keys
        """
        # Get from environment or use defaults
        host = host or os.getenv("REDIS_HOST", "localhost")
        port = port or int(os.getenv("REDIS_PORT", "6379"))
        password = os.getenv("REDIS_PASSWORD", None)
        
        # Try to connect to Redis
        try:
            self.redis = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            
            # Test connection
            self.redis.ping()
            self.available = True
            print(f"✅ Redis Cache initialized: {host}:{port} DB{db} (TTL: {ttl_hours}h)")
            
        except (redis.ConnectionError, redis.TimeoutError) as e:
            print(f"⚠️  Redis not available: {e}")
            print(f"   Falling back to memory cache...")
            self.redis = None
            self.available = False
            self._memory_cache = {}  # Fallback to in-memory dict
        
        self.ttl = timedelta(hours=ttl_hours)
        self.prefix = prefix
    
    def _get_key(self, key: str) -> str:
        """Generate full key with prefix"""
        return f"{self.prefix}:{key}" if self.prefix else key
    
    def _get_cache_key(self, data: str) -> str:
        """Generate cache key from data using MD5"""
        return hashlib.md5(data.encode('utf-8')).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None if not found/expired
        """
        if not self.available:
            # Fallback to memory cache
            return self._memory_cache.get(self._get_key(key))
        
        try:
            full_key = self._get_key(key)
            value = self.redis.get(full_key)
            
            if value is None:
                return None
            
            # Deserialize JSON
            return json.loads(value)
            
        except Exception as e:
            print(f"⚠️  Redis GET error: {e}")
            return None
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: int = None
    ) -> bool:
        """
        Set value in cache with auto-expiration
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (default: use instance TTL)
        
        Returns:
            True if successful, False otherwise
        """
        if not self.available:
            # Fallback to memory cache
            self._memory_cache[self._get_key(key)] = value
            return True
        
        try:
            full_key = self._get_key(key)
            ttl_seconds = ttl or int(self.ttl.total_seconds())
            
            # Serialize to JSON
            serialized = json.dumps(value, ensure_ascii=False)
            
            # Set with expiration
            return self.redis.setex(
                full_key,
                ttl_seconds,
                serialized
            )
            
        except Exception as e:
            print(f"⚠️  Redis SET error: {e}")
            return False
    
    def get_or_compute(
        self,
        key: str,
        compute_fn: Callable,
        ttl: int = None
    ) -> Any:
        """
        Get from cache or compute if not found
        
        Args:
            key: Cache key
            compute_fn: Function to compute value if not in cache
            ttl: Time-to-live in seconds
        
        Returns:
            Cached or computed value
        """
        # Try cache first
        cached = self.get(key)
        if cached is not None:
            return cached
        
        # Compute value
        value = compute_fn()
        
        # Cache it
        self.set(key, value, ttl)
        
        return value
    
    def delete(self, key: str) -> bool:
        """
        Delete a key from cache
        
        Args:
            key: Cache key
        
        Returns:
            True if deleted, False otherwise
        """
        if not self.available:
            self._memory_cache.pop(self._get_key(key), None)
            return True
        
        try:
            full_key = self._get_key(key)
            return bool(self.redis.delete(full_key))
        except Exception as e:
            print(f"⚠️  Redis DELETE error: {e}")
            return False
    
    def clear_pattern(self, pattern: str) -> int:
        """
        Clear all keys matching a pattern
        
        Args:
            pattern: Pattern to match (e.g., "user:*")
        
        Returns:
            Number of keys deleted
        """
        if not self.available:
            # Clear from memory cache
            keys_to_delete = [
                k for k in self._memory_cache.keys()
                if pattern.replace('*', '') in k
            ]
            for k in keys_to_delete:
                del self._memory_cache[k]
            return len(keys_to_delete)
        
        try:
            full_pattern = self._get_key(pattern)
            keys = list(self.redis.scan_iter(match=full_pattern))
            
            if keys:
                return self.redis.delete(*keys)
            return 0
            
        except Exception as e:
            print(f"⚠️  Redis CLEAR error: {e}")
            return 0
    
    def clear(self) -> int:
        """
        Clear all keys with this cache's prefix
        
        Returns:
            Number of keys deleted
        """
        if self.prefix:
            return self.clear_pattern(f"{self.prefix}:*")
        else:
            # Be careful - this clears entire DB!
            if not self.available:
                count = len(self._memory_cache)
                self._memory_cache.clear()
                return count
            
            try:
                keys = list(self.redis.scan_iter())
                if keys:
                    return self.redis.delete(*keys)
                return 0
            except Exception as e:
                print(f"⚠️  Redis CLEAR ALL error: {e}")
                return 0
    
    def get_stats(self) -> dict:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache stats
        """
        if not self.available:
            return {
                "available": False,
                "fallback": "memory",
                "keys": len(self._memory_cache),
                "ttl_hours": self.ttl.total_seconds() / 3600
            }
        
        try:
            info = self.redis.info('stats')
            memory_info = self.redis.info('memory')
            
            # Get number of keys
            dbsize = self.redis.dbsize()
            
            # Calculate hit rate
            hits = info.get('keyspace_hits', 0)
            misses = info.get('keyspace_misses', 0)
            total = hits + misses
            hit_rate = (hits / total * 100) if total > 0 else 0
            
            return {
                "available": True,
                "keys": dbsize,
                "hits": hits,
                "misses": misses,
                "hit_rate": f"{hit_rate:.1f}%",
                "memory_used": memory_info.get('used_memory_human', 'N/A'),
                "ttl_hours": self.ttl.total_seconds() / 3600
            }
            
        except Exception as e:
            print(f"⚠️  Redis STATS error: {e}")
            return {
                "available": False,
                "error": str(e)
            }
    
    def ping(self) -> bool:
        """
        Test if Redis is available
        
        Returns:
            True if Redis responds, False otherwise
        """
        if not self.available:
            return False
        
        try:
            return self.redis.ping()
        except:
            return False


# ============================================================
# GLOBAL CACHE INSTANCES
# ============================================================

# Translation cache (1 week TTL)
translation_cache = RedisCache(
    db=0,
    ttl_hours=168,  # 7 days
    prefix="trans"
)

# Audio cache (3 days TTL)
audio_cache = RedisCache(
    db=1,
    ttl_hours=72,  # 3 days
    prefix="audio"
)

# Session cache (1 day TTL)
session_cache = RedisCache(
    db=2,
    ttl_hours=24,  # 1 day
    prefix="session"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def cached_translation(
    text: str,
    source_lang: str,
    target_lang: str,
    translate_fn: Callable
) -> str:
    """
    Helper function for cached translation
    
    Args:
        text: Text to translate
        source_lang: Source language
        target_lang: Target language
        translate_fn: Translation function
    
    Returns:
        Translated text
    """
    # Create cache key
    cache_data = f"{source_lang}:{target_lang}:{text}"
    cache_key = translation_cache._get_cache_key(cache_data)
    
    # Get or compute
    return translation_cache.get_or_compute(
        cache_key,
        lambda: translate_fn(text, source_lang, target_lang)
    )


if __name__ == "__main__":
    print("🧪 Testing Redis Cache...")
    
    # Test connection
    cache = RedisCache(prefix="test")
    
    if cache.available:
        print("✅ Redis available!")
        
        # Test set/get
        cache.set("key1", "value1")
        print(f"   GET key1: {cache.get('key1')}")
        
        # Test stats
        stats = cache.get_stats()
        print(f"   Stats: {stats}")
        
        # Cleanup
        cache.clear()
    else:
        print("⚠️  Redis not available - using memory fallback")

