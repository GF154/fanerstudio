# 🔄 Kreyòl IA - Workflows Guide

> **Gid konplè pou itilize workflows yo**

## 📋 Table of Contents

- [Audio Workflows](#audio-workflows)
- [Video Workflows](#video-workflows)
- [Batch Processing](#batch-processing)
- [Examples](#examples)

---

## 🎵 Audio Workflows

### 1. Create Audiobook

Kreye liv odyo soti nan yon dokiman (PDF, TXT, DOCX)

```python
from app.workflows import create_audiobook

result = await create_audiobook(
    file_path="input/book.pdf",
    voice="creole-native",
    out_dir="output/audiobook_1"
)

print(result)
# {
#     "audio": "output/audiobook_1/audiobook.mp3",
#     "text_preview": "Premye 500 karaktè..."
# }
```

### 2. Create Podcast

Kreye podcast soti nan URL oswa dokiman

```python
from app.workflows import create_podcast

# Soti nan URL
result = await create_podcast(
    source="https://example.com/article",
    title="Mon Podcast",
    voice="creole-native",
    out_dir="output/podcast_1"
)

# Soti nan fichye
result = await create_podcast(
    source="input/article.txt",
    title="Mon Podcast",
    voice="creole-native",
    out_dir="output/podcast_1"
)

print(result)
# {
#     "title": "Mon Podcast",
#     "parts": ["output/podcast_1/podcast_part_1.mp3"]
# }
```

### 3. Generate AI Script

Jenere skrip ak IA soti nan pwonp

```python
from app.workflows import generate_script

script = await generate_script(
    prompt="Kreye yon skrip sou istwa Ayiti"
)

print(script)
```

### 4. URL to Audio

Konvèti kontni URL an odyo

```python
from app.workflows import url_to_audio

result = await url_to_audio(
    url="https://example.com/article",
    voice="creole-native",
    out_dir="output/url_audio"
)

print(result)
# {
#     "audio": "output/url_audio/url_audio.mp3",
#     "url": "https://example.com/article",
#     "text_length": 1234
# }
```

---

## 🎬 Video Workflows

### 1. Add Video Voiceover

Ajoute vwadeyò nan videyo

```python
from app.workflows import add_video_voiceover

result = await add_video_voiceover(
    video_file="input/video.mp4",
    voice="creole-native",
    out_dir="output/video_voiceover"
)

print(result)
# {"video": "output/video_voiceover/video_with_voiceover.mp4"}
```

### 2. Add SFX and Music

Ajoute efè son ak mizik

```python
from app.workflows import add_sfx_and_music

result = await add_sfx_and_music(
    video_file="input/video.mp4",
    out_dir="output/video_sfx"
)

print(result)
# {"video": "output/video_sfx/video_with_sfx.mp4"}
```

### 3. Add Captions

Ajoute soutit otomatik

```python
from app.workflows import add_captions

result = await add_captions(
    video_file="input/video.mp4",
    language="ht",  # Kreyòl Ayisyen
    out_dir="output/video_captions"
)

print(result)
# {
#     "srt": "output/video_captions/captions.srt",
#     "language": "ht"
# }
```

### 4. Remove Background Noise

Retire bri background

```python
from app.workflows import remove_background_noise

result = await remove_background_noise(
    video_file="input/noisy_video.mp4",
    out_dir="output/video_clean"
)

print(result)
# {"video": "output/video_clean/video_denoised.mp4"}
```

### 5. Fix Voiceover Mistakes

Korije erè nan vwadeyò

```python
from app.workflows import fix_voiceover_mistakes

result = await fix_voiceover_mistakes(
    video_file="input/video.mp4",
    voice="creole-native",
    out_dir="output/video_fixed"
)

print(result)
# {"video": "output/video_fixed/video_fixed_voiceover.mp4"}
```

### 6. AI Soundtrack Generator

Jenere soundtrack ak IA

```python
from app.workflows import ai_soundtrack_generator

result = await ai_soundtrack_generator(
    video_file="input/video.mp4",
    out_dir="output/soundtrack"
)

print(result)
# {"soundtrack": "output/soundtrack/ai_soundtrack.mp3"}
```

---

## 📦 Batch Processing

### Batch Audiobooks

Pwosese plizyè audiobook an menm tan

```python
from app.workflows import batch_process_audiobooks

results = await batch_process_audiobooks(
    file_paths=[
        "input/book1.pdf",
        "input/book2.pdf",
        "input/book3.pdf"
    ],
    voice="creole-native",
    out_base_dir="output/batch_audiobooks"
)

for i, result in enumerate(results):
    print(f"Book {i+1}: {result}")
```

### Batch URL to Audio

Konvèti plizyè URL an odyo

```python
from app.workflows import batch_url_to_audio

results = await batch_url_to_audio(
    urls=[
        "https://example.com/article1",
        "https://example.com/article2",
        "https://example.com/article3"
    ],
    voice="creole-native",
    out_base_dir="output/batch_urls"
)

for i, result in enumerate(results):
    print(f"URL {i+1}: {result}")
```

---

## 💡 Complete Examples

### Example 1: Full Audiobook Pipeline

```python
import asyncio
from app.workflows import create_audiobook

async def main():
    # Kreye audiobook soti nan PDF
    result = await create_audiobook(
        file_path="books/haitian_history.pdf",
        voice="creole-native",
        out_dir="output/haitian_history_audiobook"
    )
    
    print("✅ Audiobook kreye!")
    print(f"📁 Audio: {result['audio']}")
    print(f"📝 Preview: {result['text_preview']}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Example 2: Podcast from Website

```python
import asyncio
from app.workflows import create_podcast

async def main():
    # Kreye podcast soti nan atik wèb
    result = await create_podcast(
        source="https://wikipedia.org/wiki/Haiti",
        title="Istwa Ayiti",
        voice="creole-native",
        out_dir="output/haiti_podcast"
    )
    
    print("✅ Podcast kreye!")
    print(f"🎙️ Title: {result['title']}")
    print(f"📁 Parts: {len(result['parts'])} fichye")
    
    for i, part in enumerate(result['parts']):
        print(f"   Part {i+1}: {part}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Example 3: Video Processing Pipeline

```python
import asyncio
from app.workflows import (
    add_video_voiceover,
    add_captions,
    remove_background_noise
)

async def main():
    video_file = "input/my_video.mp4"
    
    # 1. Retire bri
    print("🔧 Retire bri background...")
    clean_result = await remove_background_noise(
        video_file=video_file,
        out_dir="output/step1_clean"
    )
    
    # 2. Ajoute vwadeyò
    print("🗣️ Ajoute vwadeyò...")
    voice_result = await add_video_voiceover(
        video_file=clean_result['video'],
        voice="creole-native",
        out_dir="output/step2_voice"
    )
    
    # 3. Ajoute soutit
    print("📝 Ajoute soutit...")
    caption_result = await add_captions(
        video_file=voice_result['video'],
        language="ht",
        out_dir="output/step3_captions"
    )
    
    print("✅ Tout etap konplete!")
    print(f"📁 Final video: {voice_result['video']}")
    print(f"📁 Captions: {caption_result['srt']}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Example 4: Batch Processing

```python
import asyncio
from app.workflows import batch_process_audiobooks

async def main():
    # Pwosese plizyè liv an menm tan
    books = [
        "books/book1.pdf",
        "books/book2.pdf",
        "books/book3.pdf",
        "books/book4.pdf",
        "books/book5.pdf"
    ]
    
    print(f"📚 Pwosese {len(books)} liv...")
    
    results = await batch_process_audiobooks(
        file_paths=books,
        voice="creole-native",
        out_base_dir="output/batch_books"
    )
    
    print(f"✅ {len(results)} audiobook kreye!")
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"❌ Book {i+1}: Erè - {result}")
        else:
            print(f"✅ Book {i+1}: {result['audio']}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🚀 Using in FastAPI

Entegre workflows nan API endpoints:

```python
from fastapi import FastAPI, UploadFile, File, Form
from app.workflows import create_audiobook
import tempfile
from pathlib import Path

app = FastAPI()

@app.post("/api/workflow/audiobook")
async def workflow_audiobook(
    file: UploadFile = File(...),
    voice: str = Form("creole-native")
):
    # Save uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    
    # Create output directory
    out_dir = f"output/audiobook_{file.filename}"
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    
    # Process audiobook
    result = await create_audiobook(tmp_path, voice, out_dir)
    
    # Cleanup
    Path(tmp_path).unlink()
    
    return result
```

---

## 📝 Notes

### Features Currently Available ✅
- Text-to-Speech (TTS)
- Document text extraction
- HTML to text conversion
- Basic audiobook creation
- Basic podcast creation

### Features In Development 🚧
- Multi-speaker podcasts
- Video voiceover
- SFX addition
- Caption generation
- Audio denoising
- Voiceover correction
- AI soundtrack generation

### TODO
- [ ] Implement Whisper for STT
- [ ] Add moviepy for video processing
- [ ] Integrate noisereduce library
- [ ] Add OpenAI for script generation
- [ ] Implement music generation API
- [ ] Add progress tracking
- [ ] Add webhook notifications
- [ ] Implement retry logic

---

**Fèt ak ❤️ pou kominote Kreyòl Ayisyen** 🇭🇹

