# 🇭🇹 NLLB Pipeline - Gid Konplè

> **PDF → Tradiksyon → Audiobook ak NLLB**

## 🎯 Sa ki Fèt

Yon pipeline konplè ki:
1. ✅ Ekstrè tèks soti nan PDF
2. ✅ Tradwi an Kreyòl Ayisyen ak NLLB
3. ✅ Kreye audiobook an Kreyòl

---

## 🚀 Quick Start

### Metòd 1: Batch File (Pi Fasil)

```bash
# Franse → Kreyòl
NLLB_AUDIOBOOK.bat "mon_livre.pdf"

# Angle → Kreyòl
NLLB_AUDIOBOOK.bat "my_book.pdf" eng_Latn

# Panyòl → Kreyòl
NLLB_AUDIOBOOK.bat "mi_libro.pdf" spa_Latn
```

### Metòd 2: Python Dirèkteman

```bash
python app/nllb_pipeline.py livre.pdf fra_Latn
```

### Metòd 3: Nan Kòd Python

```python
from app.nllb_pipeline import pdf_to_kreyol_audiobook

# Simple usage
result = pdf_to_kreyol_audiobook(
    pdf_path="livre.pdf",
    src_lang="fra_Latn"
)

print(f"Audiobook: {result['audiobook']}")
```

---

## 📚 Usage Detaye

### Class NLLBPipeline

```python
from app.nllb_pipeline import NLLBPipeline

# Initialize pipeline
pipeline = NLLBPipeline(
    model_name="facebook/nllb-200-distilled-600M"
)

# Process PDF
result = pipeline.process_pdf_to_audiobook(
    pdf_path="livre.pdf",
    output_dir="output/mon_projet",
    src_lang="fra_Latn",
    use_native_tts=True  # Use Kreyòl native TTS
)

# Results
print(result['extracted_text'])   # Tèks ekstrè
print(result['translated_text'])  # Tèks tradwi
print(result['audiobook'])        # Audiobook MP3
```

### Individual Functions

```python
from app.nllb_pipeline import NLLBPipeline

pipeline = NLLBPipeline()

# 1. Extract text from PDF
text = pipeline.extract_text_from_pdf("livre.pdf")

# 2. Translate to Creole
translated = pipeline.translate_to_creole(
    text, 
    src_lang="fra_Latn",
    tgt_lang="hat_Latn",
    chunk_size=500
)

# 3. Create audiobook
pipeline.text_to_audio(
    translated, 
    output_audio="audiobook.mp3",
    lang="ht"
)
```

---

## 🌍 Lang Sipòte

### Lang Sous (src_lang)

| Lang | Code | Egzanp |
|------|------|--------|
| **Franse** | `fra_Latn` | "Bonjour le monde" |
| **Angle** | `eng_Latn` | "Hello world" |
| **Panyòl** | `spa_Latn` | "Hola mundo" |
| **Pòtigè** | `por_Latn` | "Olá mundo" |
| **Italyen** | `ita_Latn` | "Ciao mondo" |
| **Alman** | `deu_Latn` | "Hallo Welt" |

### Lang Sib (tgt_lang)

- **Kreyòl Ayisyen**: `hat_Latn` (Default)

---

## 🎨 Models NLLB Disponib

### 1. nllb-200-distilled-600M (Default)
- **Size**: 600M parameters
- **Speed**: ⚡⚡⚡ Rapid
- **Quality**: ⭐⭐⭐ Bon
- **RAM**: ~2 GB
- **Recommended**: ✅ Yes

```python
pipeline = NLLBPipeline("facebook/nllb-200-distilled-600M")
```

### 2. nllb-200-1.3B
- **Size**: 1.3B parameters
- **Speed**: ⚡⚡ Mwayen
- **Quality**: ⭐⭐⭐⭐ Trè Bon
- **RAM**: ~5 GB

```python
pipeline = NLLBPipeline("facebook/nllb-200-1.3B")
```

### 3. nllb-200-3.3B
- **Size**: 3.3B parameters
- **Speed**: ⚡ Ralanti
- **Quality**: ⭐⭐⭐⭐⭐ Ekselan
- **RAM**: ~13 GB

```python
pipeline = NLLBPipeline("facebook/nllb-200-3.3B")
```

---

## 🎧 TTS Options

### Option 1: gTTS (Default, Fast)
```python
result = pipeline.process_pdf_to_audiobook(
    pdf_path="livre.pdf",
    use_native_tts=False  # Use gTTS
)
```

### Option 2: Kreyòl Native (Better Quality)
```python
result = pipeline.process_pdf_to_audiobook(
    pdf_path="livre.pdf",
    use_native_tts=True  # Use Facebook MMS-TTS
)
```

---

## ⚙️ Advanced Configuration

### Chunk Size

```python
pipeline = NLLBPipeline()

# Smaller chunks = slower but more accurate
translated = pipeline.translate_to_creole(
    text,
    chunk_size=300  # Default: 500
)

# Larger chunks = faster but may lose context
translated = pipeline.translate_to_creole(
    text,
    chunk_size=1000
)
```

### Custom Output Directory

```python
result = pipeline.process_pdf_to_audiobook(
    pdf_path="livre.pdf",
    output_dir="output/mon_projet_special"
)
```

### Different Languages

```python
# English to Creole
result = pipeline.process_pdf_to_audiobook(
    pdf_path="book.pdf",
    src_lang="eng_Latn"
)

# Spanish to Creole
result = pipeline.process_pdf_to_audiobook(
    pdf_path="libro.pdf",
    src_lang="spa_Latn"
)
```

---

## 📊 Output Files

Chak run kreye 3 fichye:

```
output/nllb/
├── livre_extracted.txt      # Tèks orijinal ekstrè
├── livre_kreyol.txt          # Tradiksyon Kreyòl
└── livre_audiobook.mp3       # Audiobook Kreyòl
```

---

## 💡 Best Practices

### 1. Chunk Size Guidelines

| Document Type | Chunk Size | Why |
|--------------|------------|-----|
| **Teknik/Scientific** | 300-400 | Need more context |
| **General/Fiction** | 500-700 | Good balance |
| **Simple Text** | 800-1000 | Faster processing |

### 2. Model Selection

| Use Case | Model | Why |
|----------|-------|-----|
| **Testing** | 600M | Fast, good enough |
| **Production** | 1.3B | Best balance |
| **High Quality** | 3.3B | Best results |

### 3. TTS Selection

| Situation | TTS | Why |
|-----------|-----|-----|
| **Fast Processing** | gTTS | Very fast |
| **Better Quality** | Native | More natural |
| **Large Documents** | gTTS | Less resource intensive |

---

## 🚀 Performance Tips

### 1. Batch Processing

```python
from app.nllb_pipeline import NLLBPipeline

pipeline = NLLBPipeline()  # Load model once

# Process multiple PDFs
pdfs = ["livre1.pdf", "livre2.pdf", "livre3.pdf"]

for pdf in pdfs:
    print(f"Processing {pdf}...")
    result = pipeline.process_pdf_to_audiobook(pdf)
    print(f"✅ Done: {result['audiobook']}")
```

### 2. GPU Acceleration

```python
import torch

# Check if CUDA is available
if torch.cuda.is_available():
    print("✅ GPU disponib!")
    # NLLB will automatically use GPU
else:
    print("⚠️ Using CPU")
```

### 3. Memory Management

```python
# For large documents, process in smaller chunks
pipeline = NLLBPipeline()

# Use smaller chunks to avoid memory issues
translated = pipeline.translate_to_creole(
    text,
    chunk_size=300  # Smaller chunks use less memory
)
```

---

## 🐛 Troubleshooting

### Error: "Out of memory"
**Solution**: Use smaller chunk size or smaller model
```python
pipeline = NLLBPipeline("facebook/nllb-200-distilled-600M")
translated = pipeline.translate_to_creole(text, chunk_size=200)
```

### Error: "Model not found"
**Solution**: Download model manually
```bash
python -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; AutoTokenizer.from_pretrained('facebook/nllb-200-distilled-600M'); AutoModelForSeq2SeqLM.from_pretrained('facebook/nllb-200-distilled-600M')"
```

### Error: "PDF extraction failed"
**Solution**: Use alternative PDF library
```bash
pip install pdfplumber
```

---

## 📈 Comparison: NLLB vs Google Translate

| Feature | NLLB | Google Translate |
|---------|------|------------------|
| **Quality (Creole)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Speed** | ⚡⚡ Mwayen | ⚡⚡⚡ Rapid |
| **Offline** | ✅ Yes | ❌ No |
| **Cost** | FREE | FREE (with limits) |
| **Privacy** | ✅ Local | ⚠️ Cloud |
| **Context** | ✅ Excellent | ⭐⭐ Good |

---

## 🎓 Examples

### Example 1: Simple Usage

```bash
NLLB_AUDIOBOOK.bat "histoire_haiti.pdf"
```

### Example 2: English Book

```bash
NLLB_AUDIOBOOK.bat "haitian_history.pdf" eng_Latn
```

### Example 3: Programmatic

```python
from app.nllb_pipeline import pdf_to_kreyol_audiobook

result = pdf_to_kreyol_audiobook(
    pdf_path="documents/livre.pdf",
    output_dir="output/mon_audiobook",
    src_lang="fra_Latn",
    use_native_tts=True
)

print(f"✅ Audiobook prè: {result['audiobook']}")
print(f"📊 Stats: {result['stats']}")
```

---

## 📞 Support

Pou plis kesyon:
- 📚 Gade `README.md`
- 📖 Gade `NLLB_GUIDE.md`
- 🌐 Visit: https://github.com/facebookresearch/fairseq/tree/nllb

---

**Fèt ak ❤️ pou kominote Kreyòl Ayisyen** 🇭🇹

**Version**: 3.0.0  
**Last Updated**: 2025-10-23

