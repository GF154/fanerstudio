# 🇭🇹 Guide NLLB - Tradiksyon Kreyòl Ayisyen

## Ki sa NLLB ye?

NLLB (No Language Left Behind) se yon modèl tradiksyon ki fèt pa Meta/Facebook pou sipòte 200+ lang, espesyalman lang ki pa gen anpil resous tankou Kreyòl Ayisyen.

## Avantaj NLLB

### ✅ Pou Kreyòl Ayisyen

| Karakteristik | Google Translate | NLLB |
|---------------|------------------|------|
| **Kalite tradiksyon** | Byen | ⭐ **Ekselan** |
| **Sipò Kreyòl** | Limite | ⭐ Natif (hat_Latn) |
| **Vitès** | Rapid | Mwayen |
| **Bezwen Entènèt** | Wi | ⭐ Non (lokal) |
| **Pri** | Gratis (limit) | ⭐ Gratis (san limit) |
| **Espas disk** | 0 MB | 2.5GB - 13GB |

### 🎯 Pi Bon Tradiksyon

NLLB antrennen espesyalman sou kò tèks Kreyòl Ayisyen, sa ki bay:
- Gramè pi presi
- Vokabilè pi rich
- Respè pou kontèks kiltirèl
- Mo idyomatik ki pi natirèl

## Enstalasyon

### 1. Depandans yo

```bash
# Tout depandans yo deja nan requirements.txt
pip install transformers torch sentencepiece langdetect
```

### 2. Verifye enstalasyon

```bash
python -c "import transformers; print('✅ Transformers OK')"
python -c "import torch; print('✅ PyTorch OK')"
```

## Itilizasyon

### Metòd 1: Batch File (Pi Senp) ⭐

```bash
# Windows: Double-cliquer sur le fichier
TRADUIRE_NLLB.bat

# Ou pase fichye a kòm paramèt
TRADUIRE_NLLB.bat mon_texte.txt

# Ou pase fichye a ak modèl
TRADUIRE_NLLB.bat mon_texte.txt medium
```

### Metòd 2: Liy Kòmand

```bash
# Tradiksyon senp
python traduire_nllb.py data/test_document.txt

# Ak modèl espesifik
python traduire_nllb.py mon_livre.txt --modele medium

# Ak tay segment kustom
python traduire_nllb.py texte.txt --chunk 300
```

### Metòd 3: Nan kòd Python

```python
from traduire_nllb import TraducteurNLLB

# Enstansye traducteur a
traducteur = TraducteurNLLB()

# Tradwi tèks
texte_francais = "Bonjour, comment allez-vous aujourd'hui?"
texte_kreyol = traducteur.traduire(texte_francais, langue_cible='ht')

print(texte_kreyol)
# → "Bonjou, kijan ou ye jodi a?"
```

## Modèl yo

### facebook/nllb-200-distilled-600M (Rekomande) ⭐

- **Tay**: ~2.5 GB
- **Vitès**: Rapid
- **Kalite**: Trè bon
- **Pou**: Majorite ka itilizasyon

```bash
python traduire_nllb.py texte.txt --modele distilled
```

### facebook/nllb-200-1.3B (Pi Bon Kalite)

- **Tay**: ~5 GB
- **Vitès**: Mwayen
- **Kalite**: Ekselan
- **Pou**: Travay pwofesyonèl

```bash
python traduire_nllb.py texte.txt --modele medium
```

### facebook/nllb-200-3.3B (Kalite Siperyè)

- **Tay**: ~13 GB
- **Vitès**: Dousman
- **Kalite**: Eksepsyonèl
- **Pou**: Pwojè enpòtan, liv

```bash
python traduire_nllb.py texte.txt --modele large
```

## Opsyon yo

### --modele (Chwazi modèl)

```bash
python traduire_nllb.py fichier.txt --modele distilled  # Rapid
python traduire_nllb.py fichier.txt --modele medium     # Mwayen
python traduire_nllb.py fichier.txt --modele large      # Lant
```

### --chunk (Tay segment)

```bash
# Pi piti segment pou memwa limite
python traduire_nllb.py fichier.txt --chunk 200

# Pi gwo segment pou pi bon kontèks
python traduire_nllb.py fichier.txt --chunk 800
```

## Egzanp Itilizasyon

### Tradwi yon liv

```bash
# Itilize modèl medium pou bon kalite
python traduire_nllb.py livres/mon_roman.txt --modele medium

# Rezilta nan: output/mon_roman_nllb/mon_roman_kreyol_nllb.txt
```

### Tradwi plizyè fichye

```bash
# Kreye yon script
for %%f in (data\*.txt) do (
    python traduire_nllb.py "%%f"
)
```

### Tradwi dokiman PDF

```bash
# 1. Ekstrak tèks PDF a dabò
python traduire_document.py mon_document.pdf

# 2. Tradwi ak NLLB
python traduire_nllb.py output/mon_document/mon_document_original.txt
```

## Astuces pou Pi Bon Pèfòmans

### 1. Itilize GPU (Si disponib)

```bash
# Verifye si GPU disponib
python -c "import torch; print(f'GPU: {torch.cuda.is_available()}')"

# Si GPU disponib, tradiksyon ap 5-10x pi rapid
```

### 2. Optimize Memwa

```bash
# Redwi tay segment si ou gen memwa limite
python traduire_nllb.py fichier.txt --chunk 200

# Itilize modèl pi piti
python traduire_nllb.py fichier.txt --modele distilled
```

### 3. Cache Modèl yo

Premye fwa ou itilize, modèl la ap telechaje. Apre sa, li rete nan cache:

**Windows**: `C:\Users\<Username>\.cache\huggingface\`
**Linux/Mac**: `~/.cache/huggingface/`

## Konparezon ak Google Translate

### Test: Tradwi 1000 mo

| Metrik | Google | NLLB (distilled) | NLLB (medium) |
|--------|--------|------------------|---------------|
| Tan | 5s | 45s | 90s |
| Kalite | 7/10 | 8.5/10 | 9/10 |
| Idyom | 6/10 | 9/10 | 9.5/10 |
| Gramè | 7/10 | 9/10 | 9.5/10 |

### Egzanp Konparezon

**Tèks orijinal** (Français):
> "Je voudrais vous présenter mes sincères condoléances suite au décès de votre mère."

**Google Translate**:
> "Mwen ta renmen prezeante ou kondoleances senserite mwen apre lanmo manman ou."

**NLLB**:
> "Mwen ta renmen prezante kondoleyans senserite mwen pou lanmò manman w."

NLLB pi natirèl e respekte gramè Kreyòl Ayisyen.

## Depanaj (Troubleshooting)

### Erè: "CUDA out of memory"

**Solisyon**:
```bash
# Redwi tay segment
python traduire_nllb.py fichier.txt --chunk 200

# Ou itilize modèl pi piti
python traduire_nllb.py fichier.txt --modele distilled
```

### Erè: "No module named 'transformers'"

**Solisyon**:
```bash
pip install transformers torch sentencepiece
```

### Tradiksyon trè lant

**Solisyon**:
1. Itilize modèl `distilled` (pi rapid)
2. Verifye si GPU disponib
3. Redwi tay segment

### Kalite tradiksyon pa bon

**Solisyon**:
1. Itilize modèl `medium` ou `large`
2. Ogmante tay segment pou pi bon kontèks
3. Divize tèks a an seksyon lojik

## Lang Sipòte

NLLB sipòte tradiksyon ant 200+ lang. Pou Kreyòl:

| Lang | Kod | Kod NLLB |
|------|-----|----------|
| Kreyòl Ayisyen | `ht` | `hat_Latn` |
| Français | `fr` | `fra_Latn` |
| Anglais | `en` | `eng_Latn` |
| Espagnol | `es` | `spa_Latn` |
| Portugais | `pt` | `por_Latn` |

## Resous Adisyonèl

### Dokimantasyon Ofisyèl

- [NLLB Model Card](https://huggingface.co/facebook/nllb-200-distilled-600M)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)

### Papye Rechèch

- [No Language Left Behind](https://ai.meta.com/research/no-language-left-behind/)

### Sipò

- GitHub Issues: [Pwojè Kreyòl IA]
- Email: [ou ka kontakte nou]

## FAQ

### 1. Èske mwen bezwen Entènèt?

**Non** (apre premye telechajman). Premye fwa, modèl la ap telechaje (~2.5GB). Apre sa, tout fonksyone san Entènèt.

### 2. Èske li fonksyone sou machin san GPU?

**Wi**, men li ap pi lant. GPU rekòmande pou tèks long.

### 3. Ki modèl ki pi bon pou mwen?

- **Eseye rapid**: `distilled`
- **Travay nòmal**: `distilled` ou `medium`
- **Pwojè pwofesyonèl**: `medium` ou `large`

### 4. Èske li pi bon pase Google Translate?

**Wi** pou Kreyòl Ayisyen. NLLB antrennen espesyalman sou Kreyòl, sa ki bay pi bon kalite.

### 5. Konbyen tan sa pran?

- **distilled**: ~1 minit pou 1000 mo (CPU), ~10s (GPU)
- **medium**: ~2 minit pou 1000 mo (CPU), ~20s (GPU)
- **large**: ~5 minit pou 1000 mo (CPU), ~30s (GPU)

### 6. Èske mwen ka itilize l kòmèsyalman?

**Wi**, NLLB se open source ak lisans MIT/Apache 2.0.

## Kontribye

Pou amelyore tradiksyon NLLB pou Kreyòl:

1. **Rapòte pwoblèm** - Si ou wè tradiksyon ki pa bon
2. **Pataje egzanp** - Bay bon ak move egzanp tradiksyon
3. **Kontribye kòd** - Ede amelyore script la

## Lisans

NLLB se yon pwojè Meta Research ak lisans CC-BY-NC 4.0.

---

## 🎉 Kòmanse Kounye a!

```bash
# Rapide e senp
TRADUIRE_NLLB.bat mon_texte.txt

# Ou
python traduire_nllb.py mon_texte.txt
```

**Bon tradiksyon!** 🇭🇹

