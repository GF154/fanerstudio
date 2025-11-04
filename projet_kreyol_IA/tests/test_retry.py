#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for retry logic module
"""

import pytest
import time
from src.retry import (
    retry_with_backoff,
    RetryStrategy,
    RetryableOperation,
    retry_call
)


def test_retry_successful():
    """Test retry with successful function"""
    call_count = 0
    
    @retry_with_backoff(max_attempts=3, initial_delay=0.1)
    def successful_function():
        nonlocal call_count
        call_count += 1
        return "success"
    
    result = successful_function()
    
    assert result == "success"
    assert call_count == 1  # Should succeed on first attempt


def test_retry_with_failures():
    """Test retry with some failures"""
    call_count = 0
    
    @retry_with_backoff(max_attempts=3, initial_delay=0.1)
    def failing_then_succeeding():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("Temporary failure")
        return "success"
    
    result = failing_then_succeeding()
    
    assert result == "success"
    assert call_count == 3  # Should succeed on third attempt


def test_retry_max_attempts_exceeded():
    """Test retry fails after max attempts"""
    call_count = 0
    
    @retry_with_backoff(max_attempts=3, initial_delay=0.1)
    def always_failing():
        nonlocal call_count
        call_count += 1
        raise ValueError("Always fails")
    
    with pytest.raises(ValueError):
        always_failing()
    
    assert call_count == 3  # Should have tried 3 times


def test_retry_exponential_backoff():
    """Test exponential backoff strategy"""
    call_times = []
    
    @retry_with_backoff(
        max_attempts=3,
        initial_delay=0.1,
        strategy=RetryStrategy.EXPONENTIAL
    )
    def failing_function():
        call_times.append(time.time())
        raise ValueError("Test failure")
    
    with pytest.raises(ValueError):
        failing_function()
    
    # Check that delays increase exponentially
    assert len(call_times) == 3
    
    # First retry should be after ~0.1s
    if len(call_times) >= 2:
        delay1 = call_times[1] - call_times[0]
        assert 0.05 < delay1 < 0.2
    
    # Second retry should be after ~0.2s
    if len(call_times) >= 3:
        delay2 = call_times[2] - call_times[1]
        assert 0.15 < delay2 < 0.3


def test_retry_linear_backoff():
    """Test linear backoff strategy"""
    call_times = []
    
    @retry_with_backoff(
        max_attempts=3,
        initial_delay=0.1,
        strategy=RetryStrategy.LINEAR
    )
    def failing_function():
        call_times.append(time.time())
        raise ValueError("Test failure")
    
    with pytest.raises(ValueError):
        failing_function()
    
    assert len(call_times) == 3


def test_retry_constant_backoff():
    """Test constant backoff strategy"""
    call_times = []
    
    @retry_with_backoff(
        max_attempts=3,
        initial_delay=0.1,
        strategy=RetryStrategy.CONSTANT
    )
    def failing_function():
        call_times.append(time.time())
        raise ValueError("Test failure")
    
    with pytest.raises(ValueError):
        failing_function()
    
    assert len(call_times) == 3


def test_retry_specific_exceptions():
    """Test retrying only specific exceptions"""
    call_count = 0
    
    @retry_with_backoff(
        max_attempts=3,
        initial_delay=0.1,
        exceptions=(ValueError,)
    )
    def function_with_specific_error():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise ValueError("Retry this")
        elif call_count == 2:
            raise TypeError("Don't retry this")
        return "success"
    
    with pytest.raises(TypeError):
        function_with_specific_error()
    
    assert call_count == 2  # Should stop after TypeError


def test_retry_callback():
    """Test retry callback function"""
    callback_calls = []
    
    def on_retry(attempt, delay, error):
        callback_calls.append((attempt, delay, str(error)))
    
    @retry_with_backoff(
        max_attempts=3,
        initial_delay=0.1,
        on_retry=on_retry
    )
    def failing_function():
        raise ValueError("Test error")
    
    with pytest.raises(ValueError):
        failing_function()
    
    # Callback should be called twice (after attempt 1 and 2)
    assert len(callback_calls) == 2


def test_retryable_operation_context():
    """Test RetryableOperation context manager"""
    call_count = 0
    
    def unstable_operation():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("Not ready yet")
        return "success"
    
    with RetryableOperation(max_attempts=3, initial_delay=0.1) as retry:
        result = retry.execute(unstable_operation)
    
    assert result == "success"
    assert call_count == 3


def test_retry_call_helper():
    """Test retry_call helper function"""
    call_count = 0
    
    def unstable_function():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise ValueError("Try again")
        return "success"
    
    result = retry_call(unstable_function, max_attempts=3, delay=0.1)
    
    assert result == "success"
    assert call_count == 2


def test_retry_max_delay():
    """Test that retry delay is capped at max_delay"""
    call_times = []
    
    @retry_with_backoff(
        max_attempts=5,
        initial_delay=1.0,
        max_delay=2.0,
        exponential_base=10.0  # Would normally create huge delays
    )
    def failing_function():
        call_times.append(time.time())
        raise ValueError("Test failure")
    
    with pytest.raises(ValueError):
        failing_function()
    
    # Check that no delay exceeds max_delay
    for i in range(1, len(call_times)):
        delay = call_times[i] - call_times[i-1]
        assert delay <= 2.5  # Max delay + some tolerance


if __name__ == "__main__":
    pytest.main([__file__, "-v"])











