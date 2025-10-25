#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application Configuration Module
Centralized configuration with environment variable support
"""

import os
from pathlib import Path
from typing import List, Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from pydantic import Field, validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AppConfig(BaseSettings):
    """
    Application configuration with environment variable support
    """
    
    # ============================================================
    # SECURITY
    # ============================================================
    
    jwt_secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        env="JWT_SECRET_KEY"
    )
    
    access_token_expire_minutes: int = Field(
        default=30,
        env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    
    refresh_token_expire_days: int = Field(
        default=7,
        env="REFRESH_TOKEN_EXPIRE_DAYS"
    )
    
    # ============================================================
    # DATABASE
    # ============================================================
    
    database_url: str = Field(
        default="sqlite:///kreyol_ai.db",
        env="DATABASE_URL"
    )
    
    # ============================================================
    # CORS & SECURITY
    # ============================================================
    
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:8000"],
        env="ALLOWED_ORIGINS"
    )
    
    @validator("allowed_origins", pre=True)
    def parse_allowed_origins(cls, v):
        """Parse comma-separated origins"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    # ============================================================
    # FILE UPLOAD LIMITS
    # ============================================================
    
    max_upload_size_mb: int = Field(
        default=10,
        env="MAX_UPLOAD_SIZE_MB"
    )
    
    max_pdf_pages: int = Field(
        default=500,
        env="MAX_PDF_PAGES"
    )
    
    max_audio_chars: int = Field(
        default=100000,
        env="MAX_AUDIO_CHARS"
    )
    
    allowed_file_extensions: List[str] = Field(
        default=[".pdf", ".txt", ".docx"]
    )
    
    allowed_mime_types: List[str] = Field(
        default=["application/pdf", "text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    )
    
    # ============================================================
    # RATE LIMITING
    # ============================================================
    
    rate_limiting_enabled: bool = Field(
        default=True,
        env="RATE_LIMITING_ENABLED"
    )
    
    default_rate_limit_tier: str = Field(
        default="free",
        env="DEFAULT_RATE_LIMIT_TIER"
    )
    
    # ============================================================
    # REDIS
    # ============================================================
    
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )
    
    redis_cache_enabled: bool = Field(
        default=False,
        env="REDIS_CACHE_ENABLED"
    )
    
    cache_ttl: int = Field(
        default=3600,
        env="CACHE_TTL"
    )
    
    # ============================================================
    # MONITORING
    # ============================================================
    
    prometheus_enabled: bool = Field(
        default=True,
        env="PROMETHEUS_ENABLED"
    )
    
    performance_monitoring: bool = Field(
        default=True,
        env="PERFORMANCE_MONITORING"
    )
    
    log_level: str = Field(
        default="INFO",
        env="LOG_LEVEL"
    )
    
    # ============================================================
    # EXTERNAL SERVICES
    # ============================================================
    
    sentry_dsn: Optional[str] = Field(
        default=None,
        env="SENTRY_DSN"
    )
    
    # ============================================================
    # FEATURE FLAGS
    # ============================================================
    
    auth_enabled: bool = Field(
        default=False,
        env="AUTH_ENABLED"
    )
    
    api_key_auth_enabled: bool = Field(
        default=False,
        env="API_KEY_AUTH_ENABLED"
    )
    
    allow_user_registration: bool = Field(
        default=True,
        env="ALLOW_USER_REGISTRATION"
    )
    
    # ============================================================
    # APPLICATION
    # ============================================================
    
    app_env: str = Field(
        default="development",
        env="APP_ENV"
    )
    
    port: int = Field(
        default=8000,
        env="PORT"
    )
    
    host: str = Field(
        default="0.0.0.0",
        env="HOST"
    )
    
    debug: bool = Field(
        default=False,
        env="DEBUG"
    )
    
    app_name: str = Field(
        default="🇭🇹 Kreyòl IA",
        env="APP_NAME"
    )
    
    app_version: str = Field(
        default="2.0.0",
        env="APP_VERSION"
    )
    
    # ============================================================
    # COMPUTED PROPERTIES
    # ============================================================
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.app_env.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.app_env.lower() == "development"
    
    @property
    def max_upload_size_bytes(self) -> int:
        """Get max upload size in bytes"""
        return self.max_upload_size_mb * 1024 * 1024
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global configuration instance
config = AppConfig()


def get_config() -> AppConfig:
    """Get global configuration instance"""
    return config


def validate_production_config():
    """
    Validate configuration for production deployment
    
    Raises:
        ValueError: If production configuration is invalid
    """
    if not config.is_production:
        return
    
    errors = []
    
    # Check JWT secret
    if config.jwt_secret_key == "dev-secret-key-change-in-production":
        errors.append("JWT_SECRET_KEY must be changed in production")
    
    # Check CORS
    if "*" in config.allowed_origins:
        errors.append("CORS cannot use wildcard (*) in production")
    
    # Check debug mode
    if config.debug:
        errors.append("DEBUG must be False in production")
    
    # Check database
    if "sqlite" in config.database_url.lower():
        errors.append("SQLite not recommended for production - use PostgreSQL")
    
    if errors:
        raise ValueError(
            "Production configuration errors:\n" + "\n".join(f"  - {e}" for e in errors)
        )


if __name__ == "__main__":
    """Test configuration loading"""
    print("=" * 60)
    print("🇭🇹 Kreyòl IA - Configuration")
    print("=" * 60)
    print()
    print(f"Environment: {config.app_env}")
    print(f"Debug: {config.debug}")
    print(f"Port: {config.port}")
    print(f"Database: {config.database_url}")
    print(f"CORS Origins: {config.allowed_origins}")
    print(f"Max Upload: {config.max_upload_size_mb}MB")
    print(f"Rate Limiting: {'Enabled' if config.rate_limiting_enabled else 'Disabled'}")
    print(f"Auth: {'Enabled' if config.auth_enabled else 'Disabled'}")
    print(f"Prometheus: {'Enabled' if config.prometheus_enabled else 'Disabled'}")
    print()
    
    # Validate if production
    try:
        validate_production_config()
        print("✅ Configuration valid")
    except ValueError as e:
        print(f"❌ Configuration errors:\n{e}")

