#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Server Starter
Start the FastAPI server with monitoring
"""

import sys
import uvicorn
from datetime import datetime

# Fix Windows console encoding
if sys.platform.startswith('win'):
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass


def main():
    """Start API server"""
    
    print("="*60)
    print("🇭🇹 Pwojè Kreyòl IA - API Server")
    print("="*60)
    print(f"Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("📡 API Server:  http://localhost:8000")
    print("📚 API Docs:    http://localhost:8000/docs")
    print("📖 ReDoc:       http://localhost:8000/redoc")
    print("💚 Health:      http://localhost:8000/health")
    print()
    print("Press CTRL+C to stop")
    print("="*60)
    print()
    
    # Start server
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )


if __name__ == "__main__":
    main()

