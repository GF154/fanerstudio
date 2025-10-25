# 📚 GID POU TRETMAN GWO DOKIMAN PDF

## 🎯 Objektif
Platfòm lan kounye a sipòte ekstraksyon ak pwosesis gwo dokiman PDF (jiska 10,000+ paj) ak optimize pou pèfòmans ak memwa.

---

## ✨ NOUVO FONKSYONALITE

### **1. Ekstraksyon Optimize ak Chunk Processing**

#### Kapasite:
- ✅ **PDF jiska 100 MB**
- ✅ **Jiska 10,000+ paj** (ak limit)
- ✅ **Chunk processing** (50 paj pa fwa)
- ✅ **Progress bars** pou gwo fichye
- ✅ **Memwa optimize** ak streaming

#### Paramèt:
```python
await extract_text_from_document(
    file_path="document.pdf",
    max_pages=500,        # Limit paj (None = tout)
    show_progress=True    # Afiche pwogresyon
)
```

---

### **2. Streaming Extraction (Nivo 2)**

Pou PDF **trè gwo** (2000+ paj):

```python
await extract_text_from_pdf_streaming(
    pdf_path=Path("large.pdf"),
    chunk_size_pages=100,     # Paj pa chunk
    callback=progress_callback # Optional callback
)
```

#### Avantaj:
- ✅ Memwa konsomatif **pi ba**
- ✅ Pwosesis **pa bloke**
- ✅ Progress **real-time**
- ✅ Kapab **rezime** si echwe

---

## 📊 LIMIT AK PÈFÒMANS

| Gwosè PDF | Paj | Tan Estimé | Metòd Rekòmande |
|-----------|-----|------------|-----------------|
| < 10 MB | < 100 | 30s - 2min | Standard |
| 10-50 MB | 100-500 | 2-10 min | Standard ak max_pages |
| 50-100 MB | 500-2000 | 10-30 min | Streaming |
| > 100 MB | > 2000 | 30+ min | Streaming + limit |

---

## 🔧 ITILIZASYON

### **Via API (Endpoint Standard):**

```bash
curl -X POST http://localhost:8000/api/audiobook \
  -F "file=@large_document.pdf" \
  -F "voice=creole-native" \
  -F "max_pages=500" \
  -F "show_progress=true"
```

### **Via API (Endpoint Streaming):**

```bash
curl -X POST http://localhost:8000/api/audiobook-streaming \
  -F "file=@very_large.pdf" \
  -F "voice=creole-native" \
  -F "chunk_size_pages=100"
```

### **Via Python:**

```python
from app.services.media_service import MediaService
from pathlib import Path

media = MediaService()

# Standard extraction
text = await media.extract_text_from_document(
    "document.pdf",
    max_pages=300,
    show_progress=True
)

# Streaming extraction
text = await media.extract_text_from_pdf_streaming(
    Path("large.pdf"),
    chunk_size_pages=100
)
```

---

## ⚠️ WARNING POU GWO FICHYE

### **PDF > 1000 paj:**

Lè ou upload yon PDF gwo, sistèm nan ap afiche:

```
⚠️  GWO PDF DETEKTE!
   📄 Paj: 2,347
   💾 Gwosè: 78.45 MB
   ⏱️  Tan estimé: 46-78 minit
```

### **Rekòmandasyon:**
1. ✅ Itilize `max_pages` pou limite ekstraksyon
2. ✅ Itilize endpoint `/api/audiobook-streaming`
3. ✅ Chwazi `chunk_size_pages` pi piti (50-100)
4. ✅ Teste ak yon pati dokiman an avan

---

## 📈 PROGRESS INDICATORS

### **Progress Bar (PDF > 20 paj):**

```
📄 Ekstrè PDF: 45%|████████▌         | 450/1000 [02:15<02:45,  3.3 paj/s]
```

### **Manual Progress (chak 100 paj):**

```
   ✓ 100/1000 paj ekstrè...
   ✓ 200/1000 paj ekstrè...
   ✓ 300/1000 paj ekstrè...
```

### **Streaming Chunks:**

```
   ✓ Chunk 1-100/2000 done
   ✓ Chunk 101-200/2000 done
   📊 Pwogresyon: 10.0% (200/2000 paj)
```

---

## 🛡️ ERROR HANDLING

### **Erè Paj:**
Si yon paj gen pwoblèm, sistèm nan ap skip epi kontinye:

```
⚠️  Erè paj 347: The input size 0, plus negative...
[Erè paj 347]
```

### **Timeout:**
Si pwosesis pran twòp tan (endpoint streaming):

```http
HTTP 504 Gateway Timeout
{
  "detail": "Timeout! Fichye a tro gwo. Eseye ak chunk_size pi piti."
}
```

---

## 🧪 TESTE

### **Test Manual:**

1. Mete yon PDF nan foldè `input/`
2. Lance: `TEST_GWO_PDF.bat`
3. Chwazi yon opsyon test
4. Gade rezilta yo

### **Test API:**

1. Lance sèvè: `python -m uvicorn app.api:app --reload`
2. Ouvri: `http://localhost:8000/docs`
3. Test endpoint `/api/audiobook` oswa `/api/audiobook-streaming`

---

## 💡 TIP POU OPTIMIZE

### **1. Chwazi Bon Chunk Size:**
- **PDF senp (tèks):** 100-200 paj
- **PDF konplèks (imaj):** 50-100 paj
- **PDF trè gwo:** 25-50 paj

### **2. Itilize max_pages:**
```python
# Teste ak premye 100 paj avan pwosese tout
text = await extract_text_from_document(
    "large.pdf",
    max_pages=100  # Test rapid
)
```

### **3. Monitè Memwa:**
```bash
# Windows
tasklist /FI "IMAGENAME eq python.exe"

# Si memwa > 2 GB, diminye chunk_size
```

---

## 📊 ESTATISTIK FINAL

Apre ekstraksyon, ou ap wè:

```
✅ Ekstraksyon konple!
   📄 Paj pwosese: 500/2000
   📝 Mo: 145,789
   🔤 Karaktè: 892,456
```

---

## 🚀 QUICK START

### **Ekstraksyon Rapid (< 100 paj):**
```python
text = await media.extract_text_from_document("document.pdf")
```

### **Ekstraksyon Mwayen (100-500 paj):**
```python
text = await media.extract_text_from_document(
    "document.pdf",
    max_pages=300
)
```

### **Ekstraksyon Gwo (500+ paj):**
```python
text = await media.extract_text_from_pdf_streaming(
    Path("large.pdf"),
    chunk_size_pages=100
)
```

---

## 📞 SIPÒ

Si ou gen pwoblèm ak gwo PDF:

1. ✅ Verifye gwosè fichye (< 100 MB rekòmande)
2. ✅ Diminye `max_pages` oswa `chunk_size_pages`
3. ✅ Itilize streaming endpoint pou fichye trè gwo
4. ✅ Check memwa disponib sou sistèm ou

---

## 🎯 REZIME

| Fonksyonalite | Status | Nivo |
|---------------|--------|------|
| Chunk processing | ✅ | Nivo 1 |
| Progress indicators | ✅ | Nivo 1 |
| Warning gwo fichye | ✅ | Nivo 1 |
| Streaming extraction | ✅ | Nivo 2 |
| Callback progress | ✅ | Nivo 2 |
| Memwa optimize | ✅ | Nivo 2 |
| Timeout protection | ✅ | Nivo 1 |
| API endpoints | ✅ | Konple |

---

**Vèsyon:** 3.2.0  
**Dènye Mizajou:** 2025-10-24  
**Status:** ✅ PRÊT POU PRODWIKSYON

