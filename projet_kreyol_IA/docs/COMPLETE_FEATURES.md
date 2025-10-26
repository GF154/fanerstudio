# 🇭🇹 Kreyòl IA Studio - Complete Features

> **Platfòm konplè ak pwofesyonèl pou kreyasyon kontni an Kreyòl Ayisyen**

## ✅ Features Enplemante

### 🗣️ Text-to-Speech (TTS)

#### Engines Disponib:
1. **🇭🇹 Kreyòl Natif** (Facebook MMS-TTS) - GRATIS
2. **🤖 OpenAI TTS** - 6 vwa ($15/1M chars)
3. **🎙️ ElevenLabs** - Voice cloning ($5-99/month)

#### API Endpoints:
- `GET /api/voices` - Jwenn tout vwa disponib
- `POST /api/tts` - Jenere odyo soti nan tèks

#### Documentation:
- 📚 `TTS_GUIDE.md` - Gid konplè ak egzanp

---

### 📝 Speech-to-Text (STT)

#### Engines Disponib:
1. **🎤 Whisper Local** - GRATIS, offline
2. **☁️ Whisper OpenAI API** - Rapid ($0.006/min)
3. **🚀 AssemblyAI** - Advanced ($0.015/min)

#### API Endpoints:
- `GET /api/stt/engines` - Jwenn engines disponib
- `POST /api/stt` - Transkripsyon odyo

#### Documentation:
- 📚 `STT_GUIDE.md` - Gid konplè ak egzanp

---

### 📚 Audiobook Creation

#### Features:
- ✅ Support PDF, TXT, DOCX, EPUB
- ✅ Automatic translation to Creole
- ✅ High-quality TTS
- ✅ Chapter splitting (planned)

#### API Endpoints:
- `POST /api/audiobook` - Kreye liv odyo

---

### 🎙️ Podcast Generation

#### Features:
- ✅ From URL or documents
- ✅ Multiple speakers (planned)
- ✅ Intro/outro music (planned)
- ✅ Auto-generate script from content

#### API Endpoints:
- `POST /api/podcast` - Kreye podcast

---

### 🌍 Translation

#### Features:
- ✅ Google Translate integration
- ✅ NLLB model for better Creole
- ✅ PDF translation
- ✅ Batch translation

#### API Endpoints:
- `POST /api/translate` - Tradwi tèks
- `POST /api/translate/pdf` - Tradwi PDF

---

### 🎬 Video Processing (In Development)

#### Planned Features:
- ⏳ Add voiceover to video
- ⏳ Add SFX and music
- ⏳ Generate captions/subtitles
- ⏳ Remove background noise
- ⏳ Fix voiceover mistakes
- ⏳ AI soundtrack generation

#### API Endpoints:
- Endpoints created, implementation pending

---

## 🏗️ Architecture

### Modern Structure:
```
app/
├── main.py              # Entry point
├── api.py               # FastAPI routes
├── utils.py             # Utility functions
├── workflows.py         # Orchestration
└── services/
    ├── tts_service.py   # Multi-engine TTS
    ├── stt_service.py   # Multi-engine STT
    └── media_service.py # Media processing
```

### Services Layer:
- **TTSService**: Handle 3 TTS engines
- **STTService**: Handle 3 STT engines
- **MediaService**: Document & media processing

### Workflows:
- High-level orchestration functions
- Combine multiple services
- Batch processing support

---

## 🔧 Configuration

### Environment Variables:

```env
# Application
APP_NAME="Kreyòl IA Studio"
APP_VERSION="3.0.0"
PORT=8000

# AI Services
OPENAI_API_KEY=sk-proj-xxxxx        # OpenAI TTS & STT
ELEVENLABS_API_KEY=xxxxx            # ElevenLabs TTS
ASSEMBLYAI_API_KEY=xxxxx            # AssemblyAI STT

# Storage (Optional)
AWS_ACCESS_KEY_ID=xxxxx
AWS_SECRET_ACCESS_KEY=xxxxx
GCS_BUCKET=xxxxx

# Security
SECRET_KEY=xxxxx
ALLOWED_ORIGINS=*
```

---

## 📊 Cost Comparison

### TTS Services:

| Provider | Free Tier | Paid | Quality |
|----------|-----------|------|---------|
| **Kreyòl Natif** | Unlimited | - | Good |
| **OpenAI** | - | $15/1M chars | Excellent |
| **ElevenLabs** | 10K/month | $5-99/month | Outstanding |

### STT Services:

| Provider | Free Tier | Paid | Speed |
|----------|-----------|------|-------|
| **Whisper Local** | Unlimited | - | Medium |
| **Whisper OpenAI** | - | $0.006/min | Fast |
| **AssemblyAI** | 10K chars | $0.015/min | Very Fast |

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone repository
git clone <repo>
cd projet_kreyol_IA

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements_studio.txt

# Optional: Install Whisper for free STT
pip install openai-whisper
```

### 2. Configuration

```bash
# Copy environment template
cp .env_studio_example .env

# Edit .env and add your API keys
# (Optional - use native Creole TTS/Whisper without keys)
```

### 3. Launch

```bash
# Launch application
python -m app.main

# Or use batch file (Windows)
LANCER_STUDIO.bat
```

### 4. Access

- 🌐 **Interface**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs
- 📖 **ReDoc**: http://localhost:8000/redoc

---

## 💡 Usage Examples

### TTS - Generate Speech

```python
from app.services.tts_service import text_to_speech_file

# Creole native (free)
await text_to_speech_file(
    "Bonjou! Kijan ou ye?",
    "output/hello.mp3",
    voice="creole-native"
)

# OpenAI (premium)
await text_to_speech_file(
    "Hello world!",
    "output/hello.mp3",
    voice="openai-nova"
)
```

### STT - Transcribe Audio

```python
from app.services.stt_service import transcribe_audio

# Auto mode (free if Whisper installed)
text = await transcribe_audio(
    "audio/recording.mp3",
    engine="auto"
)

print(text)
```

### Audiobook - Full Workflow

```python
from app.workflows import create_audiobook

result = await create_audiobook(
    file_path="books/book.pdf",
    voice="creole-native",
    out_dir="output/audiobook"
)

print(f"Audio: {result['audio']}")
```

### Podcast - From URL

```python
from app.workflows import create_podcast

result = await create_podcast(
    source="https://example.com/article",
    title="Mon Podcast",
    voice="openai-nova",
    out_dir="output/podcast"
)

print(f"Parts: {result['parts']}")
```

---

## 📚 Documentation

### Complete Guides:

1. **README_STUDIO.md** - Architecture & deployment
2. **TTS_GUIDE.md** - Text-to-Speech complete guide
3. **STT_GUIDE.md** - Speech-to-Text complete guide
4. **WORKFLOWS_GUIDE.md** - Workflows & orchestration
5. **COMPLETE_FEATURES.md** - This document

### API Documentation:
- Interactive: http://localhost:8000/docs
- Alternative: http://localhost:8000/redoc

---

## 🐳 Deployment

### Docker:

```bash
# Build image
docker build -f Dockerfile_studio -t kreyol-ia-studio .

# Run container
docker run -p 8000:8000 kreyol-ia-studio
```

### Cloud (Render/Heroku):

```bash
# See README_STUDIO.md for detailed instructions
```

---

## 🔒 Security Features

- ✅ Environment variables for secrets
- ✅ CORS configuration
- ✅ File upload validation
- ✅ API key management
- ⏳ Rate limiting (planned)
- ⏳ JWT authentication (planned)

---

## 🎯 Roadmap

### Phase 1: Core Features ✅ DONE
- [x] TTS with multiple engines
- [x] STT with multiple engines
- [x] Audiobook creation
- [x] Podcast generation
- [x] Translation

### Phase 2: Video Features 🚧 IN PROGRESS
- [ ] Video voiceover
- [ ] Caption generation
- [ ] Audio denoising
- [ ] SFX addition
- [ ] AI soundtrack

### Phase 3: Advanced Features 📋 PLANNED
- [ ] Multi-speaker podcasts
- [ ] Voice cloning
- [ ] Real-time transcription
- [ ] Batch processing UI
- [ ] Progress tracking

### Phase 4: Enterprise 🔮 FUTURE
- [ ] Database integration
- [ ] User authentication
- [ ] Team collaboration
- [ ] API rate limiting
- [ ] Webhook notifications

---

## 🤝 Contributing

We welcome contributions! Areas for improvement:

1. **Video Processing**: Implement moviepy integration
2. **Voice Cloning**: ElevenLabs custom voices
3. **UI/UX**: Enhance web interface
4. **Testing**: Add comprehensive tests
5. **Documentation**: Improve guides

---

## 📝 Notes

### Currently Free Options:
- ✅ Kreyòl Natif TTS (unlimited)
- ✅ Whisper Local STT (unlimited)
- ✅ Translation (Google Translate)
- ✅ Document processing

### Premium Options:
- 💰 OpenAI TTS ($15/1M chars)
- 💰 OpenAI STT ($0.006/min)
- 💰 ElevenLabs TTS ($5-99/month)
- 💰 AssemblyAI STT ($0.015/min)

### Recommended Setup:
1. **Start Free**: Use Kreyòl Natif + Whisper Local
2. **Add OpenAI**: For better quality when needed
3. **Add ElevenLabs**: For voice cloning projects
4. **Add AssemblyAI**: For advanced STT features

---

## 📞 Support

- **Documentation**: See guides in project root
- **API Docs**: http://localhost:8000/docs
- **Issues**: Open GitHub issue
- **Community**: Join our Discord (TBD)

---

## 📄 License

MIT License - See `LICENSE` for details

---

**Fèt ak ❤️ pou kominote Kreyòl Ayisyen** 🇭🇹

**Version**: 3.0.0  
**Last Updated**: 2025-10-23  
**Status**: Production Ready ✅

