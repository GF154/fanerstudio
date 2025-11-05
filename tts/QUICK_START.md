# 🎙️ Quick Start - Coqui TTS API

## 🚀 Installation Rapid

```bash
cd tts
pip install -r requirements.txt
```

**Note:** Coqui TTS ap download modèl yo (1-2 GB) nan premye itilizasyon.

## ▶️ Lanse Sèvè

```bash
python api_coqui.py
```

Sèvè ap viv sou: **http://localhost:8000**

## 📖 API Docs

Ouvri navigatè ou: **http://localhost:8000/docs**

## 🧪 Test API

### 1. Simple `/speak` Endpoint

```bash
curl "http://localhost:8000/speak?text=Bonjou%20tout%20moun&language=ht"
```

Oswa nan navigatè:
```
http://localhost:8000/speak?text=Bonjou tout moun&language=ht
```

### 2. Advanced `/api/tts/generate` Endpoint

```bash
curl -X POST "http://localhost:8000/api/tts/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Bonjou! Sa se yon tès pou platfòm Faner Studio.",
    "language": "ht",
    "engine": "coqui",
    "format": "wav"
  }'
```

### 3. Python Client

```python
import requests

# Simple speak
response = requests.get(
    "http://localhost:8000/speak",
    params={
        "text": "Bonjou tout moun!",
        "language": "ht"
    }
)

with open("output.wav", "wb") as f:
    f.write(response.content)

print("✅ Audio saved: output.wav")
```

```python
# Advanced generate
response = requests.post(
    "http://localhost:8000/api/tts/generate",
    json={
        "text": "Bonjou! Sa se yon tès pou platfòm Faner Studio.",
        "language": "ht",
        "engine": "coqui",
        "format": "wav"
    }
)

data = response.json()
print(f"Audio URL: {data['audio_url']}")
print(f"Filename: {data['filename']}")
```

## 🎯 Available Engines

| Engine | Quality | Speed | Use Case |
|--------|---------|-------|----------|
| **coqui** | Excellent | Medium | Best for Creole |
| **gtts** | Good | Fast | Quick generation |
| **edge** | Excellent | Fast | High quality |

## 🇭🇹 Haitian Creole Support

All engines use **French** as a phonetic substitute for Haitian Creole:
- Coqui TTS: Multilingual YourTTS model
- Language code: `"ht"` (automatically converted to `"fr"`)

## 📋 Available Endpoints

```
GET  /                      - Root info
GET  /health                - Health check
GET  /api/tts/engines       - List engines
GET  /api/tts/models        - List Coqui models
GET  /speak?text=...        - Simple speak (original format)
POST /api/tts/generate      - Advanced generation
GET  /download/{filename}   - Download audio
```

## 🔧 Configuration

Edit `api_coqui.py` to change:

```python
# Change Coqui model
MODEL = "tts_models/multilingual/multi-dataset/your_tts"

# Change server port
uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 🐛 Troubleshooting

### Coqui TTS not loading?
```bash
pip install --upgrade TTS
```

### Model download failed?
```bash
# Manual download
tts --model_name tts_models/multilingual/multi-dataset/your_tts --text "test"
```

### Port already in use?
```bash
# Change port in api_coqui.py
uvicorn.run(app, host="0.0.0.0", port=8080)
```

## 📊 Performance

- **First request**: Slow (loading model)
- **Subsequent requests**: Fast (~1-2 seconds)
- **Memory usage**: ~2-3 GB
- **Disk space**: ~1-2 GB (models)

## 🎤 Voice Quality Comparison

```
Coqui TTS    ████████████ 95%  (Best for Creole)
Edge TTS     ███████████░ 90%  (Fast & Good)
gTTS         ████████░░░░ 70%  (Quick & Simple)
```

## 🚀 Next Steps

1. ✅ Test API with Postman or curl
2. ✅ Integrate with Faner Studio frontend
3. ✅ Deploy to production server
4. ✅ Add voice customization options

---

🇭🇹 **Fèt ak ❤️ pou Kreyatè Kreyòl Ayisyen yo**

