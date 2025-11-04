# 🇭🇹 Faner Studio - Complete Platform

**Platfòm #1 pou kreyasyon kontni pwofesyonèl an Kreyòl Ayisyen**

[![Version](https://img.shields.io/badge/version-3.2.0-blue.svg)](https://github.com/GF154/fanerstudio)
[![Python](https://img.shields.io/badge/python-3.9%2B-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)

---

## 🎯 Features / Karakteristik

### ✅ **FULLY FUNCTIONAL** - Tout Fonksyonèl!

| Tool | Status | Description |
|------|--------|-------------|
| 🌍 **Translation** | ✅ Active | NLLB-200 translation (200+ languages including Haitian Creole) |
| 🎤 **Text-to-Speech** | ✅ Active | gTTS integration with Haitian Creole support |
| 📚 **Audiobook** | ✅ Active | PDF/TXT/DOCX/EPUB to audio conversion |
| 🎙️ **Podcast (Basic)** | ✅ Active | Simple podcast generation from scripts |
| 🎙️ **Podcast (Advanced)** | ✅ Active | Multi-speaker, emotions, background music, SFX |
| 🎵 **Custom Voice** | ✅ Active | Voice cloning with 3 methods (basic/medium/premium) |
| 🔐 **Authentication** | ✅ Active | JWT-based auth with SQLite/PostgreSQL |
| 📊 **Admin Dashboard** | ✅ Active | User management, analytics, monitoring |
| ⚡ **Performance** | ✅ Active | Caching, rate limiting, monitoring |

---

## 🚀 Quick Start

### 1. **Clone Repository**
```bash
git clone https://github.com/GF154/fanerstudio.git
cd fanerstudio
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Validate Environment**
```bash
python environment_validator.py
```

### 4. **Run Locally**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. **Access Platform**
- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📦 What's New in v3.2.0

### 🎉 **Major Improvements**

1. **✅ Real TTS Integration**
   - `generer_audio_huggingface.py` with gTTS/Coqui/pyttsx3 support
   - Automatic fallback between engines
   - Haitian Creole optimized

2. **✅ Advanced Voice Cloning**
   - 3 methods: Basic (free), Medium (RVC), Premium (ElevenLabs)
   - Voice analysis with librosa + parselmouth
   - Pitch, speed, volume, EQ control

3. **✅ Complete Podcast Fabric**
   - Real TTS integration
   - Background music library (auto-generated)
   - Sound effects library
   - Audio mixing with pydub
   - Multi-speaker support with emotions

4. **✅ Music & SFX Library**
   - Auto-generated royalty-free music
   - Professional sound effects
   - Podcast jingles (intro/outro)
   - Audio mixer with volume control

5. **✅ Environment Validation**
   - Comprehensive environment checks
   - Deployment readiness validation
   - Detailed error reporting

6. **✅ Vercel Deployment**
   - Complete `vercel.json` configuration
   - Environment variable management
   - Deployment guide
   - `.vercelignore` for optimization

7. **✅ Testing Suite**
   - Comprehensive unit tests
   - Integration tests
   - Environment tests
   - TTS tests

---

## 🏗️ Architecture

```
faner-studio/
├── main.py                          # FastAPI application
├── generer_audio_huggingface.py     # TTS engine (gTTS/Coqui/pyttsx3)
├── podcast_fabric.py                # Advanced podcast generator
├── audio_library.py                 # Music & SFX library
├── environment_validator.py         # Environment validation
├── database.py                      # SQLAlchemy models & CRUD
├── auth.py                          # JWT authentication
├── performance.py                   # Caching & monitoring
│
├── projet_kreyol_IA/
│   ├── app_studio_dark.html         # Main frontend
│   ├── src/
│   │   ├── advanced_voice_cloning.py  # Voice cloning system
│   │   └── custom_voice_manager.py    # Voice storage
│   └── app/services/
│       ├── tts_service.py           # TTS service
│       └── media_service.py         # Media processing
│
├── api/
│   └── index.py                     # Vercel entry point
│
├── requirements.txt                 # Python dependencies
├── vercel.json                      # Vercel configuration
├── .vercelignore                    # Vercel ignore rules
│
├── test_complete_platform.py        # Test suite
├── RUN_COMPLETE_TESTS.bat          # Test runner
│
└── docs/
    ├── VERCEL_DEPLOYMENT_GUIDE.md
    └── ...
```

---

## 🔧 Configuration

### **Required Environment Variables**

```bash
# Database (Optional - defaults to SQLite)
DATABASE_URL=sqlite:///./data/fanerstudio.db

# Security (Required for production)
SECRET_KEY=your-secret-key-here-make-it-long-and-random
```

### **Optional API Keys** (for enhanced features)

```bash
# Hugging Face API (for better translation)
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxx

# OpenAI API (for premium TTS)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx

# ElevenLabs API (for premium voice cloning)
ELEVENLABS_API_KEY=xxxxxxxxxxxxxxxxxxxxx

# Supabase (for cloud database)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 🌐 Deployment

### **Deploy to Vercel** (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

See [VERCEL_DEPLOYMENT_GUIDE.md](VERCEL_DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## 🧪 Testing

### **Run All Tests**
```bash
python test_complete_platform.py
```

### **Or use batch file** (Windows)
```bash
RUN_COMPLETE_TESTS.bat
```

### **Test Categories**
- ✅ Environment validation
- ✅ TTS integration
- ✅ Voice cloning
- ✅ Podcast generation
- ✅ Audio library
- ✅ Database integration
- ✅ Authentication
- ✅ Performance monitoring

---

## 📊 API Endpoints

### **Core Endpoints**
```
GET  /                    # Main frontend
GET  /health              # Health check with detailed status
GET  /api/info            # API information
GET  /api/status          # System status
GET  /docs                # Interactive API documentation
```

### **Translation**
```
POST /api/translate       # Translate text (NLLB-200)
```

### **Audio Tools**
```
POST /api/audiobook       # Create audiobook from document
POST /api/podcast         # Create simple podcast
POST /api/podcast/advanced # Create advanced podcast (Veed Fabric style)
GET  /api/podcast/templates # Get podcast templates
```

### **Voice Management**
```
POST /api/voice/create    # Create custom voice
GET  /api/voices          # List all available voices
```

### **Authentication**
```
POST /api/auth/register   # Register new user
POST /api/auth/login      # Login (get JWT token)
GET  /api/auth/me         # Get current user info
GET  /api/auth/projects   # Get user's projects
GET  /api/auth/voices     # Get user's custom voices
```

### **Admin** (requires admin role)
```
GET    /api/admin/stats   # Get statistics
GET    /api/admin/users   # List all users
GET    /api/admin/projects # List all projects
GET    /api/admin/voices  # List all voices
PUT    /api/admin/user/{id} # Update user
DELETE /api/admin/user/{id} # Delete user
```

---

## 🛠️ Development

### **Tech Stack**
- **Backend**: FastAPI 0.109.0 + Python 3.9+
- **Database**: SQLAlchemy + SQLite/PostgreSQL
- **Auth**: JWT + bcrypt
- **TTS**: gTTS / Coqui TTS / pyttsx3
- **Audio**: pydub + soundfile + scipy
- **Translation**: NLLB-200 via Hugging Face API
- **Deployment**: Vercel / Render

### **Key Libraries**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `bcrypt` - Password hashing
- `pydub` - Audio processing
- `gtts` - Text-to-speech
- `httpx` - HTTP client
- `pytest` - Testing

---

## 📚 Documentation

- [Vercel Deployment Guide](VERCEL_DEPLOYMENT_GUIDE.md)
- [Environment Validation](environment_validator.py)
- [Testing Guide](test_complete_platform.py)
- [API Documentation](http://localhost:8000/docs) (when running)

---

## 🔍 Troubleshooting

### **Issue: TTS not working**
```bash
# Check TTS engines
python -c "from generer_audio_huggingface import check_tts_available; print(check_tts_available())"

# Install gTTS if missing
pip install gtts
```

### **Issue: Audio processing errors**
```bash
# Install ffmpeg (required for pydub)
# Windows: Download from https://ffmpeg.org/
# Linux: sudo apt install ffmpeg
# Mac: brew install ffmpeg
```

### **Issue: Database errors**
```bash
# Recreate database
rm data/fanerstudio.db
python -c "from database import init_db; init_db()"
```

### **Issue: Environment validation fails**
```bash
# Run validator to see specific issues
python environment_validator.py
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 👨‍💻 Author

**Faner Studio Team**
- GitHub: [@GF154](https://github.com/GF154)
- Email: fanerstudio@gmail.com

---

## 🙏 Acknowledgments

- **Hugging Face** - NLLB-200 translation model
- **gTTS** - Google Text-to-Speech
- **Coqui TTS** - Open source TTS
- **FastAPI** - Modern web framework
- **Vercel** - Deployment platform

---

## 📈 Status

- **Version**: 3.2.0
- **Status**: ✅ Production Ready
- **Last Updated**: November 4, 2024
- **Platform**: Vercel + Render
- **Database**: SQLite + Supabase

---

**🎉 Ready to create amazing Haitian Creole content!**

Visit: https://fanerstudio.vercel.app (after deployment)

