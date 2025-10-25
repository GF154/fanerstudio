#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 Background Tasks with Celery
Sistèm task asenkwon pou pwosesis long
"""

from celery import Celery
from pathlib import Path
import os
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure Celery
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    'kreyol_ia',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['app.tasks']
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Port-au-Prince',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max
    task_soft_time_limit=3300,  # 55 minutes soft limit
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
)

# ============================================================
# AUDIOBOOK TASKS
# ============================================================

@celery_app.task(bind=True, name='app.tasks.process_audiobook')
def process_audiobook(self, file_path: str, voice: str, max_pages: int = None):
    """
    Pwosese audiobook nan background ak progress tracking
    
    Args:
        self: Task instance (auto-injected by bind=True)
        file_path: Chemen fichye dokiman
        voice: Vwa pou itilize
        max_pages: Limit paj (optional)
    
    Returns:
        dict: Rezilta ak chemen fichye yo
    """
    try:
        from app.services.media_service import MediaService
        from app.services.tts_service import TTSService
        import asyncio
        
        print(f"\n{'='*60}")
        print(f"📚 BACKGROUND AUDIOBOOK TASK START")
        print(f"   Task ID: {self.request.id}")
        print(f"   File: {file_path}")
        print(f"   Voice: {voice}")
        print(f"{'='*60}\n")
        
        # Update state: Starting
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 0,
                'total': 100,
                'status': 'Kòmanse pwosesis...',
                'stage': 'initialization'
            }
        )
        
        # Initialize services
        media_service = MediaService()
        tts_service = TTSService()
        
        # Stage 1: Extract text (0-40%)
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 5,
                'total': 100,
                'status': 'Ekstrè tèks soti nan dokiman...',
                'stage': 'extraction'
            }
        )
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        text = loop.run_until_complete(
            media_service.extract_text_from_document(
                file_path,
                max_pages=max_pages,
                show_progress=False  # We handle progress here
            )
        )
        
        if not text or len(text.strip()) < 10:
            raise ValueError("Dokiman an vid oswa pa gen ase tèks!")
        
        word_count = len(text.split())
        char_count = len(text)
        
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 40,
                'total': 100,
                'status': f'Ekstraksyon konple! {word_count:,} mo ekstrè.',
                'stage': 'extraction_complete',
                'word_count': word_count,
                'char_count': char_count
            }
        )
        
        # Stage 2: Generate audio (40-90%)
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 45,
                'total': 100,
                'status': 'Jenere odyo...',
                'stage': 'audio_generation'
            }
        )
        
        from datetime import datetime
        audio_filename = f"audiobook_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        audio_path = Path("output") / audio_filename
        audio_path.parent.mkdir(exist_ok=True)
        
        # Generate audio
        loop.run_until_complete(
            tts_service.text_to_speech_file(text, str(audio_path), voice)
        )
        
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 85,
                'total': 100,
                'status': 'Odyo kreye! Finalizasyon...',
                'stage': 'audio_complete'
            }
        )
        
        # Stage 3: Save metadata (90-100%)
        preview_filename = f"audiobook_{datetime.now().strftime('%Y%m%d_%H%M%S')}_text.txt"
        preview_path = Path("output") / preview_filename
        preview_path.write_text(
            text[:1000] + "..." if len(text) > 1000 else text,
            encoding='utf-8'
        )
        
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 95,
                'total': 100,
                'status': 'Finalizasyon...',
                'stage': 'finalization'
            }
        )
        
        # Cleanup
        Path(file_path).unlink(missing_ok=True)
        
        # Final result
        result = {
            'status': 'success',
            'audio': f"/output/{audio_filename}",
            'preview': f"/output/{preview_filename}",
            'stats': {
                'word_count': word_count,
                'char_count': char_count,
                'voice': voice
            }
        }
        
        print(f"\n✅ AUDIOBOOK TASK COMPLETE!")
        print(f"   Audio: {audio_filename}")
        print(f"   Words: {word_count:,}")
        print(f"{'='*60}\n")
        
        return result
        
    except Exception as e:
        print(f"\n❌ AUDIOBOOK TASK FAILED: {str(e)}\n")
        self.update_state(
            state='FAILURE',
            meta={
                'current': 0,
                'total': 100,
                'status': f'Erè: {str(e)}',
                'stage': 'failed',
                'error': str(e)
            }
        )
        raise


@celery_app.task(bind=True, name='app.tasks.process_translation')
def process_translation(self, text: str, target_lang: str):
    """
    Pwosese tradiksyon nan background
    
    Args:
        text: Tèks pou tradwi
        target_lang: Lang sib
    
    Returns:
        dict: Rezilta tradiksyon
    """
    try:
        from traduire_texte import traduire_avec_progress
        
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 10,
                'total': 100,
                'status': 'Kòmanse tradiksyon...'
            }
        )
        
        # Translate
        translated = traduire_avec_progress(text, langue_cible=target_lang)
        
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 90,
                'total': 100,
                'status': 'Tradiksyon konple!'
            }
        )
        
        return {
            'status': 'success',
            'original': text,
            'translated': translated,
            'target_lang': target_lang,
            'char_count': len(translated)
        }
        
    except Exception as e:
        self.update_state(
            state='FAILURE',
            meta={'error': str(e)}
        )
        raise


@celery_app.task(bind=True, name='app.tasks.process_pdf_extraction')
def process_pdf_extraction(self, file_path: str, max_pages: int = None):
    """
    Ekstrè tèks soti nan PDF nan background
    
    Args:
        file_path: Chemen fichye PDF
        max_pages: Limit paj
    
    Returns:
        dict: Tèks ekstrè ak stats
    """
    try:
        from app.services.media_service import MediaService
        import asyncio
        
        media_service = MediaService()
        
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 10,
                'total': 100,
                'status': 'Ekstrè PDF...'
            }
        )
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        text = loop.run_until_complete(
            media_service.extract_text_from_document(
                file_path,
                max_pages=max_pages,
                show_progress=False
            )
        )
        
        self.update_state(
            state='PROGRESS',
            meta={
                'current': 90,
                'total': 100,
                'status': 'Ekstraksyon konple!'
            }
        )
        
        # Cleanup
        Path(file_path).unlink(missing_ok=True)
        
        return {
            'status': 'success',
            'text': text,
            'word_count': len(text.split()),
            'char_count': len(text)
        }
        
    except Exception as e:
        self.update_state(
            state='FAILURE',
            meta={'error': str(e)}
        )
        raise


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def get_task_status(task_id: str) -> dict:
    """
    Jwenn status yon task
    
    Args:
        task_id: ID task la
    
    Returns:
        dict: Status ak metadata
    """
    task = celery_app.AsyncResult(task_id)
    
    if task.state == 'PENDING':
        return {
            'state': 'PENDING',
            'status': 'Tann...',
            'progress': 0
        }
    elif task.state == 'PROGRESS':
        return {
            'state': 'PROGRESS',
            'status': task.info.get('status', 'Ap pwosese...'),
            'progress': task.info.get('current', 0),
            'total': task.info.get('total', 100),
            'stage': task.info.get('stage', 'processing'),
            **task.info
        }
    elif task.state == 'SUCCESS':
        return {
            'state': 'SUCCESS',
            'status': 'Konple!',
            'progress': 100,
            'result': task.result
        }
    elif task.state == 'FAILURE':
        return {
            'state': 'FAILURE',
            'status': 'Echwe',
            'progress': 0,
            'error': str(task.info)
        }
    else:
        return {
            'state': task.state,
            'status': 'Unknown',
            'progress': 0
        }


if __name__ == "__main__":
    print("🔄 Celery Worker")
    print("=" * 60)
    print("Pou lance worker la:")
    print("  celery -A app.tasks worker --loglevel=info --pool=solo")
    print("=" * 60)

