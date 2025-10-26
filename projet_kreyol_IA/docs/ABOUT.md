# 📚 Sou Pwojè sa a / About This Project

## 🎯 Objektif / Objective

**Kreyòl:** Kreye yon zouti gratis ak open-source ki pèmèt moun tradui nenpòt dokiman PDF an Kreyòl Ayisyen epi konvèti li an liv odyo, pou fasilite aksè nan enfòmasyon ak edikasyon.

**English:** Create a free and open-source tool that allows people to translate any PDF document into Haitian Creole and convert it into an audiobook, to facilitate access to information and education.

---

## 🧠 Teknoloji Itilize / Technologies Used

### 1. **pypdf** - Ekstraksyon PDF
- Bibliyotèk modèn pou li fichye PDF
- Modern library for reading PDF files
- Pi rapid ak pi efikas pase lòt opsyon

### 2. **transformers + M2M100** - Tradiksyon AI
- **Modèl:** facebook/m2m100_418M
- Antrennen sou plis pase 100 lang, enkli Kreyòl Ayisyen
- Trained on 100+ languages, including Haitian Creole
- Pi bon kalite tradiksyon pou Kreyòl ke Google Translate
- Better translation quality for Creole than Google Translate

### 3. **PyTorch** - Backend ML
- Platfòm machin aprann ki sipòte transformers
- Machine learning platform that supports transformers
- Fonksyone sou CPU (pa bezwen GPU)
- Works on CPU (no GPU needed)

### 4. **gTTS** - Text-to-Speech
- Google Text-to-Speech pou Kreyòl Ayisyen
- Kalite odyo bon, gratis, san limit
- Good audio quality, free, unlimited

### 5. **langdetect** - Deteksyon Lang
- Detekte otomatikman lang PDF la
- Automatically detects PDF language
- Sipòte 55+ lang

### 6. **tqdm** - Ba Pwogrè
- Montre pwogrè pou chak etap
- Shows progress for each step
- Amelyore eksperyans itilizatè

---

## 📊 Fòs ak Limit / Strengths & Limitations

### ✅ Fòs / Strengths

1. **100% Gratis ak Open Source**
   - Pa gen frè, pa gen limit itilizasyon
   - No fees, no usage limits

2. **Tradiksyon Kalite Wo**
   - Itilize modèl AI estat-de-la a pou Kreyòl
   - Uses state-of-the-art AI model for Creole

3. **Fonksyone San Entènèt** (apre premye enstàlasyon)
   - Tout sa w bezwen telechaje yon fwa
   - Everything downloads once

4. **Deteksyon Lang Otomatik**
   - Pa bezwen espesifye lang sous la
   - No need to specify source language

5. **Liv Odyo Otomatik**
   - Kreye MP3 dirèkteman
   - Creates MP3 directly

### ⚠️ Limit / Limitations

1. **Espas Disk**
   - Modèl AI bezwen ~1.5GB espas
   - AI model requires ~1.5GB space

2. **RAM Nesesè**
   - Bezwen omwen 4GB RAM (8GB rekòmande)
   - Requires at least 4GB RAM (8GB recommended)

3. **Tan Pwosesis**
   - Pran plizyè minit pou gwo dokiman
   - Takes several minutes for large documents

4. **PDF Imaj**
   - Pa fonksyone ak PDF eskane san OCR
   - Doesn't work with scanned PDFs without OCR

5. **Kalite Tradiksyon**
   - Malgre modèl AI bon, tradiksyon pa toujou pafè
   - Despite good AI model, translation not always perfect

---

## 🌍 Lang Sipòte / Supported Languages

Script la ka tradui **NAN** Kreyòl Ayisyen soti nan:

The script can translate **TO** Haitian Creole from:

- 🇫🇷 Franse / French
- 🇺🇸 Angle / English
- 🇪🇸 Panyòl / Spanish
- 🇵🇹 Pòtigè / Portuguese
- 🇩🇪 Alman / German
- 🇮🇹 Italyen / Italian
- 🇨🇳 Chinwa / Chinese
- 🇯🇵 Japonè / Japanese
- ...ak plis pase 90 lòt lang / and 90+ other languages

---

## 🔬 Kijan li Fonksyone / How It Works

### Etap 1: Ekstraksyon (30s - 2min)
```python
PDF → pypdf → Tèks brit / Raw text
```

### Etap 2: Deteksyon Lang (instant)
```python
Tèks → langdetect → Lang detekte (ex: "fr", "en")
```

### Etap 3: Tradiksyon (5-20min)
```python
Tèks → Divize an moso → M2M100 → Tradui chak moso → Ranmase rezilta yo
```

### Etap 4: Odyo (1-5min)
```python
Tèks Kreyòl → gTTS → MP3 audiobook
```

---

## 👥 Ki Moun Ki Ka Itilize Sa? / Who Can Use This?

- 📚 **Etidyan** ki bezwen materyèl edikasyon an Kreyòl
- 👨‍🏫 **Pwofesè** ki vle kreye resous pou elèv yo
- 📖 **Bibliyotèk** ki vle òfri liv odyo Kreyòl
- 🏛️ **ONG** ki travay nan edikasyon ak alfabetizasyon
- 👴 **Granmoun** ki prefere koute pito ke li
- 🌍 **Dyaspora** ki vle konsève lang Kreyòl la
- 💻 **Devlopè** ki vle amelyore zouti a

---

## 🚀 Amelyorasyon Pwochen / Future Improvements

- [ ] Sipò pou PDF eskane (OCR)
- [ ] Entèfas grafik (GUI)
- [ ] Plis opsyon vwa pou TTS
- [ ] Tradiksyon bidireksyonèl (Kreyòl → lòt lang)
- [ ] Sipò pou lòt fòma (EPUB, DOCX, TXT)
- [ ] Aplikasyon mobil (Android/iOS)
- [ ] API web pou entegrasyon
- [ ] Amelyorasyon modèl AI pou Kreyòl espesifikman

---

## 📄 Lisans / License

MIT License - 100% gratis pou itilize, modifye, ak distribye

---

## 🙏 Remèsiman / Acknowledgments

- **Facebook AI Research** - Pou modèl M2M100
- **Hugging Face** - Pou bibliyotèk transformers
- **Google** - Pou gTTS
- **Kominote Kreyòl Ayisyen** - Pou enspirasyon ak sipò

---

## 📞 Kontak / Contact

Si ou gen kesyon, sijesyon, oswa si ou vle kontribye:

- Ouvè yon Issue sou GitHub
- Kontakte kominote devlopè Kreyòl
- Pataje pwojè a ak lòt moun!

---

**Ansanm, nou ka fè teknoloji pi aksesib pou tout moun ki pale Kreyòl! 🇭🇹**

**Together, we can make technology more accessible for all Creole speakers! 🇭🇹**

