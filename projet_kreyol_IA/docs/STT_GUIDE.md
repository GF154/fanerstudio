# 📝 Speech-to-Text (STT) Guide

> **Gid konplè pou itilize Speech-to-Text ak plizyè engines**

## 🎯 STT Engines Disponib

### 1. 🎤 Whisper Local (Recommended for Free)
- **Provider**: OpenAI (Open Source)
- **Gratis**: ✅ Wi
- **Kalite**: Trè bon
- **Vitès**: Mwayen (depend sou hardware)
- **Requirements**: `pip install openai-whisper`
- **Engine ID**: `whisper-local`

### 2. ☁️ Whisper OpenAI API
- **Provider**: OpenAI
- **Gratis**: ❌ Non (bezwen API key)
- **Kalite**: Ekselan
- **Vitès**: Rapid
- **Pri**: $0.006 / minute
- **Engine ID**: `whisper-openai`

### 3. 🚀 AssemblyAI
- **Provider**: AssemblyAI
- **Gratis**: ❌ Non (bezwen API key, 10K characters free/month)
- **Kalite**: Trè bon ak features avanse
- **Vitès**: Rapid
- **Pri**: $0.00025 / second ($0.015 / minute)
- **Engine ID**: `assemblyai`

---

## 🔧 Setup & Installation

### Option 1: Whisper Local (Free)

```bash
# Install Whisper
pip install openai-whisper

# Optional: Install ffmpeg (required for some audio formats)
# Windows: choco install ffmpeg
# Mac: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

### Option 2: OpenAI Whisper API

1. Get API key: https://platform.openai.com/api-keys

2. Add to `.env`:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

### Option 3: AssemblyAI

1. Get API key: https://www.assemblyai.com/dashboard/signup

2. Add to `.env`:
```env
ASSEMBLYAI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 📝 Usage Examples

### Python API

#### 1. Auto Mode (Recommended)

```python
from app.services.stt_service import transcribe_audio

# Automatically choose best available engine
text = await transcribe_audio(
    audio_path="audio/recording.mp3",
    engine="auto"
)

print(f"Transcription: {text}")
```

**Auto mode logic:**
1. Try local Whisper (free)
2. If not available, try OpenAI Whisper API
3. If not available, try AssemblyAI
4. If none available, raise error

#### 2. Whisper Local

```python
from app.services.stt_service import transcribe_audio

# Use local Whisper (free, offline)
text = await transcribe_audio(
    audio_path="audio/recording.mp3",
    engine="whisper-local"
)

print(f"Transcription: {text}")
```

#### 3. OpenAI Whisper API

```python
from app.services.stt_service import transcribe_audio

# Use OpenAI Whisper API (fast, paid)
text = await transcribe_audio(
    audio_path="audio/recording.mp3",
    engine="whisper-openai"
)

print(f"Transcription: {text}")
```

#### 4. AssemblyAI

```python
from app.services.stt_service import transcribe_audio

# Use AssemblyAI (fast, paid, advanced features)
text = await transcribe_audio(
    audio_path="audio/recording.mp3",
    engine="assemblyai"
)

print(f"Transcription: {text}")
```

---

## 🌐 REST API

### Get Available Engines

```bash
GET http://localhost:8000/api/stt/engines
```

**Response:**
```json
{
  "status": "siksè",
  "engines": [
    {
      "id": "whisper-local",
      "name": "Whisper Local",
      "provider": "OpenAI",
      "cost": "free",
      "speed": "medium",
      "accuracy": "high"
    },
    {
      "id": "whisper-openai",
      "name": "Whisper API",
      "provider": "OpenAI",
      "cost": "$0.006/minute",
      "speed": "fast",
      "accuracy": "high"
    }
  ],
  "total": 2
}
```

### Transcribe Audio

```bash
POST http://localhost:8000/api/stt
Content-Type: multipart/form-data

file: audio.mp3
engine: auto
```

**Response:**
```json
{
  "status": "siksè",
  "message": "Transkripsyon konplete! 📝✅",
  "text": "Bonjou! Kijan ou ye? Mwen byen, mèsi.",
  "char_count": 35,
  "engine": "whisper-local",
  "file_name": "audio.mp3"
}
```

---

## 💰 Pricing Comparison

| Engine | Cost | Speed | Quality | Offline |
|--------|------|-------|---------|---------|
| **Whisper Local** | FREE | Medium | High | ✅ Yes |
| **Whisper OpenAI** | $0.006/min | Fast | High | ❌ No |
| **AssemblyAI** | $0.015/min | Fast | Very High | ❌ No |

### Cost Examples

**1 hour of audio:**
- Whisper Local: **$0** (FREE)
- OpenAI Whisper: **$0.36**
- AssemblyAI: **$0.90**

**10 hours of audio:**
- Whisper Local: **$0** (FREE)
- OpenAI Whisper: **$3.60**
- AssemblyAI: **$9.00**

---

## 🎨 Whisper Models (Local)

Whisper offers different model sizes. Choose based on your needs:

| Model | Size | Speed | Accuracy | RAM |
|-------|------|-------|----------|-----|
| `tiny` | 39 MB | Very Fast | Good | ~1 GB |
| `base` | 74 MB | Fast | Better | ~1 GB |
| `small` | 244 MB | Medium | Good | ~2 GB |
| `medium` | 769 MB | Slow | Very Good | ~5 GB |
| `large` | 1550 MB | Very Slow | Best | ~10 GB |

**Change model in code:**
```python
# In stt_service.py, line 79:
model = whisper.load_model("small")  # Change from "base" to any model
```

---

## 🌍 Language Support

All engines support Haitian Creole (`ht`). They also support:

- English (en)
- French (fr)
- Spanish (es)
- Portuguese (pt)
- And 90+ more languages!

**Automatic language detection** is available - the engines will detect the language automatically.

---

## 🚀 Production Tips

### 1. Batch Processing

```python
import asyncio
from app.services.stt_service import transcribe_audio

async def batch_transcribe(audio_files: list, engine: str = "auto"):
    tasks = []
    for audio_file in audio_files:
        tasks.append(transcribe_audio(audio_file, engine))
    
    return await asyncio.gather(*tasks, return_exceptions=True)

# Use it
audio_files = ["audio1.mp3", "audio2.mp3", "audio3.mp3"]
results = await batch_transcribe(audio_files, engine="whisper-local")

for i, result in enumerate(results):
    if isinstance(result, Exception):
        print(f"❌ File {i+1}: Error - {result}")
    else:
        print(f"✅ File {i+1}: {result[:50]}...")
```

### 2. Caching Transcriptions

```python
import hashlib
from pathlib import Path
import json

def get_cache_path(audio_path: str, engine: str) -> Path:
    """Generate cache path for transcription"""
    file_hash = hashlib.md5(Path(audio_path).read_bytes()).hexdigest()
    return Path(f"cache/transcriptions/{engine}_{file_hash}.json")

async def transcribe_with_cache(audio_path: str, engine: str = "auto"):
    cache_path = get_cache_path(audio_path, engine)
    
    # Check cache
    if cache_path.exists():
        print("Using cached transcription")
        return json.loads(cache_path.read_text())["text"]
    
    # Transcribe
    text = await transcribe_audio(audio_path, engine)
    
    # Save to cache
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps({"text": text}))
    
    return text
```

### 3. Error Handling with Fallback

```python
async def transcribe_with_fallback(audio_path: str):
    """Try multiple engines with fallback"""
    engines = ["whisper-local", "whisper-openai", "assemblyai"]
    
    for engine in engines:
        try:
            print(f"Trying {engine}...")
            return await transcribe_audio(audio_path, engine)
        except Exception as e:
            print(f"❌ {engine} failed: {e}")
            continue
    
    raise Exception("All STT engines failed!")
```

### 4. Progress Tracking

```python
from tqdm import tqdm

async def transcribe_with_progress(audio_files: list, engine: str = "auto"):
    results = []
    
    with tqdm(total=len(audio_files), desc="Transcribing") as pbar:
        for audio_file in audio_files:
            try:
                text = await transcribe_audio(audio_file, engine)
                results.append({"file": audio_file, "text": text, "status": "success"})
            except Exception as e:
                results.append({"file": audio_file, "error": str(e), "status": "failed"})
            
            pbar.update(1)
    
    return results
```

---

## 🎯 Use Cases

### 1. Podcast Transcription

```python
async def transcribe_podcast(podcast_file: str):
    """Transcribe entire podcast"""
    text = await transcribe_audio(podcast_file, engine="whisper-local")
    
    # Save transcription
    output_file = podcast_file.replace(".mp3", "_transcript.txt")
    Path(output_file).write_text(text, encoding="utf-8")
    
    return text
```

### 2. Video Subtitles

```python
async def generate_subtitles(video_file: str):
    """Extract audio and create subtitles"""
    from moviepy.editor import VideoFileClip
    
    # Extract audio
    video = VideoFileClip(video_file)
    audio_file = video_file.replace(".mp4", "_audio.mp3")
    video.audio.write_audiofile(audio_file)
    
    # Transcribe
    text = await transcribe_audio(audio_file, engine="whisper-openai")
    
    # Create SRT file
    srt_file = video_file.replace(".mp4", ".srt")
    # TODO: Split text into timed segments
    
    return text
```

### 3. Meeting Notes

```python
async def meeting_to_notes(meeting_audio: str):
    """Convert meeting audio to notes"""
    # Transcribe
    transcript = await transcribe_audio(meeting_audio, engine="assemblyai")
    
    # Optional: Use GPT to summarize
    # summary = await generate_summary(transcript)
    
    return transcript
```

---

## 🐛 Troubleshooting

### Error: "Whisper pa enstale!"
**Solution**: Install Whisper
```bash
pip install openai-whisper
```

### Error: "OPENAI_API_KEY pa konfigire!"
**Solution**: Set API key in `.env`
```env
OPENAI_API_KEY=sk-proj-your-key
```

### Error: "ASSEMBLYAI_API_KEY pa konfigire!"
**Solution**: Set API key in `.env`
```env
ASSEMBLYAI_API_KEY=your-key
```

### Whisper Local is Slow
**Solutions:**
1. Use smaller model: `tiny` or `base`
2. Use GPU acceleration (if CUDA available)
3. Use OpenAI Whisper API instead

### Poor Transcription Quality
**Solutions:**
1. Use larger Whisper model (`medium` or `large`)
2. Ensure audio quality is good
3. Remove background noise first
4. Try AssemblyAI for best quality

### Out of Memory Error
**Solutions:**
1. Use smaller Whisper model
2. Use OpenAI or AssemblyAI API
3. Process shorter audio segments

---

## 📚 Additional Resources

- **Whisper GitHub**: https://github.com/openai/whisper
- **OpenAI Whisper API**: https://platform.openai.com/docs/guides/speech-to-text
- **AssemblyAI Docs**: https://www.assemblyai.com/docs
- **Supported Languages**: https://github.com/openai/whisper#available-models-and-languages

---

## 🆚 Which Engine to Choose?

### Use **Whisper Local** if:
- ✅ You want FREE transcription
- ✅ You have decent hardware (CPU/GPU)
- ✅ You need offline capability
- ✅ Privacy is important

### Use **Whisper OpenAI** if:
- ✅ You need fast transcription
- ✅ You don't want to manage models
- ✅ You have budget ($0.006/min)
- ✅ You need cloud processing

### Use **AssemblyAI** if:
- ✅ You need best quality
- ✅ You want advanced features (speaker detection, etc.)
- ✅ You have budget ($0.015/min)
- ✅ You need very fast processing

---

**Kreye ak ❤️ pou kominote Kreyòl Ayisyen** 🇭🇹

