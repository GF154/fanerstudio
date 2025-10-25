#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💾 Cache System
Sistèm kachaj pou amelyore pèfòmans
"""

import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Any

class SimpleCache:
    """Sistèm kachaj senp pou storaj fichye"""
    
    def __init__(self, cache_dir: str = "cache", ttl_hours: int = 24):
        """
        Inisyalize kachaj
        
        Args:
            cache_dir: Dosye pou storaj kachaj
            ttl_hours: Tan lavi kachaj an è (time-to-live)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
        print(f"✅ Cache initialized: {cache_dir} (TTL: {ttl_hours}h)")
    
    def _get_cache_key(self, data: str) -> str:
        """Jenere yon cache key soti nan done yo"""
        return hashlib.md5(data.encode('utf-8')).hexdigest()
    
    def _get_cache_path(self, key: str) -> Path:
        """Jwenn chemen fichye kachaj la"""
        return self.cache_dir / f"{key}.json"
    
    def get(self, key: str) -> Optional[Any]:
        """
        Rekipere valè soti nan kachaj
        
        Args:
            key: Cache key
            
        Returns:
            Valè ki an kachaj oswa None si li pa egziste oswa eksipe
        """
        try:
            cache_path = self._get_cache_path(key)
            
            if not cache_path.exists():
                return None
            
            # Li cache file
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Verifye si cache la eksipe
            cached_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.now() - cached_time > self.ttl:
                # Cache eksipe, efase l
                cache_path.unlink()
                return None
            
            return cache_data['value']
            
        except Exception as e:
            print(f"⚠️  Cache read error: {e}")
            return None
    
    def set(self, key: str, value: Any) -> bool:
        """
        Sove valè nan kachaj
        
        Args:
            key: Cache key
            value: Valè pou sove
            
        Returns:
            True si siksè, False si echèk
        """
        try:
            cache_path = self._get_cache_path(key)
            
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'value': value
            }
            
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"⚠️  Cache write error: {e}")
            return False
    
    def get_or_compute(self, key: str, compute_fn) -> Any:
        """
        Jwenn valè nan kachaj oswa kalkile l si li pa la
        
        Args:
            key: Cache key
            compute_fn: Fonksyon pou kalkile valè a
            
        Returns:
            Valè (swa nan kachaj oswa nouvèlman kalkile)
        """
        # Eseye jwenn nan kachaj
        cached_value = self.get(key)
        if cached_value is not None:
            print(f"💾 Cache hit: {key[:16]}...")
            return cached_value
        
        # Kalkile valè a
        print(f"🔄 Cache miss, computing: {key[:16]}...")
        value = compute_fn()
        
        # Sove nan kachaj
        self.set(key, value)
        
        return value
    
    def clear(self) -> int:
        """
        Efase tout kachaj la
        
        Returns:
            Kantite fichye ki efase
        """
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
                count += 1
            except Exception as e:
                print(f"⚠️  Error deleting {cache_file}: {e}")
        
        print(f"🗑️  Cleared {count} cache files")
        return count
    
    def clear_expired(self) -> int:
        """
        Efase sèlman kachaj ki eksipe yo
        
        Returns:
            Kantite fichye ki efase
        """
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                cached_time = datetime.fromisoformat(cache_data['timestamp'])
                if datetime.now() - cached_time > self.ttl:
                    cache_file.unlink()
                    count += 1
                    
            except Exception as e:
                print(f"⚠️  Error checking {cache_file}: {e}")
        
        print(f"🗑️  Cleared {count} expired cache files")
        return count
    
    def get_stats(self) -> dict:
        """
        Jwenn estatistik kachaj la
        
        Returns:
            dict ak enfòmasyon sou kachaj la
        """
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        expired_count = 0
        for cache_file in cache_files:
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                cached_time = datetime.fromisoformat(cache_data['timestamp'])
                if datetime.now() - cached_time > self.ttl:
                    expired_count += 1
            except:
                pass
        
        return {
            "total_entries": len(cache_files),
            "expired_entries": expired_count,
            "valid_entries": len(cache_files) - expired_count,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "cache_dir": str(self.cache_dir),
            "ttl_hours": self.ttl.total_seconds() / 3600
        }


# Global cache instance for translations
translation_cache = SimpleCache(cache_dir="cache/translations", ttl_hours=168)  # 1 week

# Global cache instance for audio
audio_cache = SimpleCache(cache_dir="cache/audio", ttl_hours=72)  # 3 days


def cached_translation(text: str, source_lang: str, target_lang: str, translate_fn) -> str:
    """
    Helper pou tradwi ak kachaj
    
    Args:
        text: Tèks pou tradwi
        source_lang: Lang sous
        target_lang: Lang sib
        translate_fn: Fonksyon tradiksyon
        
    Returns:
        Tèks ki tradwi
    """
    # Kreye cache key
    cache_data = f"{source_lang}:{target_lang}:{text}"
    cache_key = translation_cache._get_cache_key(cache_data)
    
    # Get or compute
    return translation_cache.get_or_compute(
        cache_key,
        lambda: translate_fn(text, source_lang, target_lang)
    )


if __name__ == "__main__":
    # Test cache system
    print("🧪 Testing cache system...")
    
    cache = SimpleCache("cache/test", ttl_hours=1)
    
    # Test set/get
    cache.set("test_key", "test_value")
    value = cache.get("test_key")
    print(f"✅ Set/Get test: {value}")
    
    # Test get_or_compute
    result = cache.get_or_compute(
        "computed_key",
        lambda: "This was computed!"
    )
    print(f"✅ Computed: {result}")
    
    # Test stats
    stats = cache.get_stats()
    print(f"📊 Stats: {stats}")
    
    # Test clear
    count = cache.clear()
    print(f"✅ Cleared {count} entries")
    
    print("✅ All tests passed!")

