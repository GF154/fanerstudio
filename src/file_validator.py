#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Upload Validation Module
Secure file upload validation with multiple security checks
"""

import logging
import hashlib
from pathlib import Path
from typing import Optional, Tuple
from fastapi import UploadFile, HTTPException
import magic  # python-magic for MIME type detection

logger = logging.getLogger('KreyolAI.FileValidator')


class FileValidator:
    """
    Secure file upload validator with multiple security layers
    """
    
    # Dangerous file extensions to always block
    DANGEROUS_EXTENSIONS = {
        '.exe', '.bat', '.cmd', '.com', '.pif', '.scr', '.vbs', '.js',
        '.jar', '.app', '.deb', '.rpm', '.dmg', '.pkg', '.sh', '.csh',
        '.pl', '.py', '.rb', '.php', '.asp', '.aspx', '.jsp'
    }
    
    def __init__(self, 
                 allowed_extensions: list = None,
                 allowed_mime_types: list = None,
                 max_size_mb: int = 10,
                 scan_content: bool = True):
        """
        Initialize file validator
        
        Args:
            allowed_extensions: List of allowed file extensions (e.g., ['.pdf', '.txt'])
            allowed_mime_types: List of allowed MIME types
            max_size_mb: Maximum file size in MB
            scan_content: Whether to scan file content
        """
        self.allowed_extensions = set(allowed_extensions or ['.pdf', '.txt', '.docx'])
        self.allowed_mime_types = set(allowed_mime_types or [
            'application/pdf',
            'text/plain',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ])
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.scan_content = scan_content
        
        logger.info(f"FileValidator initialized: max_size={max_size_mb}MB, "
                   f"allowed_extensions={self.allowed_extensions}")
    
    async def validate(self, file: UploadFile, read_content: bool = True) -> Tuple[bytes, str]:
        """
        Validate uploaded file with comprehensive security checks
        
        Args:
            file: FastAPI UploadFile object
            read_content: Whether to read and return file content
        
        Returns:
            Tuple of (file_content, file_hash)
        
        Raises:
            HTTPException: If validation fails
        """
        try:
            # 1. Check filename
            self._validate_filename(file.filename)
            
            # 2. Check extension
            self._validate_extension(file.filename)
            
            # 3. Read content
            content = await file.read()
            
            # 4. Check size
            self._validate_size(len(content), file.filename)
            
            # 5. Check MIME type
            await self._validate_mime_type(content, file.filename)
            
            # 6. Scan content for suspicious patterns
            if self.scan_content:
                self._scan_content(content, file.filename)
            
            # 7. Calculate hash for tracking/deduplication
            file_hash = self._calculate_hash(content)
            
            # Reset file pointer for subsequent reads
            await file.seek(0)
            
            logger.info(f"File validated successfully: {file.filename} "
                       f"({len(content)} bytes, hash={file_hash[:16]}...)")
            
            return content if read_content else b'', file_hash
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected validation error for {file.filename}: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"File validation error: {str(e)}"
            )
    
    def _validate_filename(self, filename: str):
        """
        Validate filename for security issues
        
        Args:
            filename: Name of the file
        
        Raises:
            HTTPException: If filename is invalid
        """
        if not filename:
            raise HTTPException(
                status_code=400,
                detail="Filename cannot be empty"
            )
        
        # Check for path traversal attempts
        if '..' in filename or '/' in filename or '\\' in filename:
            logger.warning(f"Path traversal attempt detected: {filename}")
            raise HTTPException(
                status_code=400,
                detail="Invalid filename: path traversal not allowed"
            )
        
        # Check for null bytes
        if '\x00' in filename:
            logger.warning(f"Null byte detected in filename: {filename}")
            raise HTTPException(
                status_code=400,
                detail="Invalid filename: null bytes not allowed"
            )
        
        # Check length
        if len(filename) > 255:
            raise HTTPException(
                status_code=400,
                detail="Filename too long (max 255 characters)"
            )
    
    def _validate_extension(self, filename: str):
        """
        Validate file extension
        
        Args:
            filename: Name of the file
        
        Raises:
            HTTPException: If extension is not allowed
        """
        ext = Path(filename).suffix.lower()
        
        # Check for dangerous extensions
        if ext in self.DANGEROUS_EXTENSIONS:
            logger.warning(f"Dangerous file extension detected: {filename}")
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed: {ext}"
            )
        
        # Check against allowed extensions
        if ext not in self.allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File extension '{ext}' not allowed. "
                       f"Allowed: {', '.join(self.allowed_extensions)}"
            )
    
    def _validate_size(self, size: int, filename: str):
        """
        Validate file size
        
        Args:
            size: File size in bytes
            filename: Name of the file
        
        Raises:
            HTTPException: If file is too large
        """
        if size == 0:
            raise HTTPException(
                status_code=400,
                detail="File is empty"
            )
        
        if size > self.max_size_bytes:
            size_mb = size / (1024 * 1024)
            max_mb = self.max_size_bytes / (1024 * 1024)
            logger.warning(f"File too large: {filename} ({size_mb:.2f}MB > {max_mb}MB)")
            raise HTTPException(
                status_code=413,
                detail=f"File too large: {size_mb:.2f}MB (max: {max_mb}MB)"
            )
    
    async def _validate_mime_type(self, content: bytes, filename: str):
        """
        Validate MIME type using python-magic
        
        Args:
            content: File content bytes
            filename: Name of the file
        
        Raises:
            HTTPException: If MIME type is not allowed
        """
        try:
            # Detect MIME type from content
            mime_type = magic.from_buffer(content, mime=True)
            
            if mime_type not in self.allowed_mime_types:
                logger.warning(f"Invalid MIME type for {filename}: {mime_type}")
                raise HTTPException(
                    status_code=400,
                    detail=f"File content type '{mime_type}' not allowed. "
                           f"Allowed: {', '.join(self.allowed_mime_types)}"
                )
            
            logger.debug(f"MIME type validated: {filename} -> {mime_type}")
            
        except ImportError:
            logger.warning("python-magic not installed, skipping MIME validation")
        except Exception as e:
            logger.error(f"MIME validation error for {filename}: {e}")
            # Don't fail validation if MIME check fails, but log it
    
    def _scan_content(self, content: bytes, filename: str):
        """
        Scan file content for suspicious patterns
        
        Args:
            content: File content bytes
            filename: Name of the file
        
        Raises:
            HTTPException: If suspicious content detected
        """
        # Check for common exploit signatures
        suspicious_patterns = [
            b'<script',  # JavaScript injection
            b'<?php',    # PHP code
            b'<%',       # ASP/JSP code
            b'eval(',    # Code execution
            b'exec(',    # Code execution
            b'system(',  # System commands
        ]
        
        content_lower = content.lower()
        
        for pattern in suspicious_patterns:
            if pattern in content_lower:
                logger.warning(f"Suspicious content detected in {filename}: {pattern}")
                raise HTTPException(
                    status_code=400,
                    detail="File contains suspicious content"
                )
    
    def _calculate_hash(self, content: bytes) -> str:
        """
        Calculate SHA256 hash of file content
        
        Args:
            content: File content bytes
        
        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(content).hexdigest()
    
    def validate_path(self, file_path: Path) -> bool:
        """
        Validate an existing file path
        
        Args:
            file_path: Path to file
        
        Returns:
            True if valid
        
        Raises:
            HTTPException: If validation fails
        """
        file_path = Path(file_path)
        
        # Check existence
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"File not found: {file_path.name}"
            )
        
        # Check if it's a file
        if not file_path.is_file():
            raise HTTPException(
                status_code=400,
                detail=f"Not a file: {file_path.name}"
            )
        
        # Validate extension
        self._validate_extension(file_path.name)
        
        # Validate size
        size = file_path.stat().st_size
        self._validate_size(size, file_path.name)
        
        return True


class PDFValidator(FileValidator):
    """Specialized validator for PDF files"""
    
    def __init__(self, max_size_mb: int = 50, max_pages: int = 500):
        super().__init__(
            allowed_extensions=['.pdf'],
            allowed_mime_types=['application/pdf'],
            max_size_mb=max_size_mb
        )
        self.max_pages = max_pages
    
    async def validate_pdf(self, file: UploadFile) -> Tuple[bytes, str, int]:
        """
        Validate PDF file and return content, hash, and page count
        
        Returns:
            Tuple of (content, hash, page_count)
        """
        content, file_hash = await self.validate(file)
        
        # Check page count
        try:
            from pypdf import PdfReader
            import io
            
            pdf_reader = PdfReader(io.BytesIO(content))
            page_count = len(pdf_reader.pages)
            
            if page_count > self.max_pages:
                raise HTTPException(
                    status_code=413,
                    detail=f"PDF has too many pages: {page_count} (max: {self.max_pages})"
                )
            
            logger.info(f"PDF validated: {file.filename} ({page_count} pages)")
            return content, file_hash, page_count
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"PDF validation error: {e}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid PDF file: {str(e)}"
            )


# Convenience functions for common use cases

async def validate_file_upload(
    file: UploadFile,
    allowed_extensions: list = None,
    max_size_mb: int = 10
) -> Tuple[bytes, str]:
    """
    Quick file validation helper
    
    Args:
        file: Uploaded file
        allowed_extensions: List of allowed extensions
        max_size_mb: Maximum size in MB
    
    Returns:
        Tuple of (content, hash)
    """
    validator = FileValidator(
        allowed_extensions=allowed_extensions,
        max_size_mb=max_size_mb
    )
    return await validator.validate(file)


async def validate_pdf_upload(
    file: UploadFile,
    max_size_mb: int = 50,
    max_pages: int = 500
) -> Tuple[bytes, str, int]:
    """
    Quick PDF validation helper
    
    Args:
        file: Uploaded PDF file
        max_size_mb: Maximum size in MB
        max_pages: Maximum number of pages
    
    Returns:
        Tuple of (content, hash, page_count)
    """
    validator = PDFValidator(max_size_mb=max_size_mb, max_pages=max_pages)
    return await validator.validate_pdf(file)


if __name__ == "__main__":
    """Test file validator"""
    print("=" * 60)
    print("🔒 File Validator - Security Tests")
    print("=" * 60)
    
    validator = FileValidator()
    
    # Test dangerous extensions
    dangerous_files = [
        "malware.exe",
        "script.bat",
        "hack.sh",
        "virus.vbs"
    ]
    
    print("\n🧪 Testing dangerous extensions:")
    for filename in dangerous_files:
        try:
            validator._validate_extension(filename)
            print(f"  ❌ FAILED: {filename} should be blocked")
        except HTTPException:
            print(f"  ✅ PASSED: {filename} correctly blocked")
    
    # Test path traversal
    print("\n🧪 Testing path traversal:")
    traversal_attempts = [
        "../../../etc/passwd",
        "..\\..\\windows\\system32",
        "file/../../../secret.txt"
    ]
    
    for filename in traversal_attempts:
        try:
            validator._validate_filename(filename)
            print(f"  ❌ FAILED: {filename} should be blocked")
        except HTTPException:
            print(f"  ✅ PASSED: {filename} correctly blocked")
    
    print("\n✅ Security tests complete")

