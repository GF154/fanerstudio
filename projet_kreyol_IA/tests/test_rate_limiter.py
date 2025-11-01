#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for rate limiter module
"""

import pytest
import time
from src.rate_limiter import RateLimiter, TieredRateLimiter


def test_rate_limiter_basic():
    """Test basic rate limiting"""
    limiter = RateLimiter(requests_per_minute=5, requests_per_hour=20, requests_per_day=100)
    client_id = "test_client"
    
    # Should allow first 5 requests
    for i in range(5):
        allowed, retry_after = limiter.is_allowed(client_id)
        assert allowed is True
        assert retry_after is None
    
    # 6th request should be blocked
    allowed, retry_after = limiter.is_allowed(client_id)
    assert allowed is False
    assert retry_after is not None
    assert retry_after["limit"] == "minute"


def test_rate_limiter_usage():
    """Test getting usage statistics"""
    limiter = RateLimiter(requests_per_minute=10)
    client_id = "test_client"
    
    # Make 3 requests
    for _ in range(3):
        limiter.is_allowed(client_id)
    
    # Check usage
    usage = limiter.get_usage(client_id)
    
    assert usage["minute"]["used"] == 3
    assert usage["minute"]["limit"] == 10
    assert usage["minute"]["remaining"] == 7


def test_rate_limiter_reset():
    """Test resetting rate limits"""
    limiter = RateLimiter(requests_per_minute=5)
    client_id = "test_client"
    
    # Make 5 requests
    for _ in range(5):
        limiter.is_allowed(client_id)
    
    # Reset
    limiter.reset(client_id)
    
    # Should allow requests again
    allowed, _ = limiter.is_allowed(client_id)
    assert allowed is True


def test_tiered_rate_limiter():
    """Test tiered rate limiting"""
    limiter = TieredRateLimiter()
    
    # Set user tiers
    limiter.set_user_tier("free_user", "free")
    limiter.set_user_tier("pro_user", "pro")
    
    # Test free tier (10 requests/min)
    for i in range(10):
        allowed, _ = limiter.is_allowed("free_user")
        assert allowed is True
    
    # 11th request should fail
    allowed, retry_after = limiter.is_allowed("free_user")
    assert allowed is False
    
    # Pro user should have higher limits (60 requests/min)
    for i in range(60):
        allowed, _ = limiter.is_allowed("pro_user")
        assert allowed is True


def test_rate_limiter_multiple_clients():
    """Test rate limiting for multiple clients"""
    limiter = RateLimiter(requests_per_minute=3)
    
    # Client 1 makes 3 requests
    for _ in range(3):
        allowed, _ = limiter.is_allowed("client1")
        assert allowed is True
    
    # Client 1 is now blocked
    allowed, _ = limiter.is_allowed("client1")
    assert allowed is False
    
    # Client 2 should still be allowed
    allowed, _ = limiter.is_allowed("client2")
    assert allowed is True


def test_rate_limiter_weighted_cost():
    """Test rate limiting with weighted costs"""
    limiter = RateLimiter(requests_per_minute=10)
    client_id = "test_client"
    
    # Make a request with cost=5
    allowed, _ = limiter.is_allowed(client_id, cost=5)
    assert allowed is True
    
    # Check usage
    usage = limiter.get_usage(client_id)
    assert usage["minute"]["used"] == 5
    assert usage["minute"]["remaining"] == 5


def test_cleanup_old_requests():
    """Test that old request timestamps are cleaned up"""
    limiter = RateLimiter(requests_per_minute=100)
    client_id = "test_client"
    
    # Make some requests
    for _ in range(5):
        limiter.is_allowed(client_id)
    
    # Manually cleanup
    limiter._cleanup_old_requests(client_id)
    
    # Requests should still be there (not old enough)
    assert len(limiter.requests[client_id]) == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])









