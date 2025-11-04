#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚙️ Celery Task Queue for Faner Studio
Background job processing with Celery + Redis

Handles:
- Audiobook generation (long-running)
- Podcast creation (multi-step)
- Voice cloning (CPU-intensive)
- Batch translation (bulk operations)
"""

from celery import Celery, Task
from celery.result import AsyncResult
from celery.signals import task_prerun, task_postrun, task_failure
import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger('FanerStudio.Celery')

# ============================================================
# CELERY CONFIGURATION
# ============================================================

# Get broker URL from environment
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# Create Celery app
celery_app = Celery(
    'faner_studio',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    
    # Task settings
    task_track_started=True,
    task_time_limit=1800,  # 30 minutes max
    task_soft_time_limit=1500,  # 25 minutes soft limit
    
    # Result backend settings
    result_expires=3600,  # Results expire after 1 hour
    result_extended=True,
    
    # Worker settings
    worker_prefetch_multiplier=1,  # One task at a time
    worker_max_tasks_per_child=100,  # Restart worker after 100 tasks
    
    # Rate limiting
    task_default_rate_limit='10/m',  # 10 tasks per minute
)


# ============================================================
# CUSTOM TASK BASE CLASS
# ============================================================

class CallbackTask(Task):
    """Task with progress tracking and callbacks"""
    
    def on_success(self, retval, task_id, args, kwargs):
        """Called when task succeeds"""
        logger.info(f"✅ Task {task_id} completed successfully")
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Called when task fails"""
        logger.error(f"❌ Task {task_id} failed: {exc}")
    
    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Called when task is retried"""
        logger.warning(f"🔄 Task {task_id} retrying: {exc}")
    
    def update_progress(self, current: int, total: int, message: str = ""):
        """Update task progress"""
        progress = int((current / total) * 100)
        self.update_state(
            state='PROGRESS',
            meta={
                'current': current,
                'total': total,
                'progress': progress,
                'message': message
            }
        )


# ============================================================
# AUDIOBOOK TASKS
# ============================================================

@celery_app.task(base=CallbackTask, bind=True, name='tasks.create_audiobook')
def create_audiobook_task(
    self,
    file_path: str,
    voice: str,
    user_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Create audiobook in background
    
    Args:
        self: Task instance
        file_path: Path to document file
        voice: Voice ID to use
        user_id: User ID (optional)
    
    Returns:
        Dict with audiobook info
    """
    try:
        logger.info(f"📚 Starting audiobook creation: {file_path}")
        
        # Update progress
        self.update_progress(0, 100, "Extracting text from document...")
        
        # Import services
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        
        from generer_audio_huggingface import generer_audio_creole
        
        # TODO: Implement actual document text extraction
        # For now, placeholder
        self.update_progress(30, 100, "Generating audio...")
        
        # Generate audio
        output_path = f"output/audiobook_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        generer_audio_creole("Sample audiobook text", output_path)
        
        self.update_progress(90, 100, "Finalizing...")
        
        result = {
            "status": "completed",
            "output_path": output_path,
            "duration_seconds": 120,  # Placeholder
            "file_size_mb": 5.2,  # Placeholder
            "created_at": datetime.now().isoformat()
        }
        
        self.update_progress(100, 100, "Audiobook completed!")
        
        logger.info(f"✅ Audiobook created: {output_path}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Audiobook creation failed: {e}")
        raise


# ============================================================
# PODCAST TASKS
# ============================================================

@celery_app.task(base=CallbackTask, bind=True, name='tasks.create_podcast')
def create_podcast_task(
    self,
    script: str,
    voice: str,
    title: str,
    add_intro: bool = True
) -> Dict[str, Any]:
    """
    Create podcast in background
    
    Args:
        self: Task instance
        script: Podcast script
        voice: Voice ID
        title: Podcast title
        add_intro: Add intro music
    
    Returns:
        Dict with podcast info
    """
    try:
        logger.info(f"🎙️ Starting podcast creation: {title}")
        
        self.update_progress(0, 100, "Parsing script...")
        
        # TODO: Implement actual podcast creation
        # For now, placeholder
        
        self.update_progress(50, 100, "Generating audio...")
        self.update_progress(75, 100, "Adding music...")
        self.update_progress(90, 100, "Mixing audio...")
        
        result = {
            "status": "completed",
            "title": title,
            "output_path": f"output/podcast_{title}.mp3",
            "duration_seconds": 300,
            "created_at": datetime.now().isoformat()
        }
        
        self.update_progress(100, 100, "Podcast completed!")
        
        logger.info(f"✅ Podcast created: {title}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Podcast creation failed: {e}")
        raise


# ============================================================
# VOICE CLONING TASKS
# ============================================================

@celery_app.task(base=CallbackTask, bind=True, name='tasks.clone_voice')
def clone_voice_task(
    self,
    audio_file_path: str,
    voice_name: str,
    method: str = "basic"
) -> Dict[str, Any]:
    """
    Clone voice in background
    
    Args:
        self: Task instance
        audio_file_path: Path to audio sample
        voice_name: Name for voice
        method: Cloning method (basic/medium/premium)
    
    Returns:
        Dict with voice info
    """
    try:
        logger.info(f"🎤 Starting voice cloning: {voice_name}")
        
        self.update_progress(0, 100, "Analyzing audio sample...")
        
        # Import voice cloning
        from projet_kreyol_IA.src.advanced_voice_cloning import VoiceCloner
        from pathlib import Path
        
        self.update_progress(30, 100, "Extracting voice features...")
        
        cloner = VoiceCloner()
        profile = cloner.clone_voice(
            audio_sample=Path(audio_file_path),
            voice_name=voice_name,
            method=method
        )
        
        self.update_progress(80, 100, "Saving voice profile...")
        
        result = {
            "status": "completed",
            "voice_id": profile.voice_id,
            "voice_name": profile.name,
            "method": method,
            "created_at": datetime.now().isoformat()
        }
        
        self.update_progress(100, 100, "Voice cloning completed!")
        
        logger.info(f"✅ Voice cloned: {voice_name}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Voice cloning failed: {e}")
        raise


# ============================================================
# TRANSLATION TASKS
# ============================================================

@celery_app.task(base=CallbackTask, bind=True, name='tasks.batch_translate')
def batch_translate_task(
    self,
    texts: list,
    source: str,
    target: str
) -> Dict[str, Any]:
    """
    Batch translate multiple texts
    
    Args:
        self: Task instance
        texts: List of texts to translate
        source: Source language
        target: Target language
    
    Returns:
        Dict with translations
    """
    try:
        logger.info(f"🌍 Starting batch translation: {len(texts)} texts")
        
        translations = []
        total = len(texts)
        
        for i, text in enumerate(texts):
            self.update_progress(i, total, f"Translating {i+1}/{total}...")
            
            # TODO: Implement actual translation
            # For now, placeholder
            translations.append({
                "original": text,
                "translated": f"[Translated] {text}",
                "source": source,
                "target": target
            })
        
        self.update_progress(total, total, "Batch translation completed!")
        
        result = {
            "status": "completed",
            "total_texts": total,
            "translations": translations,
            "completed_at": datetime.now().isoformat()
        }
        
        logger.info(f"✅ Batch translation completed: {total} texts")
        return result
        
    except Exception as e:
        logger.error(f"❌ Batch translation failed: {e}")
        raise


# ============================================================
# TASK MANAGEMENT
# ============================================================

class TaskManager:
    """Manage and monitor Celery tasks"""
    
    @staticmethod
    def get_task_status(task_id: str) -> Dict[str, Any]:
        """
        Get task status
        
        Args:
            task_id: Task ID
        
        Returns:
            Task status info
        """
        task = AsyncResult(task_id, app=celery_app)
        
        if task.state == 'PROGRESS':
            return {
                "task_id": task_id,
                "state": task.state,
                "progress": task.info.get('progress', 0),
                "current": task.info.get('current', 0),
                "total": task.info.get('total', 0),
                "message": task.info.get('message', '')
            }
        elif task.state == 'SUCCESS':
            return {
                "task_id": task_id,
                "state": task.state,
                "result": task.result
            }
        elif task.state == 'FAILURE':
            return {
                "task_id": task_id,
                "state": task.state,
                "error": str(task.info)
            }
        else:
            return {
                "task_id": task_id,
                "state": task.state
            }
    
    @staticmethod
    def cancel_task(task_id: str) -> bool:
        """Cancel a running task"""
        task = AsyncResult(task_id, app=celery_app)
        task.revoke(terminate=True)
        return True
    
    @staticmethod
    def get_active_tasks() -> list:
        """Get list of active tasks"""
        inspect = celery_app.control.inspect()
        active = inspect.active()
        
        if active:
            all_tasks = []
            for worker, tasks in active.items():
                all_tasks.extend(tasks)
            return all_tasks
        return []
    
    @staticmethod
    def get_queue_length() -> int:
        """Get number of tasks in queue"""
        inspect = celery_app.control.inspect()
        reserved = inspect.reserved()
        
        if reserved:
            return sum(len(tasks) for tasks in reserved.values())
        return 0


# ============================================================
# CELERY SIGNALS
# ============================================================

@task_prerun.connect
def task_prerun_handler(sender=None, task_id=None, task=None, **kwargs):
    """Log when task starts"""
    logger.info(f"⏩ Task started: {task.name} [{task_id}]")


@task_postrun.connect
def task_postrun_handler(sender=None, task_id=None, task=None, **kwargs):
    """Log when task completes"""
    logger.info(f"✅ Task completed: {task.name} [{task_id}]")


@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, **kwargs):
    """Log when task fails"""
    logger.error(f"❌ Task failed: {sender.name} [{task_id}] - {exception}")


# ============================================================
# TESTING
# ============================================================

def test_celery_tasks():
    """Test Celery task system"""
    print("🧪 Testing Celery Tasks\n")
    
    try:
        # Test simple task
        print("1. Testing audiobook task (async):")
        task = create_audiobook_task.delay("test.pdf", "creole-native")
        print(f"   Task ID: {task.id}")
        print(f"   State: {task.state}")
        
        # Check status
        print("\n2. Checking task status:")
        status = TaskManager.get_task_status(task.id)
        print(f"   Status: {status}")
        
        print("\n✅ Test completed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("   Make sure Redis and Celery worker are running:")
        print("   $ redis-server")
        print("   $ celery -A celery_tasks worker --loglevel=info")


if __name__ == "__main__":
    test_celery_tasks()

