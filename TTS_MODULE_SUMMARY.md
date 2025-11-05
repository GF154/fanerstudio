# 🎙️ Faner Studio - TTS Module

## 📁 Structure Created

```
project/
 └─ tts/
     ├─ main.py          # Advanced TTS Engine
     ├─ requirements.txt # Dependencies
     └─ README.md        # Documentation
```

## ✅ What's Included

### 1. **main.py** - Advanced TTS Engine
- Multi-engine support (gTTS, Edge TTS, ElevenLabs, OpenAI)
- Haitian Creole support (via French voices)
- Voice control (speed, pitch, emotion)
- Async/await for better performance
- Estimated duration calculation
- Multiple audio formats (mp3, wav, opus)

### 2. **requirements.txt** - Dependencies
- `gtts==2.5.1` - Google TTS (Free)
- `edge-tts==6.1.9` - Microsoft Edge TTS (Free, HD)
- Optional: ElevenLabs, OpenAI for premium features

### 3. **README.md** - Complete Documentation
- Installation instructions
- Usage examples
- API reference
- Haitian Creole support guide
- Troubleshooting tips

## 🚀 Quick Start

### Install
```bash
cd tts
pip install -r requirements.txt
```

### Test
```bash
python main.py
```

### Use in Your Code
```python
from tts.main import TTSEngine
import asyncio

async def generate_speech():
    tts = TTSEngine(engine="gtts")
    
    audio = await tts.generate_audio(
        text="Bonjou! Sa se yon tès an Kreyòl Ayisyen.",
        language="ht",
        speed=1.0,
        output_file="output.mp3"
    )
    
    print(f"Audio: {audio}")

asyncio.run(generate_speech())
```

## 🎯 Supported Engines

| Engine | Price | Quality | Voices |
|--------|-------|---------|--------|
| gTTS | Free | Good | 50+ |
| Edge TTS | Free | Excellent | 100+ |
| ElevenLabs | Premium | Premium | Custom |
| OpenAI TTS | Premium | HD | 6 |

## 🇭🇹 Haitian Creole

Best voices for Haitian Creole:
- **Edge TTS**: `fr-FR-DeniseNeural` (female)
- **Edge TTS**: `fr-FR-HenriNeural` (male)
- **gTTS**: `lang='fr'`

## ✅ Test Results

```
🎙️ Faner Studio - TTS Engine Test
✅ Available engines: 1
  - gtts: Google Text-to-Speech (Free, 50+ languages)
  
🧪 Testing gTTS...
✅ Audio generated: tmp7eh2s3vm.mp3
📊 Estimated duration: 00:05

✅ Test complete!
```

## 🔗 Integration

You can now integrate this TTS engine into:
- **Audiobook generation** (`api/index.py`)
- **Podcast creation** (`podcast_generator.py`)
- **Custom voice testing** (`custom_voice_cloner.py`)
- **Video voiceovers** (`video_processor_simple.py`)

## 📝 Next Steps

1. ✅ Install Edge TTS for better quality:
   ```bash
   pip install edge-tts
   ```

2. ✅ Update existing modules to use this TTS engine

3. ✅ Add voice customization UI

4. ✅ Integrate with Vercel deployment

---

🇭🇹 **Fèt ak ❤️ pou Kreyatè Kreyòl Ayisyen yo**

