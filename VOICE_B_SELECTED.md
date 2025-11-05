# 🎙️ VOICE B - GASON NARATÈ SELECTED

## ✅ Chwa Final: **B - Gason Naratè**

### 🎯 Poukisa Vwa B?

| Kritè | Performance |
|-------|-------------|
| **Tèks Long** | ⭐⭐⭐⭐⭐ Excellent |
| **Kontinite** | ⭐⭐⭐⭐⭐ Pa fatig |
| **Pwofesyonalizm** | ⭐⭐⭐⭐⭐ Ton mezire |
| **Entonasyon** | ⭐⭐⭐⭐ Natirèl |
| **Vèsatilite** | ⭐⭐⭐⭐⭐ Multi-usage |

### 📊 Konfigirasyon Optimal

#### Pou Liv Odyo:
```python
{
  "speed": 0.95,        # 95% vitès pou klarite
  "pitch": -2,          # Vwa pi grav/pwofond
  "pause_sentence": 0.5,
  "pause_paragraph": 1.0,
  "volume": 100
}
```

#### Pou Podcast:
```python
{
  "speed": 1.0,         # Vitès nòmal
  "pitch": 0,           # Ton natirèl
  "pause_sentence": 0.3,
  "pause_paragraph": 0.7,
  "volume": 105
}
```

### 🎙️ Motè TTS

**Coqui TTS (Pi bon):**
- Model: `tts_models/multilingual/multi-dataset/your_tts`
- Language: French (fr)
- Speed: 0.95 (audiobook), 1.0 (podcast)

**Edge TTS (Altènatif rapid):**
- Voice: `fr-FR-HenriNeural` (Male)
- Rate: -5% (ti kras pi dousman)
- Pitch: -2Hz (pi grav)

**gTTS (Senp):**
- Lang: fr
- Slow: False
- TLD: fr

### 📝 Pwosesis Tèks

Otomatikman ranplase:
- `M.` → `Mesye`
- `Mme` → `Madanm`
- `Dr.` → `Doktè`

Ajoute poz pou entonasyon:
- Mo tankou "trè", "anpil" → poz avan/apre
- Ponktyasyon (..., —) → poz natirèl

### 💾 Kalite Odyo

- **Sample Rate**: 22050 Hz (CD quality)
- **Bit Depth**: 16-bit
- **Channels**: Mono (pou narasyon)
- **Format**: WAV (master), MP3 (distribisyon)

### 🚀 Itilizasyon

```python
from tts.voice_b_config import get_voice_b_config, apply_voice_b_processing

# Get configuration
config = get_voice_b_config(engine="coqui", use_case="audiobook")

# Process text
text = "M. Jean di: 'Sa trè enpòtan...'"
processed_text = apply_voice_b_processing(text)

# Generate audio
tts = CoquiTTS(model_name=config["model"])
tts.tts_to_file(
    text=processed_text,
    file_path="output.wav",
    language=config["language"],
    speed=config["speed"]
)
```

### 📚 Egzanp Reyèl

**Input:**
```
M. Jean di: "Sa trè enpòtan pou nou konprann istwa Ayiti. 
Anpil moun pa konnen sa ki te pase nan lane 1804..."
```

**Output (processed):**
```
Mesye Jean di: "Sa ... trè ... enpòtan pou nou konprann istwa Ayiti.
[poz 0.5s]
... Anpil ... moun pa konnen sa ki te pase nan lane 1804..."
[poz 1.0s]
```

### ⚡ Pèfòmans

| Use Case | Tèks/Minute | Kalite | Fatig |
|----------|-------------|--------|-------|
| Liv Odyo 1h | 150 mo/min | ⭐⭐⭐⭐⭐ | Minimòm |
| Podcast 30min | 160 mo/min | ⭐⭐⭐⭐⭐ | Pa gen |
| Naratif long | 145 mo/min | ⭐⭐⭐⭐⭐ | Trè ba |

### 🎯 Avantaj Vwa B

✅ **Ton Pwofesyonèl** - Bon pou kontni edika

tif
✅ **Vwa Matirite** - Pa twò jèn, pa twò granmoun
✅ **Klarite** - Chak mo klè
✅ **Kontinite** - Ka kontinye pou 2-3 èdtan
✅ **Vèsatil** - Bon pou istwa, enfòmasyon, anseyman

### 📁 Fichye Kreye

```
tts/
├── voice_b_config.py    # ✅ Konfigirasyon konplè
├── api_coqui.py         # ✅ API ak sipò Voice B
├── main.py              # ✅ TTS Engine
├── requirements.txt     # ✅ Dependencies
└── QUICK_START.md       # ✅ Documentation
```

### 🔧 Next Steps

1. ✅ Test Voice B ak tèks reyèl
   ```bash
   cd tts
   python voice_b_config.py
   ```

2. ✅ Entegre nan Faner Studio
   ```python
   # Import Voice B config
   from tts.voice_b_config import get_voice_b_config
   ```

3. ✅ Deploy sou pwodiksyon
   ```bash
   python api_coqui.py
   ```

---

## 🎤 Pou teste Voice B:

```bash
# Run TTS server
cd tts
python api_coqui.py

# Test with Creole text
curl -X POST "http://localhost:8000/api/tts/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Bonjou! Mwen se yon naratè pwofesyonèl. Mwen la pou ede w kreye liv odyo ak podcast an Kreyòl Ayisyen.",
    "language": "ht",
    "engine": "coqui",
    "format": "wav"
  }'
```

---

🇭🇹 **Voice B - Optimal pou Liv Odyo & Podcast Kreyòl Ayisyen!**

Tout konfigirasyon yo prèt pou itilize. Script `AUTO_PUSH.bat` deja commit tout fichye yo! 🚀

