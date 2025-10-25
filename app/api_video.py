#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 Video & AI API Endpoints
Tout endpoints pou video processing ak AI tools
"""

from fastapi import UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import tempfile
import shutil

# Import with graceful fallback
try:
    from app.services.video_service import video_service
    VIDEO_SERVICE_AVAILABLE = True
except Exception as e:
    print(f"⚠️  Video service not available: {e}")
    VIDEO_SERVICE_AVAILABLE = False
    video_service = None

try:
    from app.services.ai_service import ai_service
    AI_SERVICE_AVAILABLE = True
except Exception as e:
    print(f"⚠️  AI service not available: {e}")
    AI_SERVICE_AVAILABLE = False
    ai_service = None

try:
    from app.auth import get_current_user_optional
    AUTH_AVAILABLE = True
except Exception as e:
    print(f"⚠️  Auth not available: {e}")
    AUTH_AVAILABLE = False
    get_current_user_optional = lambda: None

try:
    from app.rate_limiter import rate_limit, rate_limit_normal
    RATE_LIMIT_AVAILABLE = True
except Exception as e:
    print(f"⚠️  Rate limiter not available: {e}")
    RATE_LIMIT_AVAILABLE = False
    # Dummy decorators
    def rate_limit(limit): return lambda f: f
    rate_limit_normal = lambda f: f


def setup_video_ai_routes(app):
    """
    Setup all video & AI routes
    
    Args:
        app: FastAPI application
    """
    
    # ============================================================
    # AI ENDPOINTS
    # ============================================================
    
    @app.post("/api/ai/generate-script")
    @rate_limit("20/hour")
    async def generate_script(
        prompt: str = Form(...),
        style: str = Form("conversational"),
        length: str = Form("medium"),
        language: str = Form("ht"),
        current_user: dict = Depends(get_current_user_optional)
    ):
        """
        🤖 Jenere yon script ak IA
        
        **Paramèt:**
        - prompt: Sijè/pwòm pou script la
        - style: Stil (conversational, formal, humorous, dramatic)
        - length: Longè (short, medium, long)
        - language: Lang (ht, fr, en)
        
        **Returns:**
        - script: Script ki jenere
        - word_count: Kantite mo
        - model: Model ki itilize
        """
        try:
            result = await ai_service.generate_script(
                prompt=prompt,
                style=style,
                length=length,
                language=language
            )
            
            return JSONResponse({
                "status": "success",
                "message": "Script jenere avèk siksè! 🤖✅",
                **result
            })
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    
    # ============================================================
    # VIDEO VOICEOVER
    # ============================================================
    
    @app.post("/api/video/add-voiceover")
    @rate_limit("10/hour")
    async def add_video_voiceover(
        file: UploadFile = File(...),
        voiceover_text: str = Form(...),
        voice: str = Form("creole-native"),
        mix_volume: float = Form(0.5),
        current_user: dict = Depends(get_current_user_optional)
    ):
        """
        🎬 Ajoute voiceover nan videyo
        
        **Paramèt:**
        - file: Fichye videyo
        - voiceover_text: Tèks pou narration
        - voice: Vwa pou itilize
        - mix_volume: Volim orijinal audio (0.0-1.0)
        """
        try:
            # Save uploaded file
            suffix = Path(file.filename).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_path = Path(tmp.name)
            
            # Process video
            output_file = await video_service.add_voiceover(
                video_file=tmp_path,
                voiceover_text=voiceover_text,
                voice=voice,
                mix_volume=mix_volume
            )
            
            # Cleanup
            tmp_path.unlink(missing_ok=True)
            
            return JSONResponse({
                "status": "success",
                "message": "Voiceover ajoute avèk siksè! 🎬✅",
                "video_url": f"/output/videos/{output_file.name}",
                "video_file": output_file.name
            })
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    
    # ============================================================
    # MUSIC & SFX
    # ============================================================
    
    @app.post("/api/video/add-music")
    @rate_limit_normal
    async def add_background_music(
        video: UploadFile = File(...),
        music: UploadFile = File(...),
        music_volume: float = Form(0.3),
        current_user: dict = Depends(get_current_user_optional)
    ):
        """
        🎵 Ajoute mizik background nan videyo
        
        **Paramèt:**
        - video: Fichye videyo
        - music: Fichye mizik
        - music_volume: Volim mizik (0.0-1.0)
        """
        try:
            # Save uploaded files
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(video.filename).suffix) as tmp_video:
                shutil.copyfileobj(video.file, tmp_video)
                video_path = Path(tmp_video.name)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(music.filename).suffix) as tmp_music:
                shutil.copyfileobj(music.file, tmp_music)
                music_path = Path(tmp_music.name)
            
            # Process
            output_file = await video_service.add_background_music(
                video_file=video_path,
                music_file=music_path,
                music_volume=music_volume
            )
            
            # Cleanup
            video_path.unlink(missing_ok=True)
            music_path.unlink(missing_ok=True)
            
            return JSONResponse({
                "status": "success",
                "message": "Mizik ajoute avèk siksè! 🎵✅",
                "video_url": f"/output/videos/{output_file.name}"
            })
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    
    # ============================================================
    # CAPTIONS / SUBTITLES
    # ============================================================
    
    @app.post("/api/video/generate-captions")
    @rate_limit("10/hour")
    async def generate_captions(
        file: UploadFile = File(...),
        language: str = Form("ht"),
        burn_captions: bool = Form(False),
        current_user: dict = Depends(get_current_user_optional)
    ):
        """
        📝 Jenere soutit pou videyo
        
        **Paramèt:**
        - file: Fichye videyo
        - language: Lang (ht, en, fr)
        - burn_captions: Ajoute soutit dirèkteman nan videyo (True/False)
        """
        try:
            # Save uploaded file
            suffix = Path(file.filename).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_path = Path(tmp.name)
            
            # Generate captions
            srt_file = await video_service.generate_captions(
                video_file=tmp_path,
                language=language
            )
            
            result = {
                "status": "success",
                "message": "Soutit jenere avèk siksè! 📝✅",
                "srt_url": f"/output/videos/{srt_file.name}",
                "srt_file": srt_file.name
            }
            
            # Burn captions if requested
            if burn_captions:
                output_video = await video_service.burn_captions(
                    video_file=tmp_path,
                    srt_file=srt_file
                )
                result["video_url"] = f"/output/videos/{output_video.name}"
                result["video_file"] = output_video.name
            
            # Cleanup
            tmp_path.unlink(missing_ok=True)
            
            return JSONResponse(result)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    
    # ============================================================
    # AUDIO PROCESSING
    # ============================================================
    
    @app.post("/api/video/denoise-audio")
    @rate_limit_normal
    async def denoise_video_audio(
        file: UploadFile = File(...),
        noise_reduction: int = Form(20),
        current_user: dict = Depends(get_current_user_optional)
    ):
        """
        🔇 Retire bri nan audio videyo
        
        **Paramèt:**
        - file: Fichye videyo
        - noise_reduction: Nivo reduction (0-100)
        """
        try:
            # Save uploaded file
            suffix = Path(file.filename).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_path = Path(tmp.name)
            
            # Process
            output_file = await video_service.denoise_audio(
                video_file=tmp_path,
                noise_reduction=noise_reduction
            )
            
            # Cleanup
            tmp_path.unlink(missing_ok=True)
            
            return JSONResponse({
                "status": "success",
                "message": "Bri retire avèk siksè! 🔇✅",
                "video_url": f"/output/videos/{output_file.name}"
            })
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    
    @app.post("/api/video/normalize-audio")
    @rate_limit_normal
    async def normalize_video_audio(
        file: UploadFile = File(...),
        current_user: dict = Depends(get_current_user_optional)
    ):
        """
        🔊 Nòmalize volim audio
        
        **Paramèt:**
        - file: Fichye videyo
        """
        try:
            # Save uploaded file
            suffix = Path(file.filename).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_path = Path(tmp.name)
            
            # Process
            output_file = await video_service.normalize_audio(
                video_file=tmp_path
            )
            
            # Cleanup
            tmp_path.unlink(missing_ok=True)
            
            return JSONResponse({
                "status": "success",
                "message": "Audio normalized avèk siksè! 🔊✅",
                "video_url": f"/output/videos/{output_file.name}"
            })
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    
    # ============================================================
    # VIDEO INFO
    # ============================================================
    
    @app.post("/api/video/info")
    async def get_video_info(
        file: UploadFile = File(...)
    ):
        """
        ℹ️ Jwenn enfòmasyon sou yon videyo
        
        **Returns:**
        - duration: Dirasyon (segonn)
        - size: Gwosè (bytes)
        - width/height: Rezolisyon
        - fps: Frames per second
        - codecs: Video ak audio codecs
        """
        try:
            # Save uploaded file
            suffix = Path(file.filename).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_path = Path(tmp.name)
            
            # Get info
            info = await video_service.get_video_info(tmp_path)
            
            # Cleanup
            tmp_path.unlink(missing_ok=True)
            
            return JSONResponse({
                "status": "success",
                "info": info
            })
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    
    print("✅ Video & AI API routes configured")
    print("   • AI Script Generation")
    print("   • Video Voiceover")
    print("   • Background Music")
    print("   • Captions/Subtitles")
    print("   • Audio Denoising")
    print("   • Audio Normalization")


if __name__ == "__main__":
    print("🎬 Video & AI API Module")
    print("=" * 60)
    print("New Endpoints:")
    print("  • POST /api/ai/generate-script - AI script generation")
    print("  • POST /api/video/add-voiceover - Add voiceover")
    print("  • POST /api/video/add-music - Add background music")
    print("  • POST /api/video/generate-captions - Generate captions")
    print("  • POST /api/video/denoise-audio - Remove noise")
    print("  • POST /api/video/normalize-audio - Normalize volume")
    print("  • POST /api/video/info - Get video information")
    print("=" * 60)

