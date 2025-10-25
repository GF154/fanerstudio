#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastAPI REST API
Pwojè Kreyòl IA - RESTful API Service
Version 5.0
"""

import sys
import asyncio
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from pathlib import Path
import tempfile
import uuid
import logging
from datetime import datetime
import shutil

# Fix Windows console encoding
if sys.platform.startswith('win'):
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

from src import Config, TextExtractor, CreoleTranslator, AudiobookGenerator, setup_logging
from src.database import DatabaseManager, Task, TaskStatus

# Initialize FastAPI app
app = FastAPI(
    title="🇭🇹 Pwojè Kreyòl IA API",
    description="Haitian Creole Translation & Audiobook Generation API",
    version="5.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
config = Config()
logger = setup_logging(config.logs_dir, log_level="INFO")
db_manager = DatabaseManager()

# Storage directories
UPLOAD_DIR = Path("api_uploads")
RESULT_DIR = Path("api_results")
UPLOAD_DIR.mkdir(exist_ok=True)
RESULT_DIR.mkdir(exist_ok=True)


# ==================== MODELS ====================

class TranslationRequest(BaseModel):
    """Request model for text translation"""
    text: str = Field(..., min_length=1, max_length=100000, description="Text to translate")
    source_lang: Optional[str] = Field(None, description="Source language code (auto-detect if None)")
    target_lang: str = Field("ht", description="Target language code")
    enable_cache: bool = Field(True, description="Enable translation cache")
    enable_parallel: bool = Field(False, description="Enable parallel translation")
    max_workers: int = Field(3, ge=1, le=8, description="Number of workers for parallel translation")


class TranslationResponse(BaseModel):
    """Response model for translation"""
    task_id: str
    status: str
    text_length: int
    translation_length: Optional[int] = None
    translation: Optional[str] = None
    processing_time: Optional[float] = None
    cache_stats: Optional[dict] = None


class AudioRequest(BaseModel):
    """Request model for audio generation"""
    text: str = Field(..., min_length=1, max_length=100000, description="Text for audio generation")
    language: str = Field("ht", description="Audio language code")
    slow_speed: bool = Field(False, description="Use slow speech speed")


class AudioResponse(BaseModel):
    """Response model for audio generation"""
    task_id: str
    status: str
    audio_url: Optional[str] = None
    audio_size_mb: Optional[float] = None
    processing_time: Optional[float] = None


class TaskStatusResponse(BaseModel):
    """Response model for task status"""
    task_id: str
    status: str
    task_type: str
    created_at: str
    updated_at: str
    result_data: Optional[dict] = None
    error_message: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: str
    services: dict


# ==================== HELPER FUNCTIONS ====================

def get_extractor():
    """Dependency injection for TextExtractor"""
    return TextExtractor(config)


def get_translator():
    """Dependency injection for CreoleTranslator"""
    return CreoleTranslator(config)


def get_audio_generator():
    """Dependency injection for AudiobookGenerator"""
    return AudiobookGenerator(config)


async def cleanup_old_files():
    """Clean up old temporary files"""
    try:
        cutoff_time = datetime.now().timestamp() - (24 * 3600)  # 24 hours
        
        for directory in [UPLOAD_DIR, RESULT_DIR]:
            for file_path in directory.iterdir():
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    logger.info(f"Cleaned up old file: {file_path}")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")


# ==================== API ENDPOINTS ====================

@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "🇭🇹 Pwojè Kreyòl IA API",
        "version": "5.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "translate": "POST /api/v1/translate",
            "generate_audio": "POST /api/v1/audio",
            "process_document": "POST /api/v1/process",
            "task_status": "GET /api/v1/tasks/{task_id}",
            "download_result": "GET /api/v1/download/{task_id}/{file_type}"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="5.0.0",
        timestamp=datetime.now().isoformat(),
        services={
            "api": "operational",
            "database": "operational",
            "storage": "operational"
        }
    )


@app.post("/api/v1/translate", response_model=TranslationResponse)
async def translate_text(
    request: TranslationRequest,
    background_tasks: BackgroundTasks,
    translator: CreoleTranslator = Depends(get_translator)
):
    """
    Translate text to target language
    
    Args:
        request: Translation request data
    
    Returns:
        Translation response with task ID and result
    """
    task_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    try:
        logger.info(f"Translation request {task_id}: {len(request.text)} chars")
        
        # Create task in database
        task = db_manager.create_task(
            task_id=task_id,
            task_type="translation",
            input_data={
                "text_length": len(request.text),
                "source_lang": request.source_lang,
                "target_lang": request.target_lang
            }
        )
        
        # Configure translator
        translator.config.source_language = request.source_lang
        translator.config.target_language = request.target_lang
        translator.config.enable_cache = request.enable_cache
        translator.config.enable_parallel = request.enable_parallel
        translator.config.max_workers = request.max_workers
        
        # Perform translation
        translation = translator.translate(request.text, src_lang=request.source_lang)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Get cache stats
        cache_stats = None
        if translator.cache:
            cache_stats = translator.cache.get_stats()
        
        # Update task
        db_manager.update_task(
            task_id=task_id,
            status=TaskStatus.COMPLETED,
            result_data={
                "translation": translation,
                "translation_length": len(translation),
                "processing_time": processing_time,
                "cache_stats": cache_stats
            }
        )
        
        logger.info(f"Translation {task_id} completed in {processing_time:.2f}s")
        
        return TranslationResponse(
            task_id=task_id,
            status="completed",
            text_length=len(request.text),
            translation_length=len(translation),
            translation=translation,
            processing_time=processing_time,
            cache_stats=cache_stats
        )
        
    except Exception as e:
        logger.error(f"Translation error {task_id}: {e}", exc_info=True)
        
        db_manager.update_task(
            task_id=task_id,
            status=TaskStatus.FAILED,
            error_message=str(e)
        )
        
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


@app.post("/api/v1/audio", response_model=AudioResponse)
async def generate_audio(
    request: AudioRequest,
    background_tasks: BackgroundTasks,
    generator: AudiobookGenerator = Depends(get_audio_generator)
):
    """
    Generate audio from text
    
    Args:
        request: Audio generation request
    
    Returns:
        Audio response with download URL
    """
    task_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    try:
        logger.info(f"Audio generation request {task_id}: {len(request.text)} chars")
        
        # Create task
        task = db_manager.create_task(
            task_id=task_id,
            task_type="audio_generation",
            input_data={
                "text_length": len(request.text),
                "language": request.language,
                "slow_speed": request.slow_speed
            }
        )
        
        # Generate audio
        output_path = RESULT_DIR / f"{task_id}.mp3"
        generator.config.tts_language = request.language
        generator.config.tts_slow = request.slow_speed
        
        generator.generate(request.text, output_path=output_path)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        audio_size_mb = output_path.stat().st_size / (1024 * 1024)
        
        # Update task
        db_manager.update_task(
            task_id=task_id,
            status=TaskStatus.COMPLETED,
            result_data={
                "audio_path": str(output_path),
                "audio_size_mb": audio_size_mb,
                "processing_time": processing_time
            }
        )
        
        logger.info(f"Audio {task_id} generated in {processing_time:.2f}s")
        
        return AudioResponse(
            task_id=task_id,
            status="completed",
            audio_url=f"/api/v1/download/{task_id}/audio",
            audio_size_mb=audio_size_mb,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Audio generation error {task_id}: {e}", exc_info=True)
        
        db_manager.update_task(
            task_id=task_id,
            status=TaskStatus.FAILED,
            error_message=str(e)
        )
        
        raise HTTPException(status_code=500, detail=f"Audio generation failed: {str(e)}")


@app.post("/api/v1/process")
async def process_document(
    file: UploadFile = File(...),
    target_lang: str = "ht",
    generate_audio: bool = True,
    background_tasks: BackgroundTasks = None,
    extractor: TextExtractor = Depends(get_extractor),
    translator: CreoleTranslator = Depends(get_translator),
    audio_generator: AudiobookGenerator = Depends(get_audio_generator)
):
    """
    Process a document: extract, translate, and optionally generate audio
    
    Args:
        file: Uploaded file (PDF, TXT, DOCX)
        target_lang: Target language code
        generate_audio: Whether to generate audiobook
    
    Returns:
        Task information with download URLs
    """
    task_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    try:
        logger.info(f"Document processing request {task_id}: {file.filename}")
        
        # Save uploaded file
        upload_path = UPLOAD_DIR / f"{task_id}_{file.filename}"
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create task
        task = db_manager.create_task(
            task_id=task_id,
            task_type="document_processing",
            input_data={
                "filename": file.filename,
                "target_lang": target_lang,
                "generate_audio": generate_audio
            }
        )
        
        # Extract text
        text = extractor.extract(upload_path)
        
        # Translate
        translator.config.target_language = target_lang
        translation = translator.translate(text)
        
        # Save translation
        translation_path = RESULT_DIR / f"{task_id}_translation.txt"
        with open(translation_path, "w", encoding="utf-8") as f:
            f.write(translation)
        
        result_data = {
            "text_length": len(text),
            "translation_length": len(translation),
            "translation_path": str(translation_path),
            "download_urls": {
                "translation": f"/api/v1/download/{task_id}/translation"
            }
        }
        
        # Generate audio if requested
        if generate_audio:
            audio_path = RESULT_DIR / f"{task_id}_audio.mp3"
            audio_generator.generate(translation, output_path=audio_path)
            audio_size_mb = audio_path.stat().st_size / (1024 * 1024)
            
            result_data["audio_path"] = str(audio_path)
            result_data["audio_size_mb"] = audio_size_mb
            result_data["download_urls"]["audio"] = f"/api/v1/download/{task_id}/audio"
        
        processing_time = (datetime.now() - start_time).total_seconds()
        result_data["processing_time"] = processing_time
        
        # Update task
        db_manager.update_task(
            task_id=task_id,
            status=TaskStatus.COMPLETED,
            result_data=result_data
        )
        
        # Schedule cleanup
        background_tasks.add_task(upload_path.unlink)
        
        logger.info(f"Document processing {task_id} completed in {processing_time:.2f}s")
        
        return {
            "task_id": task_id,
            "status": "completed",
            "filename": file.filename,
            "processing_time": processing_time,
            "results": result_data
        }
        
    except Exception as e:
        logger.error(f"Document processing error {task_id}: {e}", exc_info=True)
        
        db_manager.update_task(
            task_id=task_id,
            status=TaskStatus.FAILED,
            error_message=str(e)
        )
        
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.get("/api/v1/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """
    Get task status and results
    
    Args:
        task_id: Task identifier
    
    Returns:
        Task status information
    """
    task = db_manager.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    return TaskStatusResponse(
        task_id=task.task_id,
        status=task.status,
        task_type=task.task_type,
        created_at=task.created_at,
        updated_at=task.updated_at,
        result_data=task.result_data,
        error_message=task.error_message
    )


@app.get("/api/v1/download/{task_id}/{file_type}")
async def download_result(task_id: str, file_type: str):
    """
    Download task result file
    
    Args:
        task_id: Task identifier
        file_type: File type (audio, translation)
    
    Returns:
        File download response
    """
    task = db_manager.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    if task.status != TaskStatus.COMPLETED:
        raise HTTPException(status_code=400, detail=f"Task {task_id} not completed yet")
    
    # Determine file path
    if file_type == "audio":
        file_path = RESULT_DIR / f"{task_id}_audio.mp3"
        media_type = "audio/mpeg"
        filename = f"audiobook_{task_id}.mp3"
    elif file_type == "translation":
        file_path = RESULT_DIR / f"{task_id}_translation.txt"
        media_type = "text/plain"
        filename = f"translation_{task_id}.txt"
    else:
        raise HTTPException(status_code=400, detail=f"Invalid file type: {file_type}")
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {file_type}")
    
    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=filename
    )


@app.get("/api/v1/tasks", response_model=List[TaskStatusResponse])
async def list_tasks(
    limit: int = 50,
    offset: int = 0,
    status: Optional[str] = None
):
    """
    List all tasks with pagination
    
    Args:
        limit: Maximum number of tasks to return
        offset: Number of tasks to skip
        status: Filter by status (optional)
    
    Returns:
        List of tasks
    """
    tasks = db_manager.list_tasks(limit=limit, offset=offset, status=status)
    
    return [
        TaskStatusResponse(
            task_id=task.task_id,
            status=task.status,
            task_type=task.task_type,
            created_at=task.created_at,
            updated_at=task.updated_at,
            result_data=task.result_data,
            error_message=task.error_message
        )
        for task in tasks
    ]


@app.delete("/api/v1/tasks/{task_id}")
async def delete_task(task_id: str):
    """
    Delete a task and its associated files
    
    Args:
        task_id: Task identifier
    
    Returns:
        Deletion confirmation
    """
    task = db_manager.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    # Delete associated files
    for file_type in ["audio", "translation"]:
        if file_type == "audio":
            file_path = RESULT_DIR / f"{task_id}_audio.mp3"
        else:
            file_path = RESULT_DIR / f"{task_id}_translation.txt"
        
        if file_path.exists():
            file_path.unlink()
    
    # Delete task from database
    db_manager.delete_task(task_id)
    
    logger.info(f"Task {task_id} deleted")
    
    return {"message": f"Task {task_id} deleted successfully"}


@app.on_event("startup")
async def startup_event():
    """Startup tasks"""
    logger.info("🚀 API Server starting...")
    logger.info("📚 Documentation available at /docs")
    logger.info("💾 Database initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown tasks"""
    logger.info("🛑 API Server shutting down...")


# ==================== MAIN ====================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


