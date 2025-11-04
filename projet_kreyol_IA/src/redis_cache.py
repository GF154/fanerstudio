#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Redis Cache Module
Distributed caching for improved scalability
"""

import logging
import json
import hashlib
from typing import Optional, Any
from datetime import timedelta

logger = logging.getLogger('KreyolAI.RedisCache')

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available. Install with: pip install redis")


class RedisCache:
    """
    Redis-based distributed cache for translations and other data
    """
    
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        default_ttl: int = 86400,  # 24 hours
        enabled: bool = True
    ):
        """
        Initialize Redis cache
        
        Args:
            host: Redis server host
            port: Redis server port
            db: Redis database number
            password: Redis password (if required)
            default_ttl: Default time-to-live in seconds
            enabled: Whether cache is enabled
        """
        self.enabled = enabled and REDIS_AVAILABLE
        self.default_ttl = default_ttl
        self.client = None
        self.hits = 0
        self.misses = 0
        
        if not REDIS_AVAILABLE:
            logger.warning("Redis not available, cache disabled")
            self.enabled = False
            return
        
        if self.enabled:
            try:
                self.client = redis.Redis(
                    host=host,
                    port=port,
                    db=db,
                    password=password,
                    decode_responses=True,
                    socket_timeout=5,
                    socket_connect_timeout=5
                )
                # Test connection
                self.client.ping()
                logger.info(f"Redis cache connected: {host}:{port}/{db}")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                self.enabled = False
                self.client = None
    
    def _make_key(self, prefix: str, data: str) -> str:
        """
        Generate cache key from data
        
        Args:
            prefix: Key prefix
            data: Data to hash
        
        Returns:
            Cache key
        """
        hash_value = hashlib.md5(data.encode('utf-8')).hexdigest()
        return f"{prefix}:{hash_value}"
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None
        """
        if not self.enabled:
            return None
        
        try:
            value = self.client.get(key)
            if value is not None:
                self.hits += 1
                logger.debug(f"Cache hit: {key}")
                return json.loads(value)
            else:
                self.misses += 1
                logger.debug(f"Cache miss: {key}")
                return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (None = default)
        
        Returns:
            True if successful
        """
        if not self.enabled:
            return False
        
        try:
            ttl = ttl or self.default_ttl
            serialized = json.dumps(value, ensure_ascii=False)
            self.client.setex(key, ttl, serialized)
            logger.debug(f"Cache set: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete value from cache
        
        Args:
            key: Cache key
        
        Returns:
            True if successful
        """
        if not self.enabled:
            return False
        
        try:
            self.client.delete(key)
            logger.debug(f"Cache delete: {key}")
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    def clear(self, pattern: Optional[str] = None) -> bool:
        """
        Clear cache
        
        Args:
            pattern: Key pattern to clear (None = all)
        
        Returns:
            True if successful
        """
        if not self.enabled:
            return False
        
        try:
            if pattern:
                keys = self.client.keys(pattern)
                if keys:
                    self.client.delete(*keys)
                logger.info(f"Cache cleared: {pattern} ({len(keys)} keys)")
            else:
                self.client.flushdb()
                logger.info("Cache cleared: all keys")
            return True
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False
    
    def get_stats(self) -> dict:
        """
        Get cache statistics
        
        Returns:
            Dictionary with statistics
        """
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        stats = {
            "enabled": self.enabled,
            "hits": self.hits,
            "misses": self.misses,
            "total": total,
            "hit_rate": round(hit_rate, 2)
        }
        
        if self.enabled and self.client:
            try:
                info = self.client.info()
                stats.update({
                    "memory_used": info.get("used_memory_human", "N/A"),
                    "keys": self.client.dbsize(),
                    "uptime": info.get("uptime_in_seconds", 0)
                })
            except Exception as e:
                logger.error(f"Failed to get Redis info: {e}")
        
        return stats
    
    def reset_stats(self):
        """Reset cache statistics"""
        self.hits = 0
        self.misses = 0
        logger.info("Cache statistics reset")


class TranslationCache:
    """
    Cache specifically for translations
    """
    
    def __init__(
        self,
        redis_cache: Optional[RedisCache] = None,
        default_ttl: int = 86400
    ):
        """
        Initialize translation cache
        
        Args:
            redis_cache: Redis cache instance (None = create new)
            default_ttl: Default TTL in seconds
        """
        if redis_cache is None:
            redis_cache = RedisCache(default_ttl=default_ttl)
        
        self.cache = redis_cache
        self.prefix = "translation"
        logger.info("Translation cache initialized")
    
    def _make_key(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """
        Generate translation cache key
        
        Args:
            text: Source text
            src_lang: Source language
            tgt_lang: Target language
        
        Returns:
            Cache key
        """
        data = f"{text}|{src_lang}|{tgt_lang}"
        return self.cache._make_key(self.prefix, data)
    
    def get_translation(
        self,
        text: str,
        src_lang: str,
        tgt_lang: str
    ) -> Optional[str]:
        """
        Get cached translation
        
        Args:
            text: Source text
            src_lang: Source language
            tgt_lang: Target language
        
        Returns:
            Cached translation or None
        """
        key = self._make_key(text, src_lang, tgt_lang)
        result = self.cache.get(key)
        
        if result:
            logger.info(f"Translation cache hit: {src_lang} → {tgt_lang} ({len(text)} chars)")
            return result.get("translation")
        
        logger.debug(f"Translation cache miss: {src_lang} → {tgt_lang}")
        return None
    
    def set_translation(
        self,
        text: str,
        translation: str,
        src_lang: str,
        tgt_lang: str,
        ttl: Optional[int] = None
    ) -> bool:
        """
        Cache translation
        
        Args:
            text: Source text
            translation: Translated text
            src_lang: Source language
            tgt_lang: Target language
            ttl: Time-to-live in seconds
        
        Returns:
            True if successful
        """
        key = self._make_key(text, src_lang, tgt_lang)
        value = {
            "translation": translation,
            "src_lang": src_lang,
            "tgt_lang": tgt_lang,
            "text_length": len(text),
            "translation_length": len(translation)
        }
        
        success = self.cache.set(key, value, ttl)
        
        if success:
            logger.info(f"Translation cached: {src_lang} → {tgt_lang} ({len(text)} chars)")
        
        return success
    
    def clear_translations(self):
        """Clear all translation cache"""
        return self.cache.clear(f"{self.prefix}:*")
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        return self.cache.get_stats()


# Global cache instance
_redis_cache = None
_translation_cache = None


def get_redis_cache(
    host: str = 'localhost',
    port: int = 6379,
    enabled: bool = True
) -> RedisCache:
    """
    Get global Redis cache instance
    
    Args:
        host: Redis host
        port: Redis port
        enabled: Whether cache is enabled
    
    Returns:
        Redis cache instance
    """
    global _redis_cache
    
    if _redis_cache is None:
        _redis_cache = RedisCache(host=host, port=port, enabled=enabled)
    
    return _redis_cache


def get_translation_cache(enabled: bool = True) -> TranslationCache:
    """
    Get global translation cache instance
    
    Args:
        enabled: Whether cache is enabled
    
    Returns:
        Translation cache instance
    """
    global _translation_cache
    
    if _translation_cache is None:
        redis_cache = get_redis_cache(enabled=enabled)
        _translation_cache = TranslationCache(redis_cache=redis_cache)
    
    return _translation_cache











