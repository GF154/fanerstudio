#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Logger
Sistèm Log Amelyore
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Colored log formatter for console output"""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        """Format log record with colors"""
        # Add color to level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        return super().format(record)


def setup_logger(
    name: str = 'KreyolAI',
    log_dir: Optional[Path] = None,
    log_level: str = 'INFO',
    console_output: bool = True,
    file_output: bool = True,
    colored_console: bool = True
) -> logging.Logger:
    """
    Setup enhanced logger
    
    Args:
        name: Logger name
        log_dir: Directory for log files
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console_output: Enable console output
        file_output: Enable file output
        colored_console: Use colored output in console
    
    Returns:
        Configured logger
    """
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Format strings
    detailed_format = '%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s'
    simple_format = '%(levelname)s | %(message)s'
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        if colored_console and sys.stdout.isatty():
            console_formatter = ColoredFormatter(simple_format)
        else:
            console_formatter = logging.Formatter(simple_format)
        
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if file_output:
        if log_dir is None:
            log_dir = Path('logs')
        
        log_dir = Path(log_dir)
        log_dir.mkdir(exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'{name}_{timestamp}.log'
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # Log everything to file
        file_formatter = logging.Formatter(detailed_format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        logger.debug(f"Log file created: {log_file}")
    
    return logger


class LoggerContext:
    """Context manager for temporary log level changes"""
    
    def __init__(self, logger: logging.Logger, level: str):
        """
        Initialize context
        
        Args:
            logger: Logger instance
            level: Temporary log level
        """
        self.logger = logger
        self.new_level = getattr(logging, level.upper())
        self.old_level = logger.level
    
    def __enter__(self):
        """Enter context - change log level"""
        self.logger.setLevel(self.new_level)
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context - restore log level"""
        self.logger.setLevel(self.old_level)


def log_function_call(logger: logging.Logger):
    """Decorator to log function calls"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"{func.__name__} completed successfully")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} failed with error: {e}")
                raise
        return wrapper
    return decorator


# Example usage
if __name__ == "__main__":
    # Setup logger
    logger = setup_logger(
        name='TestLogger',
        log_level='DEBUG',
        console_output=True,
        file_output=True,
        colored_console=True
    )
    
    # Test different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    # Test context manager
    with LoggerContext(logger, 'WARNING'):
        logger.info("This won't be shown (level is WARNING)")
        logger.warning("This will be shown")
    
    # Test decorator
    @log_function_call(logger)
    def test_function(x, y):
        return x + y
    
    result = test_function(5, 3)
    logger.info(f"Result: {result}")

