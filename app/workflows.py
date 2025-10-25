#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 Workflows - Orchestration Functions
Fonksyon pou òganize workflow konplè
"""

from app.services.tts_service import text_to_speech_file
from app.services.stt_service import transcribe_audio
from app.services.media_service import (
    extract_text_from_document,
    html_to_text,
    add_voiceover_to_video,
    add_sfx_to_video,
    generate_captions_from_video,
    denoise_audio_in_video,
    correct_voiceover,
    generate_soundtrack_for_video,
)
import os
import asyncio
from pathlib import Path

# ============================================================
# AUDIO WORKFLOWS
# ============================================================

async def create_audiobook(file_path: str, voice: str, out_dir: str) -> dict:
    """
    Kreye liv odyo konplè
    
    Args:
        file_path: Chemen fichye dokiman an
        voice: Vwa pou itilize
        out_dir: Dosye pou sove rezilta yo
        
    Returns:
        dict: Enfòmasyon sou fichye yo kreye
    """
    # 1) Ekstrè tèks si bezwen
    text = await extract_text_from_document(file_path)
    
    # 2) Fè TTS epi sove mp3
    audio_path = os.path.join(out_dir, "audiobook.mp3")
    await text_to_speech_file(text, audio_path, voice)
    
    return {
        "audio": audio_path,
        "text_preview": text[:500]
    }


async def create_podcast(source: str, title: str, voice: str, out_dir: str) -> dict:
    """
    Kreye podcast soti nan URL oswa dokiman
    
    Args:
        source: URL oswa chemen fichye
        title: Tit podcast la
        voice: Vwa pou itilize
        out_dir: Dosye pou sove rezilta yo
        
    Returns:
        dict: Enfòmasyon sou podcast la
    """
    # Si source se url, li paj la; si se yon file path, ekstrè tèks
    if source.startswith("http"):
        text = await html_to_text(source)
    else:
        text = await extract_text_from_document(source)
    
    # Siplemantè: kap koupe an segman podcast, ajoute entwodiksyon, elatriye
    segments = [text]  # Senplifye
    out_files = []
    
    for i, seg in enumerate(segments):
        out_file = os.path.join(out_dir, f"podcast_part_{i+1}.mp3")
        await text_to_speech_file(seg, out_file, voice)
        out_files.append(out_file)
    
    return {
        "title": title,
        "parts": out_files
    }


async def generate_script(prompt: str) -> str:
    """
    Jenere skrip ak IA soti nan yon pwonp
    
    Args:
        prompt: Pwonp pou jenere skrip la
        
    Returns:
        str: Skrip ki jenere
    """
    # Placeholder: rele OpenAI / LLM pou jenere script
    # Retounen script kòm string
    # TODO: Ajoute rele httpx.post(...) pou OpenAI completion/chat/completion
    
    script = f"""
Script Ki Jenere Pou Prompt Sa A:

{prompt}

--- KÒMANSMAN SKRIP ---

[ENTWODIKSYON]
Byenveni! Jodi a n ap pale sou yon sijè enpòtan...

[KÒ PRENSIPAL]
Nan pati sa a, n ap eksplore divès aspè sijè a...

[KONKLIZYON]
An rezime, nou te wè ke...

--- FEN SKRIP ---

Note: Itilize OpenAI API pou pi bon rezilta!
"""
    
    return script


async def url_to_audio(url: str, voice: str, out_dir: str) -> dict:
    """
    Konvèti kontni URL an odyo
    
    Args:
        url: URL paj wèb la
        voice: Vwa pou itilize
        out_dir: Dosye pou sove rezilta yo
        
    Returns:
        dict: Enfòmasyon sou fichye odyo a
    """
    text = await html_to_text(url)
    out_file = os.path.join(out_dir, "url_audio.mp3")
    await text_to_speech_file(text, out_file, voice)
    
    return {
        "audio": out_file,
        "url": url,
        "text_length": len(text)
    }


# ============================================================
# VIDEO WORKFLOWS
# ============================================================

async def add_video_voiceover(video_file: str, voice: str, out_dir: str) -> dict:
    """
    Ajoute vwadeyò nan videyo
    
    Args:
        video_file: Chemen fichye videyo orijinal
        voice: Vwa pou itilize
        out_dir: Dosye pou sove rezilta yo
        
    Returns:
        dict: Enfòmasyon sou videyo ak vwadeyò
    """
    out_video = os.path.join(out_dir, "video_with_voiceover.mp4")
    await add_voiceover_to_video(video_file, out_video, voice)
    
    return {
        "video": out_video
    }


async def add_sfx_and_music(video_file: str, out_dir: str) -> dict:
    """
    Ajoute efè son ak mizik nan videyo
    
    Args:
        video_file: Chemen fichye videyo orijinal
        out_dir: Dosye pou sove rezilta yo
        
    Returns:
        dict: Enfòmasyon sou videyo ak efè
    """
    out_video = os.path.join(out_dir, "video_with_sfx.mp4")
    await add_sfx_to_video(video_file, out_video)
    
    return {
        "video": out_video
    }


async def add_captions(video_file: str, language: str, out_dir: str) -> dict:
    """
    Ajoute soutit nan videyo
    
    Args:
        video_file: Chemen fichye videyo
        language: Lang soutit yo
        out_dir: Dosye pou sove rezilta yo
        
    Returns:
        dict: Enfòmasyon sou fichye soutit
    """
    srt_path = os.path.join(out_dir, "captions.srt")
    await generate_captions_from_video(video_file, srt_path, language)
    
    return {
        "srt": srt_path,
        "language": language
    }


async def remove_background_noise(video_file: str, out_dir: str) -> dict:
    """
    Retire bri background nan videyo
    
    Args:
        video_file: Chemen fichye videyo orijinal
        out_dir: Dosye pou sove rezilta yo
        
    Returns:
        dict: Enfòmasyon sou videyo netwaye
    """
    out_video = os.path.join(out_dir, "video_denoised.mp4")
    await denoise_audio_in_video(video_file, out_video)
    
    return {
        "video": out_video
    }


async def fix_voiceover_mistakes(video_file: str, voice: str, out_dir: str) -> dict:
    """
    Korije erè nan vwadeyò videyo a
    
    Args:
        video_file: Chemen fichye videyo orijinal
        voice: Vwa pou re-jenere pati yo
        out_dir: Dosye pou sove rezilta yo
        
    Returns:
        dict: Enfòmasyon sou videyo korije
    """
    out_video = os.path.join(out_dir, "video_fixed_voiceover.mp4")
    await correct_voiceover(video_file, out_video, voice)
    
    return {
        "video": out_video
    }


async def ai_soundtrack_generator(video_file: str, out_dir: str) -> dict:
    """
    Jenere soundtrack ak IA pou videyo
    
    Args:
        video_file: Chemen fichye videyo
        out_dir: Dosye pou sove rezilta yo
        
    Returns:
        dict: Enfòmasyon sou soundtrack la
    """
    soundtrack_path = os.path.join(out_dir, "ai_soundtrack.mp3")
    await generate_soundtrack_for_video(video_file, soundtrack_path)
    
    # Optionally merge soundtrack to video
    return {
        "soundtrack": soundtrack_path
    }


# ============================================================
# BATCH PROCESSING
# ============================================================

async def batch_process_audiobooks(file_paths: list, voice: str, out_base_dir: str) -> list:
    """
    Pwosese plizyè audiobook an menm tan
    
    Args:
        file_paths: Lis chemen fichye yo
        voice: Vwa pou itilize
        out_base_dir: Dosye baz pou sove rezilta yo
        
    Returns:
        list: Lis rezilta yo
    """
    tasks = []
    for i, file_path in enumerate(file_paths):
        out_dir = os.path.join(out_base_dir, f"audiobook_{i+1}")
        os.makedirs(out_dir, exist_ok=True)
        tasks.append(create_audiobook(file_path, voice, out_dir))
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


async def batch_url_to_audio(urls: list, voice: str, out_base_dir: str) -> list:
    """
    Konvèti plizyè URL an odyo an menm tan
    
    Args:
        urls: Lis URL yo
        voice: Vwa pou itilize
        out_base_dir: Dosye baz pou sove rezilta yo
        
    Returns:
        list: Lis rezilta yo
    """
    tasks = []
    for i, url in enumerate(urls):
        out_dir = os.path.join(out_base_dir, f"url_audio_{i+1}")
        os.makedirs(out_dir, exist_ok=True)
        tasks.append(url_to_audio(url, voice, out_dir))
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

