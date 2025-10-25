#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛠️ Utility Functions
Fonksyon itil pou tout aplikasyon an
"""

from pathlib import Path
from datetime import datetime
import uuid
import hashlib

def generate_unique_filename(prefix: str = "", extension: str = "") -> str:
    """
    Jenere yon non fichye inik
    
    Args:
        prefix: Prefiks pou non fichye a
        extension: Extension fichye a
        
    Returns:
        str: Non fichye inik
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = uuid.uuid4().hex[:8]
    
    if prefix:
        filename = f"{prefix}_{timestamp}_{unique_id}"
    else:
        filename = f"{timestamp}_{unique_id}"
    
    if extension:
        if not extension.startswith('.'):
            extension = f".{extension}"
        filename += extension
    
    return filename

def calculate_file_hash(file_path: Path) -> str:
    """
    Kalkile hash MD5 yon fichye
    
    Args:
        file_path: Chemen fichye a
        
    Returns:
        str: Hash MD5 fichye a
    """
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def format_file_size(size_bytes: int) -> str:
    """
    Fòmate gwosè fichye an fòma lisib
    
    Args:
        size_bytes: Gwosè an bytes
        
    Returns:
        str: Gwosè fòmate (ex: "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"

def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """
    Valide extension yon fichye
    
    Args:
        filename: Non fichye a
        allowed_extensions: Lis extension ki otorize
        
    Returns:
        bool: True si extension valid
    """
    file_ext = Path(filename).suffix.lower()
    return file_ext in [ext.lower() if ext.startswith('.') else f".{ext.lower()}" for ext in allowed_extensions]

def sanitize_filename(filename: str) -> str:
    """
    Netwaye non fichye pou retire karaktè pa valid
    
    Args:
        filename: Non fichye orijinal
        
    Returns:
        str: Non fichye netwaye
    """
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    return filename

def get_file_info(file_path: Path) -> dict:
    """
    Jwenn enfòmasyon sou yon fichye
    
    Args:
        file_path: Chemen fichye a
        
    Returns:
        dict: Enfòmasyon sou fichye a
    """
    if not file_path.exists():
        return None
    
    stat = file_path.stat()
    
    return {
        "name": file_path.name,
        "size": format_file_size(stat.st_size),
        "size_bytes": stat.st_size,
        "extension": file_path.suffix,
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "hash": calculate_file_hash(file_path)
    }

