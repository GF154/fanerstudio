# 🇭🇹 Kreyòl IA Studio - Architecture Pwofesyonèl

> **Platfòm Pwofesyonèl pou Kreyasyon Kontni an Kreyòl Ayisyen**

## 📁 Estrikti Pwojè

```
studio-ai/
├─ app/
│  ├─ __init__.py
│  ├─ main.py              # 🚀 Pwen antre prensipal
│  ├─ api.py               # 🌐 Routes FastAPI
│  ├─ utils.py             # 🛠️ Fonksyon itil
│  ├─ services/
│  │   ├─ __init__.py
│  │   ├─ tts_service.py   # 🗣️ Text-to-Speech
│  │   ├─ stt_service.py   # 📝 Speech-to-Text
│  │   └─ media_service.py # 🎬 Media processing
├─ requirements_studio.txt  # 📦 Dependencies
├─ Dockerfile_studio        # 🐳 Docker config
├─ Procfile_studio          # ☁️ Render/Heroku config
├─ .env.example_studio      # 🔐 Environment variables
└─ README_STUDIO.md         # 📖 Documentation

```

## 🚀 Quick Start

### 1️⃣ Enstale Dependencies

```bash
# Kreye virtual environment
python -m venv venv

# Aktive virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Enstale dependencies
pip install -r requirements_studio.txt
```

### 2️⃣ Konfigire Environment

```bash
# Kòpye .env.example epi modifye l
copy .env.example_studio .env
```

### 3️⃣ Lance Aplikasyon

```bash
# Lance ak Python
python -m app.main

# Oswa ak Uvicorn
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

### 4️⃣ Aksede Aplikasyon

- **Interface Web**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Endpoints

### 🗣️ Text-to-Speech
```bash
POST /api/tts
Content-Type: multipart/form-data

text: "Bonjou, kijan ou ye?"
voice: "creole-native"
```

### 📚 Audiobook
```bash
POST /api/audiobook
Content-Type: multipart/form-data

file: document.pdf
voice: "creole-native"
```

### 🎙️ Podcast
```bash
POST /api/podcast
Content-Type: multipart/form-data

title: "Podcast Kreyòl"
content: "Kontni pou diskite..."
num_speakers: 2
```

### 🌍 Translation
```bash
POST /api/translate
Content-Type: multipart/form-data

text: "Hello, how are you?"
target_lang: "ht"
```

### 📄 PDF Translation
```bash
POST /api/translate/pdf
Content-Type: multipart/form-data

file: document.pdf
target_lang: "ht"
```

### 📝 Speech-to-Text
```bash
POST /api/stt
Content-Type: multipart/form-data

file: audio.mp3
```

## 🐳 Docker Deployment

### Build Image
```bash
docker build -f Dockerfile_studio -t kreyol-ia-studio .
```

### Run Container
```bash
docker run -p 8000:8000 kreyol-ia-studio
```

### Docker Compose
```yaml
version: '3.8'

services:
  kreyol-ia:
    build:
      context: .
      dockerfile: Dockerfile_studio
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=your-secret-key
    volumes:
      - ./output:/app/output
```

## ☁️ Cloud Deployment

### Render
1. Push kod ou sou GitHub
2. Kreye nouvo Web Service sou Render
3. Konekte repo GitHub ou
4. Set build command: `pip install -r requirements_studio.txt`
5. Set start command: `python -m app.main`
6. Deploy!

### Heroku
```bash
# Login
heroku login

# Create app
heroku create kreyol-ia-studio

# Add buildpack
heroku buildpacks:add --index 1 https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git

# Deploy
git push heroku main
```

## 🏗️ Architecture

### Services Layer
```
app/services/
├─ tts_service.py    # Konvèti tèks an paròl
├─ stt_service.py    # Konvèti paròl an tèks
└─ media_service.py  # Pwosese audiobook, podcast, PDF
```

### API Layer
```
app/api.py           # FastAPI routes ak endpoints
```

### Main Application
```
app/main.py          # Pwen antre, lance servè
```

### Utilities
```
app/utils.py         # Fonksyon itil (file handling, validation)
```

## 🔒 Security

- ✅ Environment variables pou secrets
- ✅ CORS configuration
- ✅ File upload validation
- ✅ Rate limiting (TODO)
- ✅ JWT authentication (TODO)

## 📊 Monitoring

- ✅ Health check endpoint: `/health`
- ✅ Prometheus metrics (TODO)
- ✅ Logging

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## 📝 TODO

- [ ] Implement rate limiting
- [ ] Add JWT authentication
- [ ] Implement real STT with Whisper
- [ ] Add Redis caching
- [ ] Implement multi-speaker podcast
- [ ] Add video processing
- [ ] Database integration (PostgreSQL)
- [ ] WebSocket support for real-time updates
- [ ] Add background tasks (Celery/Redis)

## 🤝 Contributing

Kontribye nan pwojè sa a! Gade `CONTRIBUTING.md` pou plis enfòmasyon.

## 📄 License

MIT License - Gade `LICENSE` pou plis detay.

## 👥 Team

Kreyòl IA Development Team

---

**Fèt ak ❤️ pou kominote Kreyòl Ayisyen** 🇭🇹

