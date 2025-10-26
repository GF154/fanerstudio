#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retry Logic Module
Automatic retry with exponential backoff for transient failures
"""

import logging
import time
import functools
from typing import Callable, Optional, Tuple, Type
from enum import Enum

logger = logging.getLogger('KreyolAI.Retry')


class RetryStrategy(Enum):
    """Retry strategy types"""
    EXPONENTIAL = "exponential"  # Exponential backoff
    LINEAR = "linear"  # Linear backoff
    CONSTANT = "constant"  # Constant delay


def retry_with_backoff(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable] = None
):
    """
    Decorator for retrying functions with configurable backoff
    
    Args:
        max_attempts: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff
        strategy: Retry strategy (exponential, linear, constant)
        exceptions: Tuple of exceptions to retry on
        on_retry: Callback function called on each retry
    
    Returns:
        Decorated function
    
    Example:
        @retry_with_backoff(max_attempts=3, initial_delay=1.0)
        def unstable_function():
            # Function that might fail
            pass
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            delay = initial_delay
            
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                    
                except exceptions as e:
                    attempt += 1
                    
                    if attempt >= max_attempts:
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts: {e}"
                        )
                        raise
                    
                    # Calculate delay based on strategy
                    if strategy == RetryStrategy.EXPONENTIAL:
                        delay = min(initial_delay * (exponential_base ** (attempt - 1)), max_delay)
                    elif strategy == RetryStrategy.LINEAR:
                        delay = min(initial_delay * attempt, max_delay)
                    else:  # CONSTANT
                        delay = initial_delay
                    
                    logger.warning(
                        f"{func.__name__} failed (attempt {attempt}/{max_attempts}): {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    
                    # Call retry callback if provided
                    if on_retry:
                        try:
                            on_retry(attempt, delay, e)
                        except Exception as callback_error:
                            logger.error(f"Retry callback error: {callback_error}")
                    
                    time.sleep(delay)
            
            # This should never be reached, but just in case
            raise RuntimeError(f"{func.__name__} failed after all retries")
        
        return wrapper
    return decorator


def retry_async_with_backoff(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable] = None
):
    """
    Async decorator for retrying functions with configurable backoff
    
    Args:
        max_attempts: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential backoff
        strategy: Retry strategy
        exceptions: Tuple of exceptions to retry on
        on_retry: Callback function called on each retry
    
    Returns:
        Decorated async function
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            import asyncio
            
            attempt = 0
            delay = initial_delay
            
            while attempt < max_attempts:
                try:
                    return await func(*args, **kwargs)
                    
                except exceptions as e:
                    attempt += 1
                    
                    if attempt >= max_attempts:
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts: {e}"
                        )
                        raise
                    
                    # Calculate delay
                    if strategy == RetryStrategy.EXPONENTIAL:
                        delay = min(initial_delay * (exponential_base ** (attempt - 1)), max_delay)
                    elif strategy == RetryStrategy.LINEAR:
                        delay = min(initial_delay * attempt, max_delay)
                    else:
                        delay = initial_delay
                    
                    logger.warning(
                        f"{func.__name__} failed (attempt {attempt}/{max_attempts}): {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    
                    if on_retry:
                        try:
                            if asyncio.iscoroutinefunction(on_retry):
                                await on_retry(attempt, delay, e)
                            else:
                                on_retry(attempt, delay, e)
                        except Exception as callback_error:
                            logger.error(f"Retry callback error: {callback_error}")
                    
                    await asyncio.sleep(delay)
            
            raise RuntimeError(f"{func.__name__} failed after all retries")
        
        return wrapper
    return decorator


class RetryableOperation:
    """
    Context manager for retryable operations
    
    Example:
        with RetryableOperation(max_attempts=3) as retry:
            result = retry.execute(lambda: risky_operation())
    """
    
    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        strategy: RetryStrategy = RetryStrategy.EXPONENTIAL,
        exceptions: Tuple[Type[Exception], ...] = (Exception,)
    ):
        """
        Initialize retryable operation context
        
        Args:
            max_attempts: Maximum retry attempts
            initial_delay: Initial delay in seconds
            max_delay: Maximum delay in seconds
            strategy: Retry strategy
            exceptions: Exceptions to retry on
        """
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.strategy = strategy
        self.exceptions = exceptions
        self.attempt = 0
    
    def __enter__(self):
        """Enter context"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context"""
        return False  # Don't suppress exceptions
    
    def execute(self, func: Callable, *args, **kwargs):
        """
        Execute function with retry logic
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
        
        Returns:
            Function result
        
        Raises:
            Exception if all retries fail
        """
        self.attempt = 0
        delay = self.initial_delay
        
        while self.attempt < self.max_attempts:
            try:
                return func(*args, **kwargs)
                
            except self.exceptions as e:
                self.attempt += 1
                
                if self.attempt >= self.max_attempts:
                    logger.error(
                        f"Operation failed after {self.max_attempts} attempts: {e}"
                    )
                    raise
                
                # Calculate delay
                if self.strategy == RetryStrategy.EXPONENTIAL:
                    delay = min(self.initial_delay * (2 ** (self.attempt - 1)), self.max_delay)
                elif self.strategy == RetryStrategy.LINEAR:
                    delay = min(self.initial_delay * self.attempt, self.max_delay)
                else:
                    delay = self.initial_delay
                
                logger.warning(
                    f"Operation failed (attempt {self.attempt}/{self.max_attempts}): {e}. "
                    f"Retrying in {delay:.2f}s..."
                )
                
                time.sleep(delay)
        
        raise RuntimeError("Operation failed after all retries")


# Predefined retry decorators for common scenarios

def retry_on_network_error(max_attempts: int = 3):
    """
    Retry decorator for network-related errors
    
    Args:
        max_attempts: Maximum retry attempts
    
    Returns:
        Decorator function
    """
    import requests
    
    return retry_with_backoff(
        max_attempts=max_attempts,
        initial_delay=2.0,
        max_delay=30.0,
        exceptions=(
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException,
        )
    )


def retry_on_rate_limit(max_attempts: int = 5):
    """
    Retry decorator for rate limit errors
    
    Args:
        max_attempts: Maximum retry attempts
    
    Returns:
        Decorator function
    """
    return retry_with_backoff(
        max_attempts=max_attempts,
        initial_delay=5.0,
        max_delay=300.0,  # 5 minutes
        strategy=RetryStrategy.EXPONENTIAL,
        exponential_base=3.0,  # Aggressive backoff
        exceptions=(Exception,)  # Customize based on your rate limit exception
    )


def retry_on_database_error(max_attempts: int = 3):
    """
    Retry decorator for database errors
    
    Args:
        max_attempts: Maximum retry attempts
    
    Returns:
        Decorator function
    """
    import sqlite3
    
    return retry_with_backoff(
        max_attempts=max_attempts,
        initial_delay=1.0,
        max_delay=10.0,
        exceptions=(
            sqlite3.OperationalError,
            sqlite3.DatabaseError,
        )
    )


# Helper function for manual retry logic
def retry_call(
    func: Callable,
    *args,
    max_attempts: int = 3,
    delay: float = 1.0,
    **kwargs
):
    """
    Retry a function call manually
    
    Args:
        func: Function to call
        *args: Function arguments
        max_attempts: Maximum retry attempts
        delay: Delay between retries
        **kwargs: Function keyword arguments
    
    Returns:
        Function result
    
    Example:
        result = retry_call(my_function, arg1, arg2, max_attempts=3)
    """
    for attempt in range(max_attempts):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
            time.sleep(delay)







