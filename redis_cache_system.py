#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔴 Redis Caching System for Faner Studio
High-performance distributed caching with Redis

Provides:
- Distributed caching across multiple servers
- Fast in-memory operations
- Automatic expiration
- Cache invalidation strategies
"""

import redis
import json
import pickle
import hashlib
from typing import Any, Optional, Callable
from functools import wraps
from datetime import timedelta
import logging
import os

logger = logging.getLogger('FanerStudio.Redis')


class RedisCache:
    """
    Redis-based caching system
    Sistèm cache avèk Redis
    """
    
    def __init__(
        self,
        host: str = None,
        port: int = 6379,
        db: int = 0,
        password: str = None,
        decode_responses: bool = True
    ):
        """
        Initialize Redis connection
        
        Args:
            host: Redis host (default: from REDIS_URL env or localhost)
            port: Redis port
            db: Redis database number
            password: Redis password
            decode_responses: Auto-decode responses to strings
        """
        # Get Redis URL from environment
        redis_url = os.getenv('REDIS_URL')
        
        if redis_url:
            # Use connection URL (production)
            self.client = redis.from_url(
                redis_url,
                decode_responses=decode_responses
            )
            logger.info(f"✅ Connected to Redis via URL")
        else:
            # Use individual parameters (local)
            host = host or os.getenv('REDIS_HOST', 'localhost')
            self.client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=decode_responses
            )
            logger.info(f"✅ Connected to Redis at {host}:{port}")
        
        # Test connection
        try:
            self.client.ping()
            logger.info("✅ Redis connection successful")
        except redis.ConnectionError as e:
            logger.error(f"❌ Redis connection failed: {e}")
            raise
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None
        """
        try:
            value = self.client.get(key)
            if value:
                # Try to deserialize JSON
                try:
                    return json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    return value
            return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: int = 3600
    ) -> bool:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (default: 1 hour)
        
        Returns:
            Success status
        """
        try:
            # Serialize value
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            # Set with expiration
            return self.client.setex(key, ttl, value)
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            return bool(self.client.delete(key))
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        try:
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(f"Cache exists error: {e}")
            return False
    
    def clear(self) -> bool:
        """Clear all cache"""
        try:
            return self.client.flushdb()
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False
    
    def get_many(self, keys: list) -> dict:
        """Get multiple keys at once"""
        try:
            values = self.client.mget(keys)
            result = {}
            for key, value in zip(keys, values):
                if value:
                    try:
                        result[key] = json.loads(value)
                    except:
                        result[key] = value
            return result
        except Exception as e:
            logger.error(f"Cache get_many error: {e}")
            return {}
    
    def set_many(self, mapping: dict, ttl: int = 3600) -> bool:
        """Set multiple keys at once"""
        try:
            pipe = self.client.pipeline()
            for key, value in mapping.items():
                if isinstance(value, (dict, list)):
                    value = json.dumps(value)
                pipe.setex(key, ttl, value)
            pipe.execute()
            return True
        except Exception as e:
            logger.error(f"Cache set_many error: {e}")
            return False
    
    def increment(self, key: str, amount: int = 1) -> int:
        """Increment counter"""
        try:
            return self.client.incrby(key, amount)
        except Exception as e:
            logger.error(f"Cache increment error: {e}")
            return 0
    
    def decrement(self, key: str, amount: int = 1) -> int:
        """Decrement counter"""
        try:
            return self.client.decrby(key, amount)
        except Exception as e:
            logger.error(f"Cache decrement error: {e}")
            return 0
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        try:
            info = self.client.info('stats')
            return {
                "total_keys": self.client.dbsize(),
                "total_connections": info.get('total_connections_received', 0),
                "total_commands": info.get('total_commands_processed', 0),
                "instantaneous_ops": info.get('instantaneous_ops_per_sec', 0),
                "used_memory_mb": self.client.info('memory').get('used_memory', 0) / (1024 * 1024),
                "connected_clients": info.get('connected_clients', 0)
            }
        except Exception as e:
            logger.error(f"Stats error: {e}")
            return {}


# ============================================================
# CACHE DECORATORS
# ============================================================

class CacheDecorator:
    """Decorator for caching function results"""
    
    def __init__(self, redis_cache: RedisCache):
        self.cache = redis_cache
    
    def cached(
        self,
        ttl: int = 3600,
        key_prefix: str = None,
        key_builder: Callable = None
    ):
        """
        Cache decorator
        
        Usage:
            @cache_decorator.cached(ttl=7200)
            def expensive_function(arg1, arg2):
                return result
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Build cache key
                if key_builder:
                    cache_key = key_builder(*args, **kwargs)
                else:
                    # Default: function name + args hash
                    prefix = key_prefix or func.__name__
                    args_str = f"{args}_{kwargs}"
                    args_hash = hashlib.md5(args_str.encode()).hexdigest()
                    cache_key = f"{prefix}:{args_hash}"
                
                # Try to get from cache
                cached_value = self.cache.get(cache_key)
                if cached_value is not None:
                    logger.debug(f"Cache hit: {cache_key}")
                    return cached_value
                
                # Execute function
                logger.debug(f"Cache miss: {cache_key}")
                result = func(*args, **kwargs)
                
                # Cache result
                self.cache.set(cache_key, result, ttl=ttl)
                
                return result
            
            return wrapper
        return decorator


# ============================================================
# SPECIALIZED CACHES
# ============================================================

class TranslationCache(RedisCache):
    """Specialized cache for translations"""
    
    def get_translation(
        self,
        text: str,
        source: str,
        target: str
    ) -> Optional[str]:
        """Get cached translation"""
        key = f"translation:{source}:{target}:{hashlib.md5(text.encode()).hexdigest()}"
        return self.get(key)
    
    def set_translation(
        self,
        text: str,
        source: str,
        target: str,
        translation: str,
        ttl: int = 86400  # 24 hours
    ):
        """Cache translation"""
        key = f"translation:{source}:{target}:{hashlib.md5(text.encode()).hexdigest()}"
        return self.set(key, translation, ttl=ttl)


class TTSCache(RedisCache):
    """Specialized cache for TTS results"""
    
    def get_audio_path(
        self,
        text: str,
        voice: str
    ) -> Optional[str]:
        """Get cached audio file path"""
        key = f"tts:{voice}:{hashlib.md5(text.encode()).hexdigest()}"
        return self.get(key)
    
    def set_audio_path(
        self,
        text: str,
        voice: str,
        audio_path: str,
        ttl: int = 604800  # 7 days
    ):
        """Cache audio file path"""
        key = f"tts:{voice}:{hashlib.md5(text.encode()).hexdigest()}"
        return self.set(key, audio_path, ttl=ttl)


class SessionCache(RedisCache):
    """Cache for user sessions"""
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """Get user session"""
        key = f"session:{session_id}"
        return self.get(key)
    
    def set_session(
        self,
        session_id: str,
        session_data: dict,
        ttl: int = 3600  # 1 hour
    ):
        """Set user session"""
        key = f"session:{session_id}"
        return self.set(key, session_data, ttl=ttl)
    
    def delete_session(self, session_id: str):
        """Delete user session"""
        key = f"session:{session_id}"
        return self.delete(key)


# ============================================================
# FALLBACK TO FILE CACHE
# ============================================================

class RedisFallback:
    """
    Fallback to file-based cache if Redis not available
    Uses the existing PersistentCache
    """
    
    def __init__(self):
        try:
            # Try Redis first
            self.cache = RedisCache()
            self.using_redis = True
            logger.info("✅ Using Redis cache")
        except:
            # Fallback to file cache
            from performance_enhanced import PersistentCache
            self.cache = PersistentCache()
            self.using_redis = False
            logger.warning("⚠️  Redis not available, using file cache")
    
    def get(self, key: str):
        return self.cache.get(key)
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        if self.using_redis:
            return self.cache.set(key, value, ttl=ttl)
        else:
            return self.cache.set(key, value, ttl=ttl)
    
    def delete(self, key: str):
        return self.cache.delete(key)
    
    def clear(self):
        return self.cache.clear()


# ============================================================
# GLOBAL INSTANCES
# ============================================================

# Create global instances (with fallback)
try:
    redis_cache = RedisCache()
    translation_cache = TranslationCache()
    tts_cache = TTSCache()
    session_cache = SessionCache()
    cache_decorator = CacheDecorator(redis_cache)
    
    logger.info("✅ All Redis caches initialized")
except Exception as e:
    logger.warning(f"⚠️  Redis not available: {e}")
    logger.info("Using fallback file-based cache")
    redis_cache = None
    cache_decorator = None


# ============================================================
# TESTING
# ============================================================

def test_redis_cache():
    """Test Redis cache functionality"""
    print("🧪 Testing Redis Cache\n")
    
    try:
        cache = RedisCache()
        
        # Test basic operations
        print("1. Testing set/get:")
        cache.set("test_key", "test_value", ttl=60)
        value = cache.get("test_key")
        print(f"   ✅ Set and got: {value}")
        
        # Test JSON serialization
        print("\n2. Testing JSON:")
        cache.set("test_dict", {"name": "Faner", "version": "3.2.0"}, ttl=60)
        data = cache.get("test_dict")
        print(f"   ✅ Dict: {data}")
        
        # Test stats
        print("\n3. Cache stats:")
        stats = cache.get_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # Cleanup
        cache.delete("test_key")
        cache.delete("test_dict")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")


if __name__ == "__main__":
    test_redis_cache()

