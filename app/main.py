#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇭🇹 Kreyòl IA - Main Application (Version 4.0)
Pwen antre prensipal pou aplikasyon an
"""

import uvicorn
from pathlib import Path
import sys

def main():
    """Lance aplikasyon an"""
    print("=" * 80)
    print("🇭🇹 KREYÒL IA - STUDIO PWOFESYONÈL (VERSION 4.0)")
    print("=" * 80)
    print("🌐 Platfòm Kreyasyon Kontni an Kreyòl Ayisyen")
    print("=" * 80)
    print()
    print("📱 INTERFACE:")
    print("   Web Interface:  http://localhost:8000")
    print("   API Docs:       http://localhost:8000/docs")
    print("   ReDoc:          http://localhost:8000/redoc")
    print()
    print("🚀 NOUVO FONKSYONALITE (v4.0):")
    print("   ✅ Background Jobs (Celery + Redis)")
    print("   ✅ Redis Cache (100x faster)")
    print("   ✅ JWT Authentication")
    print("   ✅ Rate Limiting")
    print("   ✅ WebSocket Real-time Progress")
    print("   ✅ Streaming TTS")
    print()
    print("🔗 NOUVO ENDPOINTS:")
    print("   POST   /api/auth/login - Login")
    print("   POST   /api/audiobook/async - Background audiobook")
    print("   GET    /api/tasks/{id} - Task status")
    print("   WS     /ws/tasks/{id} - Real-time progress")
    print("   POST   /api/translate/cached - Cached translation")
    print("   POST   /api/tts/streaming - Streaming audio")
    print()
    print("💡 DEMO USER:")
    print("   Email: demo@kreyolia.ht")
    print("   Password: demo123")
    print()
    print("⚠️  NÒTE:")
    print("   • Redis dwe ap kouri pou cache/celery (optional)")
    print("   • Celery worker dwe ap kouri pou background jobs (optional)")
    print("   • Si yo pa disponib, sistèm la ap itilize fallback")
    print()
    print("=" * 80)
    print()
    
    # Check if Redis is available
    try:
        from app.cache_redis import translation_cache
        if translation_cache.available:
            print("✅ Redis: Connected")
        else:
            print("⚠️  Redis: Not available (using memory fallback)")
    except Exception as e:
        print(f"⚠️  Redis: {e}")
    
    # Check if Celery is available
    try:
        from app.tasks import celery_app
        print("✅ Celery: Configured")
        print("   To start worker: celery -A app.tasks worker --loglevel=info --pool=solo")
    except Exception as e:
        print(f"⚠️  Celery: {e}")
    
    print()
    print("=" * 80)
    print("🚀 STARTING SERVER...")
    print("=" * 80)
    print()
    
    # Setup enhanced routes
    try:
        # Import from current directory
        import sys
        from pathlib import Path
        
        # Add project root to path
        project_root = Path(__file__).parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        
        # Now import
        from app.api import app
        
        # Try to load enhanced features
        try:
            from app.api_enhanced import setup_enhanced_routes
            setup_enhanced_routes(app)
            print("✅ Enhanced routes loaded!")
        except Exception as e:
            print(f"⚠️  Enhanced routes not available: {e}")
        
        # Try to load video/AI features
        try:
            from app.api_video import setup_video_ai_routes
            setup_video_ai_routes(app)
            print("✅ Video & AI routes loaded!")
        except Exception as e:
            print(f"⚠️  Video & AI routes not available: {e}")
            
    except Exception as e:
        print(f"⚠️  Error loading routes: {e}")
        print("   Running with basic features only")
        import traceback
        traceback.print_exc()
    
    # Lance servè a
    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        log_level="info"
    )

if __name__ == "__main__":
    main()

