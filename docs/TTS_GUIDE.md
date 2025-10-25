# 🗣️ Text-to-Speech (TTS) Guide

> **Gid konplè pou itilize TTS ak plizyè engines**

## 🎯 TTS Engines Disponib

### 1. 🇭🇹 Kreyòl Natif (Default)
- **Engine**: Facebook MMS-TTS Haitian
- **Gratis**: ✅ Wi
- **Kalite**: Bon pou Kreyòl Ayisyen
- **Voice ID**: `creole-native`

### 2. 🤖 OpenAI TTS
- **Engine**: OpenAI TTS-1 / TTS-1-HD
- **Gratis**: ❌ Non (bezwen API key)
- **Kalite**: Trè bon
- **Vwa**: 6 vwa disponib
- **Voice IDs**: 
  - `openai-alloy` (neutral)
  - `openai-echo` (male)
  - `openai-fable` (neutral)
  - `openai-onyx` (male)
  - `openai-nova` (female)
  - `openai-shimmer` (female)

### 3. 🎙️ ElevenLabs
- **Engine**: ElevenLabs Multilingual v2
- **Gratis**: ❌ Non (bezwen API key)
- **Kalite**: Ekselan
- **Vwa**: Custom voice cloning disponib
- **Voice ID**: `elevenlabs-<voice_id>`

---

## 🔧 Configuration

### 1. Kreye Fichye `.env`

```bash
# Kòpye template
cp .env_studio_example .env
```

### 2. Ajoute API Keys

Modifye `.env`:

```env
# OpenAI TTS
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ElevenLabs
ELEVENLABS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 📝 Usage Examples

### Python API

#### 1. Kreyòl Natif (Default)

```python
from app.services.tts_service import text_to_speech_file

# Generate audio
audio_path = await text_to_speech_file(
    text="Bonjou! Kijan ou ye?",
    output_path="output/hello.mp3",
    voice="creole-native"
)

print(f"Audio saved: {audio_path}")
```

#### 2. OpenAI TTS

```python
from app.services.tts_service import text_to_speech_file

# Generate with OpenAI
audio_path = await text_to_speech_file(
    text="Hello! How are you today?",
    output_path="output/hello_openai.mp3",
    voice="openai-nova"  # Female voice
)

print(f"Audio saved: {audio_path}")
```

#### 3. ElevenLabs

```python
from app.services.tts_service import text_to_speech_file

# Generate with ElevenLabs
# Replace with your actual voice ID
audio_path = await text_to_speech_file(
    text="Hello from ElevenLabs!",
    output_path="output/hello_elevenlabs.mp3",
    voice="elevenlabs-21m00Tcm4TlvDq8ikWAM"
)

print(f"Audio saved: {audio_path}")
```

---

## 🌐 REST API

### Get Available Voices

```bash
GET http://localhost:8000/api/voices
```

**Response:**
```json
{
  "status": "siksè",
  "voices": [
    {
      "id": "creole-native",
      "name": "🇭🇹 Kreyòl Ayisyen (Natif)",
      "language": "ht",
      "gender": "neutral",
      "engine": "native"
    },
    {
      "id": "openai-alloy",
      "name": "OpenAI Alloy",
      "language": "multilingual",
      "gender": "neutral",
      "engine": "openai"
    }
  ],
  "total": 7
}
```

### Generate Speech

```bash
POST http://localhost:8000/api/tts
Content-Type: multipart/form-data

text: "Bonjou! Sa ou ap fè?"
voice: "creole-native"
```

**Response:**
```json
{
  "status": "siksè",
  "message": "Odyo kreye avèk siksè! ✅",
  "audio_url": "/output/tts_20250123_120000_abc123.mp3",
  "text_length": 22
}
```

---

## 💰 Pricing

### Kreyòl Natif
- **Prix**: GRATIS ✅
- **Limit**: Okenn limit

### OpenAI TTS
- **Prix**: $15.00 / 1M characters (TTS-1)
- **Prix HD**: $30.00 / 1M characters (TTS-1-HD)
- **Example**: 1,000 characters = $0.015
- **Link**: https://openai.com/pricing

### ElevenLabs
- **Free Tier**: 10,000 characters/month
- **Starter**: $5/month - 30,000 characters
- **Creator**: $22/month - 100,000 characters
- **Pro**: $99/month - 500,000 characters
- **Link**: https://elevenlabs.io/pricing

---

## 🎨 Voice Customization

### OpenAI

Choose voice based on your needs:
- **alloy**: Balanced, neutral tone
- **echo**: Male, clear articulation
- **fable**: Warm, expressive
- **onyx**: Deep, authoritative male
- **nova**: Friendly, energetic female
- **shimmer**: Soft, gentle female

### ElevenLabs

1. **Get Voice ID**: 
   - Go to https://elevenlabs.io/voice-library
   - Choose a voice
   - Copy the Voice ID

2. **Use Custom Voice**:
   ```python
   voice="elevenlabs-21m00Tcm4TlvDq8ikWAM"
   ```

3. **Clone Your Voice**:
   - Upload samples of your voice
   - Get custom voice ID
   - Use it in the app!

---

## 🔍 Finding ElevenLabs Voice IDs

### Method 1: Voice Library
1. Visit https://elevenlabs.io/voice-library
2. Click on a voice
3. Copy the Voice ID from URL

### Method 2: API
```python
import httpx
import os

async def get_elevenlabs_voices():
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.elevenlabs.io/v1/voices",
            headers={"xi-api-key": api_key}
        )
        
        voices = response.json()
        for voice in voices["voices"]:
            print(f"{voice['name']}: {voice['voice_id']}")

# Run it
import asyncio
asyncio.run(get_elevenlabs_voices())
```

---

## 🚀 Production Tips

### 1. Cache Audio Files
```python
import hashlib

def get_cache_path(text: str, voice: str) -> str:
    """Generate cache path based on text + voice"""
    text_hash = hashlib.md5(f"{text}:{voice}".encode()).hexdigest()
    return f"cache/audio/{text_hash}.mp3"

async def generate_with_cache(text: str, voice: str):
    cache_path = get_cache_path(text, voice)
    
    if Path(cache_path).exists():
        print("Using cached audio")
        return cache_path
    
    return await text_to_speech_file(text, cache_path, voice)
```

### 2. Batch Processing
```python
async def batch_tts(texts: list, voice: str = "creole-native"):
    tasks = []
    for i, text in enumerate(texts):
        output = f"output/batch_{i}.mp3"
        tasks.append(text_to_speech_file(text, output, voice))
    
    return await asyncio.gather(*tasks)

# Use it
texts = ["Text 1", "Text 2", "Text 3"]
results = await batch_tts(texts, voice="openai-nova")
```

### 3. Error Handling
```python
async def safe_tts(text: str, output: str, voice: str):
    try:
        return await text_to_speech_file(text, output, voice)
    except ValueError as e:
        # API key not configured - fallback to native
        print(f"⚠️ {e}")
        print("Falling back to native Creole TTS")
        return await text_to_speech_file(text, output, "creole-native")
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
```

---

## 🐛 Troubleshooting

### Error: "OPENAI_API_KEY pa konfigire"
**Solution**: Set your OpenAI API key in `.env`:
```env
OPENAI_API_KEY=sk-proj-your-key-here
```

### Error: "ELEVENLABS_API_KEY pa konfigire"
**Solution**: Set your ElevenLabs API key in `.env`:
```env
ELEVENLABS_API_KEY=your-key-here
```

### Audio Quality Issues
- **OpenAI**: Use `tts-1-hd` model for better quality (change in code)
- **ElevenLabs**: Adjust `stability` and `similarity_boost` parameters
- **Native**: Check text language (best for Haitian Creole)

### Slow Generation
- Use caching (see Production Tips)
- Use batch processing for multiple files
- Consider using faster `tts-1` instead of `tts-1-hd`

---

## 📚 Additional Resources

- **OpenAI TTS Docs**: https://platform.openai.com/docs/guides/text-to-speech
- **ElevenLabs Docs**: https://docs.elevenlabs.io/
- **Facebook MMS**: https://huggingface.co/facebook/mms-tts-hat

---

**Kreye ak ❤️ pou kominote Kreyòl Ayisyen** 🇭🇹

