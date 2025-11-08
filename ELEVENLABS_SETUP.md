# 🎙️ ELEVENLABS VOICE CLONING - GID KONFIGIRASYON

## 🎯 SA W BEZWEN FÈ:

### 1️⃣ **Ajoute ElevenLabs API Key nan `.env`**

```bash
# Ouvri fichye .env ou kreye l si li pa egziste
# Kopi fichye env.example → .env

# Ajoute ElevenLabs API key ou:
ELEVENLABS_API_KEY=sk_81ec6a037bdfdfb4317dfa41d14083eb68b8939b308a15e2
```

⚠️ **ENPÒTAN:** Pa JANM commit fichye `.env` nan Git! Li deja nan `.gitignore`.

---

### 2️⃣ **Ajoute API Key nan Vercel**

Pou deployment Vercel:

1. Ale nan: https://vercel.com/dashboard
2. Chwazi pwojè ou
3. **Settings** → **Environment Variables**
4. Ajoute:
   - **Key:** `ELEVENLABS_API_KEY`
   - **Value:** `sk_81ec6a037bdfdfb4317dfa41d14083eb68b8939b308a15e2`
   - **Environment:** Production, Preview, Development (chwazi tout)
5. Klike **Save**
6. **Redeploy** aplikasyon an

---

## ✨ SA K AP FONKSYONE KOUNYE A:

### 🎯 **REAL Voice Cloning:**
- Upload 1 echantiyon vwa (1-3 minit)
- ElevenLabs ap klone vwa a **reyèlman**
- Jenere nouvo odyo ak vwa klone a
- Kalite siperyè, son natirèl

### 🔄 **Fallback Otomatik:**
- Si ElevenLabs pa disponib → itilize gTTS
- Si w pa gen API key → itilize gTTS
- Si limit depase → itilize gTTS

---

## 📊 LIMIT ELEVENLABS:

### **Free Tier:** (Ou gen sa a)
- ✅ 10,000 characters/mwa
- ✅ 3 vwa kistòm
- ✅ Tout modèl disponib
- ✅ 29 lang sipòte

### **Creator Plan:** ($11/mwa)
- ✅ 100,000 characters/mwa
- ✅ Vwa kistòm ilimite
- ✅ Voice Library akse
- ✅ Commercial use

### **Pro Plan:** ($99/mwa)
- ✅ 500,000 characters/mwa
- ✅ Tout fonksyonalite Creator
- ✅ API akse pou volume
- ✅ Priyorite

---

## 🧪 KÒMAN TESTE:

1. **Deployment la ap fèt otomatikman** apre push
2. Ale nan: `/custom-voice.html`
3. Kreye yon vwa:
   - Upload 1 fichye odyo
   - Bay yon non
   - Klike "🎯 Kreye Vwa Natirèl"
4. Mesaj la ap di: **"🎯 REAL voice cloning ak ElevenLabs!"**
5. Teste vwa a nan tab "🧪 Test Vwa"

---

## 📝 DIFERANS: gTTS vs ElevenLabs

| Karakteristik | gTTS (FREE) | ElevenLabs (PREMIUM) |
|--------------|-------------|---------------------|
| **Voice Cloning** | ❌ Non | ✅ Wi (REYÈL) |
| **Kalite Son** | 🥉 Pi Ba | 🥇 Ekselan |
| **Lang Sipòte** | 50+ | 29 (men pi bon) |
| **Natirèl** | Robotik | 🎯 Trè Natirèl |
| **Pitch Control** | ❌ Non | ✅ Wi |
| **Speed Control** | Limite | ✅ Avanse |
| **Emosyon** | ❌ Non | ✅ Wi |
| **Limit** | Ilimite | 10K chars/mwa (Free) |
| **Pri** | 100% FREE | FREE oswa $11+/mwa |

---

## 🔧 TROUBLESHOOTING:

### ❌ **"Voice cloner not available"**
→ Enstale library: `pip install elevenlabs`

### ❌ **"⚠️ ElevenLabs init failed"**
→ Verifye API key la kòrèk nan `.env`

### ❌ **"Using gTTS fallback"**
→ API key pa trouve oswa ElevenLabs limit depase

### ❌ **"Character limit exceeded"**
→ Ou depase 10K chars/mwa (Free tier)
→ Upgrade nan Creator plan oswa tann mwa pwochèn

---

## 💡 TIPS POU PI BON REZILTA:

### 📤 **Upload Echantiyon:**
- ✅ 1-3 minit odyo (minimum 30 segonn)
- ✅ Klè, san bri
- ✅ Menm moun ap pale
- ✅ Ekspresif (pa monoton)
- ✅ MP3, WAV, M4A, oswa OGG

### 🎙️ **Pou Vwa Kreyòl:**
- ✅ Pale klè an Kreyòl
- ✅ Varyasyon tonalite
- ✅ Ekspresyon natirèl
- ✅ Pa twò rapid, pa twò ralanti

---

## 🚀 PROCHÈN ETAP:

1. ✅ **API key ajoute** - Ou fin fè sa!
2. ✅ **ElevenLabs entegre** - Kòd la prè!
3. ⏳ **Deploy nan Vercel** - M ap fè sa kounye a
4. 🎯 **Teste voice cloning** - Ou pral teste apre deployment

---

## 📞 SIPÒ:

- **ElevenLabs Docs:** https://docs.elevenlabs.io/
- **API Reference:** https://elevenlabs.io/docs/api-reference
- **Discord Community:** https://discord.gg/elevenlabs

---

**Ou prè pou REAL voice cloning! 🎙️✨**

