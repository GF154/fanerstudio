#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rate Limiting Module
Protect API from abuse with rate limiting
"""

import logging
import time
from typing import Dict, Optional, Tuple
from collections import defaultdict
from datetime import datetime, timedelta
from threading import Lock

logger = logging.getLogger('KreyolAI.RateLimiter')


class RateLimiter:
    """
    Rate limiter using sliding window algorithm
    """
    
    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        requests_per_day: int = 10000
    ):
        """
        Initialize rate limiter
        
        Args:
            requests_per_minute: Max requests per minute
            requests_per_hour: Max requests per hour
            requests_per_day: Max requests per day
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.requests_per_day = requests_per_day
        
        # Storage for request timestamps
        self.requests: Dict[str, list] = defaultdict(list)
        self.lock = Lock()
        
        logger.info(
            f"Rate limiter initialized: "
            f"{requests_per_minute}/min, "
            f"{requests_per_hour}/hr, "
            f"{requests_per_day}/day"
        )
    
    def _cleanup_old_requests(self, client_id: str):
        """
        Remove old request timestamps
        
        Args:
            client_id: Client identifier
        """
        now = time.time()
        day_ago = now - 86400  # 24 hours
        
        # Keep only requests from last 24 hours
        self.requests[client_id] = [
            ts for ts in self.requests[client_id]
            if ts > day_ago
        ]
    
    def is_allowed(
        self,
        client_id: str,
        cost: int = 1
    ) -> Tuple[bool, Optional[Dict[str, int]]]:
        """
        Check if request is allowed
        
        Args:
            client_id: Client identifier (IP, user ID, API key)
            cost: Request cost (for weighted rate limiting)
        
        Returns:
            Tuple of (allowed: bool, retry_after: Optional[Dict])
        """
        with self.lock:
            now = time.time()
            
            # Cleanup old requests
            self._cleanup_old_requests(client_id)
            
            # Get request timestamps
            timestamps = self.requests[client_id]
            
            # Check limits
            minute_ago = now - 60
            hour_ago = now - 3600
            day_ago = now - 86400
            
            requests_last_minute = sum(1 for ts in timestamps if ts > minute_ago)
            requests_last_hour = sum(1 for ts in timestamps if ts > hour_ago)
            requests_last_day = sum(1 for ts in timestamps if ts > day_ago)
            
            # Check if any limit is exceeded
            if requests_last_minute >= self.requests_per_minute:
                retry_after = {
                    "seconds": int(60 - (now - timestamps[-self.requests_per_minute])),
                    "limit": "minute",
                    "current": requests_last_minute,
                    "max": self.requests_per_minute
                }
                logger.warning(
                    f"Rate limit exceeded for {client_id}: "
                    f"{requests_last_minute}/{self.requests_per_minute} per minute"
                )
                return False, retry_after
            
            if requests_last_hour >= self.requests_per_hour:
                retry_after = {
                    "seconds": int(3600 - (now - timestamps[-self.requests_per_hour])),
                    "limit": "hour",
                    "current": requests_last_hour,
                    "max": self.requests_per_hour
                }
                logger.warning(
                    f"Rate limit exceeded for {client_id}: "
                    f"{requests_last_hour}/{self.requests_per_hour} per hour"
                )
                return False, retry_after
            
            if requests_last_day >= self.requests_per_day:
                retry_after = {
                    "seconds": int(86400 - (now - timestamps[-self.requests_per_day])),
                    "limit": "day",
                    "current": requests_last_day,
                    "max": self.requests_per_day
                }
                logger.warning(
                    f"Rate limit exceeded for {client_id}: "
                    f"{requests_last_day}/{self.requests_per_day} per day"
                )
                return False, retry_after
            
            # Request allowed - record it
            for _ in range(cost):
                self.requests[client_id].append(now)
            
            return True, None
    
    def get_usage(self, client_id: str) -> Dict[str, any]:
        """
        Get current usage for client
        
        Args:
            client_id: Client identifier
        
        Returns:
            Dictionary with usage statistics
        """
        with self.lock:
            now = time.time()
            self._cleanup_old_requests(client_id)
            
            timestamps = self.requests[client_id]
            
            minute_ago = now - 60
            hour_ago = now - 3600
            day_ago = now - 86400
            
            requests_last_minute = sum(1 for ts in timestamps if ts > minute_ago)
            requests_last_hour = sum(1 for ts in timestamps if ts > hour_ago)
            requests_last_day = sum(1 for ts in timestamps if ts > day_ago)
            
            return {
                "minute": {
                    "used": requests_last_minute,
                    "limit": self.requests_per_minute,
                    "remaining": max(0, self.requests_per_minute - requests_last_minute),
                    "reset_in": 60
                },
                "hour": {
                    "used": requests_last_hour,
                    "limit": self.requests_per_hour,
                    "remaining": max(0, self.requests_per_hour - requests_last_hour),
                    "reset_in": 3600
                },
                "day": {
                    "used": requests_last_day,
                    "limit": self.requests_per_day,
                    "remaining": max(0, self.requests_per_day - requests_last_day),
                    "reset_in": 86400
                }
            }
    
    def reset(self, client_id: Optional[str] = None):
        """
        Reset rate limits
        
        Args:
            client_id: Client to reset (None for all)
        """
        with self.lock:
            if client_id:
                self.requests[client_id] = []
                logger.info(f"Rate limit reset for: {client_id}")
            else:
                self.requests.clear()
                logger.info("All rate limits reset")


class TieredRateLimiter(RateLimiter):
    """
    Rate limiter with different tiers for different user types
    """
    
    TIERS = {
        "free": {
            "requests_per_minute": 10,
            "requests_per_hour": 100,
            "requests_per_day": 1000
        },
        "basic": {
            "requests_per_minute": 30,
            "requests_per_hour": 500,
            "requests_per_day": 5000
        },
        "pro": {
            "requests_per_minute": 60,
            "requests_per_hour": 2000,
            "requests_per_day": 20000
        },
        "enterprise": {
            "requests_per_minute": 200,
            "requests_per_hour": 10000,
            "requests_per_day": 100000
        }
    }
    
    def __init__(self):
        """Initialize tiered rate limiter"""
        # Default to free tier
        super().__init__(**self.TIERS["free"])
        self.user_tiers: Dict[str, str] = {}
        logger.info("Tiered rate limiter initialized")
    
    def set_user_tier(self, user_id: str, tier: str):
        """
        Set user tier
        
        Args:
            user_id: User identifier
            tier: Tier name (free, basic, pro, enterprise)
        
        Raises:
            ValueError: If tier is invalid
        """
        if tier not in self.TIERS:
            raise ValueError(f"Invalid tier: {tier}. Must be one of {list(self.TIERS.keys())}")
        
        self.user_tiers[user_id] = tier
        logger.info(f"User {user_id} set to tier: {tier}")
    
    def get_user_tier(self, user_id: str) -> str:
        """
        Get user tier
        
        Args:
            user_id: User identifier
        
        Returns:
            Tier name
        """
        return self.user_tiers.get(user_id, "free")
    
    def is_allowed(
        self,
        client_id: str,
        cost: int = 1
    ) -> Tuple[bool, Optional[Dict[str, int]]]:
        """
        Check if request is allowed based on user tier
        
        Args:
            client_id: Client identifier
            cost: Request cost
        
        Returns:
            Tuple of (allowed: bool, retry_after: Optional[Dict])
        """
        # Get user tier
        tier = self.get_user_tier(client_id)
        tier_limits = self.TIERS[tier]
        
        # Temporarily set limits for this user
        original_limits = (
            self.requests_per_minute,
            self.requests_per_hour,
            self.requests_per_day
        )
        
        self.requests_per_minute = tier_limits["requests_per_minute"]
        self.requests_per_hour = tier_limits["requests_per_hour"]
        self.requests_per_day = tier_limits["requests_per_day"]
        
        # Check rate limit
        result = super().is_allowed(client_id, cost)
        
        # Restore original limits
        self.requests_per_minute, self.requests_per_hour, self.requests_per_day = original_limits
        
        return result


# Global rate limiter instance
_rate_limiter = None


def get_rate_limiter(tiered: bool = False) -> RateLimiter:
    """
    Get global rate limiter instance
    
    Args:
        tiered: Whether to use tiered rate limiter
    
    Returns:
        Rate limiter instance
    """
    global _rate_limiter
    
    if _rate_limiter is None:
        if tiered:
            _rate_limiter = TieredRateLimiter()
        else:
            _rate_limiter = RateLimiter()
    
    return _rate_limiter












