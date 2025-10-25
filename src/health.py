#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Health Check Module
Comprehensive health checks for production monitoring
"""

import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel

logger = logging.getLogger('KreyolAI.Health')


class HealthStatus(str, Enum):
    """Health check status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class ComponentHealth(BaseModel):
    """Health status of a single component"""
    status: HealthStatus
    message: Optional[str] = None
    response_time_ms: Optional[float] = None
    details: Optional[Dict[str, Any]] = None


class HealthCheck(BaseModel):
    """Overall health check response"""
    status: HealthStatus
    timestamp: str
    uptime_seconds: float
    version: str
    environment: str
    components: Dict[str, ComponentHealth]


class HealthChecker:
    """
    Comprehensive health checker for all system components
    """
    
    def __init__(self, app_version: str = "2.0.0", environment: str = "development"):
        """
        Initialize health checker
        
        Args:
            app_version: Application version
            environment: Deployment environment
        """
        self.app_version = app_version
        self.environment = environment
        self.start_time = time.time()
        logger.info("Health checker initialized")
    
    async def check_all(self, include_details: bool = True) -> HealthCheck:
        """
        Check health of all components
        
        Args:
            include_details: Whether to include detailed component checks
        
        Returns:
            HealthCheck object with overall status
        """
        components = {}
        
        if include_details:
            # Check database
            components["database"] = await self.check_database()
            
            # Check translator
            components["translator"] = await self.check_translator()
            
            # Check audio generator
            components["audio_generator"] = await self.check_audio_generator()
            
            # Check storage
            components["storage"] = await self.check_storage()
            
            # Check cache (if enabled)
            components["cache"] = await self.check_cache()
        
        # Determine overall status
        overall_status = self._determine_overall_status(components)
        
        # Calculate uptime
        uptime = time.time() - self.start_time
        
        return HealthCheck(
            status=overall_status,
            timestamp=datetime.utcnow().isoformat(),
            uptime_seconds=uptime,
            version=self.app_version,
            environment=self.environment,
            components=components
        )
    
    async def check_database(self) -> ComponentHealth:
        """
        Check database connectivity and health
        
        Returns:
            ComponentHealth for database
        """
        start_time = time.time()
        
        try:
            from .database import DatabaseManager
            
            # Try to connect to database
            db = DatabaseManager()
            
            # Simple query to test connectivity
            # This would be more comprehensive in production
            conn = db._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            
            response_time = (time.time() - start_time) * 1000
            
            return ComponentHealth(
                status=HealthStatus.HEALTHY,
                message="Database is operational",
                response_time_ms=response_time,
                details={"type": "SQLite"}
            )
            
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return ComponentHealth(
                status=HealthStatus.UNHEALTHY,
                message=f"Database error: {str(e)}"
            )
    
    async def check_translator(self) -> ComponentHealth:
        """
        Check translator service health
        
        Returns:
            ComponentHealth for translator
        """
        start_time = time.time()
        
        try:
            # Check if translator can be initialized
            # In production, you might do a test translation
            from deep_translator import GoogleTranslator
            
            # Try to create translator instance
            translator = GoogleTranslator(source='auto', target='ht')
            
            # Quick test translation
            test_result = translator.translate("test")
            
            response_time = (time.time() - start_time) * 1000
            
            if test_result:
                return ComponentHealth(
                    status=HealthStatus.HEALTHY,
                    message="Translator is operational",
                    response_time_ms=response_time,
                    details={"service": "GoogleTranslator"}
                )
            else:
                return ComponentHealth(
                    status=HealthStatus.DEGRADED,
                    message="Translator responding but results unclear"
                )
                
        except ImportError:
            return ComponentHealth(
                status=HealthStatus.UNHEALTHY,
                message="Translator module not available"
            )
        except Exception as e:
            logger.error(f"Translator health check failed: {e}")
            return ComponentHealth(
                status=HealthStatus.UNHEALTHY,
                message=f"Translator error: {str(e)}"
            )
    
    async def check_audio_generator(self) -> ComponentHealth:
        """
        Check audio generation service health
        
        Returns:
            ComponentHealth for audio generator
        """
        start_time = time.time()
        
        try:
            # Check if gTTS is available
            from gtts import gTTS
            
            # gTTS is available
            response_time = (time.time() - start_time) * 1000
            
            return ComponentHealth(
                status=HealthStatus.HEALTHY,
                message="Audio generator is operational",
                response_time_ms=response_time,
                details={"service": "gTTS"}
            )
            
        except ImportError:
            return ComponentHealth(
                status=HealthStatus.UNHEALTHY,
                message="Audio generator module not available"
            )
        except Exception as e:
            logger.error(f"Audio generator health check failed: {e}")
            return ComponentHealth(
                status=HealthStatus.DEGRADED,
                message=f"Audio generator warning: {str(e)}"
            )
    
    async def check_storage(self) -> ComponentHealth:
        """
        Check storage (disk) health
        
        Returns:
            ComponentHealth for storage
        """
        start_time = time.time()
        
        try:
            from pathlib import Path
            import shutil
            
            # Check output directory
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            
            # Check disk space
            stat = shutil.disk_usage(output_dir)
            
            # Calculate percentages
            used_percent = (stat.used / stat.total) * 100
            free_gb = stat.free / (1024 ** 3)
            
            response_time = (time.time() - start_time) * 1000
            
            # Warn if disk is getting full
            if used_percent > 90:
                status = HealthStatus.UNHEALTHY
                message = f"Disk critically full: {used_percent:.1f}% used"
            elif used_percent > 80:
                status = HealthStatus.DEGRADED
                message = f"Disk space low: {used_percent:.1f}% used"
            else:
                status = HealthStatus.HEALTHY
                message = "Storage is operational"
            
            return ComponentHealth(
                status=status,
                message=message,
                response_time_ms=response_time,
                details={
                    "used_percent": round(used_percent, 2),
                    "free_gb": round(free_gb, 2),
                    "total_gb": round(stat.total / (1024 ** 3), 2)
                }
            )
            
        except Exception as e:
            logger.error(f"Storage health check failed: {e}")
            return ComponentHealth(
                status=HealthStatus.UNHEALTHY,
                message=f"Storage error: {str(e)}"
            )
    
    async def check_cache(self) -> ComponentHealth:
        """
        Check cache (Redis) health if enabled
        
        Returns:
            ComponentHealth for cache
        """
        start_time = time.time()
        
        try:
            # Try to import redis
            import redis
            
            # Try to connect (with short timeout)
            r = redis.Redis(
                host='localhost',
                port=6379,
                socket_connect_timeout=1,
                socket_timeout=1
            )
            
            # Ping Redis
            r.ping()
            
            # Get info
            info = r.info()
            
            response_time = (time.time() - start_time) * 1000
            
            return ComponentHealth(
                status=HealthStatus.HEALTHY,
                message="Cache is operational",
                response_time_ms=response_time,
                details={
                    "service": "Redis",
                    "version": info.get('redis_version', 'unknown'),
                    "connected_clients": info.get('connected_clients', 0)
                }
            )
            
        except ImportError:
            return ComponentHealth(
                status=HealthStatus.DEGRADED,
                message="Cache module not installed (optional)"
            )
        except Exception as e:
            # Cache not available is not critical
            return ComponentHealth(
                status=HealthStatus.DEGRADED,
                message=f"Cache not available: {str(e)}"
            )
    
    def _determine_overall_status(self, components: Dict[str, ComponentHealth]) -> HealthStatus:
        """
        Determine overall health status from component statuses
        
        Args:
            components: Dictionary of component health statuses
        
        Returns:
            Overall HealthStatus
        """
        if not components:
            return HealthStatus.HEALTHY
        
        statuses = [comp.status for comp in components.values()]
        
        # If any component is unhealthy, system is unhealthy
        if HealthStatus.UNHEALTHY in statuses:
            return HealthStatus.UNHEALTHY
        
        # If any component is degraded, system is degraded
        if HealthStatus.DEGRADED in statuses:
            return HealthStatus.DEGRADED
        
        # All components healthy
        return HealthStatus.HEALTHY
    
    async def liveness_probe(self) -> Dict[str, str]:
        """
        Kubernetes-style liveness probe
        Simple check that application is running
        
        Returns:
            Dict with status
        """
        return {
            "status": "alive",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def readiness_probe(self) -> Dict[str, Any]:
        """
        Kubernetes-style readiness probe
        Check if application is ready to serve traffic
        
        Returns:
            Dict with status and component checks
        """
        health = await self.check_all(include_details=True)
        
        is_ready = health.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED]
        
        return {
            "status": "ready" if is_ready else "not_ready",
            "timestamp": health.timestamp,
            "components": {
                name: comp.status
                for name, comp in health.components.items()
            }
        }
    
    async def startup_probe(self) -> Dict[str, Any]:
        """
        Kubernetes-style startup probe
        Check if application has started successfully
        
        Returns:
            Dict with status
        """
        # Check critical components only
        critical_checks = {
            "database": await self.check_database(),
            "storage": await self.check_storage()
        }
        
        all_healthy = all(
            comp.status == HealthStatus.HEALTHY
            for comp in critical_checks.values()
        )
        
        return {
            "status": "started" if all_healthy else "starting",
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {
                name: comp.status
                for name, comp in critical_checks.items()
            }
        }


# ============================================================
# FASTAPI ENDPOINT HELPERS
# ============================================================

async def health_endpoint(checker: HealthChecker, detailed: bool = False):
    """
    FastAPI endpoint for health checks
    
    Args:
        checker: HealthChecker instance
        detailed: Whether to include detailed checks
    
    Returns:
        Health check response
    """
    health = await checker.check_all(include_details=detailed)
    
    # Return appropriate HTTP status code
    status_code = 200 if health.status != HealthStatus.UNHEALTHY else 503
    
    return health, status_code


async def liveness_endpoint(checker: HealthChecker):
    """FastAPI endpoint for liveness probe"""
    return await checker.liveness_probe()


async def readiness_endpoint(checker: HealthChecker):
    """FastAPI endpoint for readiness probe"""
    result = await checker.readiness_probe()
    status_code = 200 if result["status"] == "ready" else 503
    return result, status_code


async def startup_endpoint(checker: HealthChecker):
    """FastAPI endpoint for startup probe"""
    result = await checker.startup_probe()
    status_code = 200 if result["status"] == "started" else 503
    return result, status_code


if __name__ == "__main__":
    """Test health checker"""
    import asyncio
    
    async def test():
        print("=" * 60)
        print("🏥 Health Checker - Test")
        print("=" * 60)
        print()
        
        checker = HealthChecker(app_version="2.0.0", environment="development")
        
        # Full health check
        print("Running full health check...")
        health = await checker.check_all(include_details=True)
        
        print(f"\n📊 Overall Status: {health.status.value.upper()}")
        print(f"⏱️  Uptime: {health.uptime_seconds:.2f}s")
        print(f"📅 Timestamp: {health.timestamp}")
        print(f"🏷️  Version: {health.version}")
        print(f"🌍 Environment: {health.environment}")
        print("\n📋 Components:")
        
        for name, component in health.components.items():
            status_emoji = {
                "healthy": "✅",
                "degraded": "⚠️",
                "unhealthy": "❌"
            }.get(component.status, "❓")
            
            print(f"  {status_emoji} {name}: {component.status}")
            if component.message:
                print(f"     {component.message}")
            if component.response_time_ms:
                print(f"     Response time: {component.response_time_ms:.2f}ms")
        
        print("\n✅ Health check complete")
    
    asyncio.run(test())

