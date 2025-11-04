#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🇭🇹 Faner Studio - Vercel Entry Point
Minimal version for Vercel deployment
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# ============================================================
# APPLICATION SETUP
# ============================================================

app = FastAPI(
    title="🇭🇹 Faner Studio", 
    version="3.0.0",
    description="Platfòm kreyasyon kontni pwofesyonèl an Kreyòl Ayisyen"
)

# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# ROOT & HEALTH CHECK
# ============================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="ht">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🇭🇹 Faner Studio</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                padding: 20px;
            }
            .container {
                text-align: center;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                padding: 60px 40px;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                max-width: 600px;
            }
            h1 {
                font-size: 3em;
                margin: 0 0 20px 0;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            }
            p {
                font-size: 1.3em;
                margin: 15px 0;
            }
            .status {
                background: rgba(255, 255, 255, 0.2);
                padding: 20px;
                border-radius: 10px;
                margin: 30px 0;
            }
            a {
                color: #fff;
                text-decoration: none;
                background: rgba(255, 255, 255, 0.2);
                padding: 12px 30px;
                border-radius: 25px;
                display: inline-block;
                margin: 10px;
                transition: all 0.3s;
            }
            a:hover {
                background: rgba(255, 255, 255, 0.3);
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🇭🇹 Faner Studio</h1>
            <p>Platfòm Pwofesyonèl pou Kreyasyon Kontni an Kreyòl</p>
            
            <div class="status">
                <p>✅ <strong>Status:</strong> LIVE on Vercel!</p>
                <p>🚀 <strong>Version:</strong> 3.0.0</p>
            </div>
            
            <div>
                <a href="/docs">📚 API Docs</a>
                <a href="/health">💚 Health Check</a>
            </div>
        </div>
    </body>
    </html>
    """)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "✅ Faner Studio is running!",
        "platform": "Vercel",
        "timestamp": datetime.now().isoformat(),
        "version": "3.0.0"
    }


@app.get("/api/test")
async def test_endpoint():
    """Test API endpoint"""
    return {
        "success": True,
        "message": "🇭🇹 Faner Studio API fonksyone!",
        "endpoints": [
            "/",
            "/health",
            "/docs",
            "/api/test"
        ]
    }


# ============================================================
# VERCEL HANDLER - ASGI Application
# ============================================================

# Vercel needs an ASGI app
from mangum import Mangum

handler = Mangum(app)
