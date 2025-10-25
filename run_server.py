#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Simple Server Launcher
Lance servè a san pwoblèm import
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("=" * 80)
print("🇭🇹 KREYÒL IA - VERSION 4.1.0")
print("=" * 80)
print()

# Import app
from app.api import app

# Try to load enhanced routes
try:
    from app.api_enhanced import setup_enhanced_routes
    setup_enhanced_routes(app)
    print("✅ Enhanced routes (v4.0) loaded!")
except Exception as e:
    print(f"⚠️  Enhanced routes: {e}")

# Try to load video/AI routes
try:
    from app.api_video import setup_video_ai_routes
    setup_video_ai_routes(app)
    print("✅ Video & AI routes (v4.1) loaded!")
except Exception as e:
    print(f"⚠️  Video & AI routes: {e}")

print()
print("=" * 80)
print("🌐 URLs:")
print("   http://localhost:8000")
print("   http://localhost:8000/docs")
print("=" * 80)
print()

# Run server
if __name__ == "__main__":
    import uvicorn
    
    # Use string import for reload to work properly
    uvicorn.run(
        "run_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(project_root / "app"), str(project_root)],
        log_level="info"
    )

