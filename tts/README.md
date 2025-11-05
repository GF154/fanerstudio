# 🎙️ Faner Studio - TTS Engine

Motè TTS (Text-to-Speech) Avanse pou Kreyòl Ayisyen

## 📋 Karakteristik

- ✅ **Multi-Engine Support**: gTTS, Edge TTS, ElevenLabs, OpenAI TTS
- ✅ **Haitian Creole**: Sipò espesyal pou Kreyòl Ayisyen
- ✅ **High Quality**: Vwa HD ak pwofesyonèl
- ✅ **Voice Control**: Kontwòl vitès, ton, emosyon
- ✅ **Async Support**: Pèfòmans rapid ak async/await

## 🚀 Enstalasyon

### Basic (Gratis)
```bash
cd tts
pip install -r requirements.txt
```

### Ak Audio Processing (FFmpeg required)
```bash
pip install -r requirements.txt pydub soundfile
```

### Ak Premium APIs
```bash
pip install -r requirements.txt elevenlabs openai
```

## 📖 Itilizasyon

### Example 1: Basic gTTS
```python
from tts.main import TTSEngine
import asyncio

async def test_gtts():
    tts = TTSEngine(engine="gtts")
    
    text = "Bonjou! Sa se yon tès an Kreyòl Ayisyen."
    
    audio_file = await tts.generate_audio(
        text=text,
        language="ht",
        speed=1.0,
        output_file="output.mp3"
    )
    
    print(f"✅ Audio saved: {audio_file}")

asyncio.run(test_gtts())
```

### Example 2: Edge TTS (HD Quality)
```python
from tts.main import TTSEngine
import asyncio

async def test_edge():
    tts = TTSEngine(engine="edge")
    
    text = "Bonjou! Sa se yon tès ak Edge TTS."
    
    audio_file = await tts.generate_audio(
        text=text,
        language="ht",
        voice="fr-FR-DeniseNeural",  # Female voice
        speed=1.2,  # 20% faster
        pitch=2,    # +2 semitones
        output_file="output.mp3"
    )
    
    print(f"✅ Audio saved: {audio_file}")

asyncio.run(test_edge())
```

### Example 3: Check Available Engines
```python
from tts.main import TTSEngine

available = TTSEngine.get_available_engines()
print(f"Available engines: {available}")
```

## 🎯 Supported Engines

| Engine | Price | Quality | Voices | Creole Support |
|--------|-------|---------|--------|----------------|
| **gTTS** | Free | Good | 50+ | ✅ (via French) |
| **Edge TTS** | Free | Excellent | 100+ | ✅ (via French) |
| **ElevenLabs** | Premium | Premium | Custom | ✅ (Voice Cloning) |
| **OpenAI TTS** | Premium | HD | 6 | ✅ (via French) |

## 🇭🇹 Haitian Creole Support

Haitian Creole is not directly supported by most TTS engines. We use **French voices** as a phonetic substitute, which provides good results.

### Recommended Voices:

**Edge TTS (Free & Best):**
- Female: `fr-FR-DeniseNeural`
- Male: `fr-FR-HenriNeural`

**gTTS (Free & Simple):**
- Language: `fr`

## 📊 API Reference

### TTSEngine

```python
class TTSEngine:
    def __init__(self, engine: str = "gtts", api_key: Optional[str] = None)
    
    async def generate_audio(
        text: str,
        language: str = "ht",
        voice: Optional[str] = None,
        output_file: Optional[str] = None,
        speed: float = 1.0,
        pitch: int = 0,
        format: str = "mp3"
    ) -> str
    
    @staticmethod
    def get_available_engines() -> Dict[str, str]
    
    @staticmethod
    def estimate_duration(text: str, speed: float = 1.0) -> float
    
    @staticmethod
    def format_duration(seconds: float) -> str
```

## 🧪 Testing

```bash
cd tts
python main.py
```

## 📝 Notes

- **Haitian Creole**: Uses French voices as phonetic substitute
- **Speed**: 0.5 = 50% slower, 1.0 = normal, 2.0 = 2x faster
- **Pitch**: -12 to +12 semitones (-12 = lower, +12 = higher)
- **Format**: mp3, wav, opus (depends on engine support)

## 🔑 Premium APIs

### ElevenLabs
```python
tts = TTSEngine(engine="elevenlabs", api_key="your_api_key")
```

### OpenAI TTS
```python
tts = TTSEngine(engine="openai", api_key="your_api_key")
```

## 🐛 Troubleshooting

### Edge TTS not working?
```bash
pip install --upgrade edge-tts
```

### gTTS not working?
```bash
pip install --upgrade gtts
```

### Audio files too large?
Use Opus format for better compression:
```python
audio_file = await tts.generate_audio(text=text, format="opus")
```

## 📄 License

Part of Faner Studio - Haitian Creole Content Creation Platform

---

🇭🇹 **Fèt ak ❤️ pou Kreyatè Kreyòl Ayisyen yo**

