# 🚀 Gid Enstalasyon Rapid / Quick Installation Guide

## Etap 1: Enstale Python / Install Python

Asire w gen Python 3.8+ enstale:
```bash
python --version
```

## Etap 2: Kreye Anviwònman Viryèl / Create Virtual Environment

**Windows:**
```bash
cd "C:\Users\Fanerlink\OneDrive\Documents\liv odyo\projet_kreyol_IA"
python -m venv venv
.\venv\Scripts\activate
```

**Mac/Linux:**
```bash
cd projet_kreyol_IA
python3 -m venv venv
source venv/bin/activate
```

## Etap 3: Enstale Depandans / Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### ⚠️ Pou PyTorch / For PyTorch

Si ou gen pwoblèm ak `torch`, chwazi vèsyon ki adapte ak sistèm ou:

**CPU sèlman / CPU only:**
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**Ak CUDA (pou GPU NVIDIA) / With CUDA (for NVIDIA GPU):**
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

## Etap 4: Teste Enstalasyon / Test Installation

```bash
python -c "import pypdf, transformers, torch, gtts, langdetect, tqdm; print('✅ Tout bagay enstale kòrèkteman!')"
```

## 📦 Pakè Prensipal / Main Packages

| Pakè / Package | Itilizasyon / Usage |
|----------------|---------------------|
| `pypdf` | Ekstraksyon tèks PDF / PDF text extraction |
| `transformers` | Modèl NLP avanse / Advanced NLP models |
| `torch` | PyTorch (sipò pou transformers) / PyTorch (transformers support) |
| `gtts` | Text-to-Speech Google / Google Text-to-Speech |
| `langdetect` | Deteksyon lang otomatik / Automatic language detection |
| `tqdm` | Ba pwogrè / Progress bars |

## 🔧 Depannaj / Troubleshooting

### Pwoblèm 1: "Microsoft Visual C++ required"
**Solisyon Windows:**
- Telechaje ak enstale Microsoft C++ Build Tools
- https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Pwoblèm 2: torch twò gwo / torch too large
**Solisyon:**
```bash
# Itilize vèsyon CPU ki pi piti
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Pwoblèm 3: Erè memwa ak transformers
**Solisyon:**
- Modèl transformers yo gwo. Si ou pa bezwen yo, ou ka retire `transformers` ak `torch`
- Remove from requirements.txt if not needed

### Pwoblèm 4: Enstalasyon long
**Solisyon:**
- Sa nòmal, `torch` ak `transformers` yo gwo (plizyè GB)
- Swa pasyans oswa itilize vèsyon CPU ki pi piti

## ✅ Verifye Enstalasyon / Verify Installation

Apre enstalasyon, egzekite:
```bash
python main.py
```

Si ou wè mesaj konsènan `input.pdf`, tout bagay enstale byen!

---

**Nòt:** Premye fwa w enstale, li ka pran 10-30 minit selon vitès entènèt ou.
**Note:** First installation may take 10-30 minutes depending on your internet speed.

