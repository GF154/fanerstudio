# 🚀 Gid Rapid / Quick Start Guide

## 3 Etap Rapid / 3 Quick Steps

### 1️⃣ Enstale / Install
```bash
pip install -r requirements.txt
```

### 2️⃣ Mete PDF la / Place PDF
Mete yon fichye PDF nan `data/input.pdf`

### 3️⃣ Egzekite / Run
```bash
python main.py
```

---

## 📋 Sa ki Pase / What Happens

```
📖 Extraction PDF              → data/output_text.txt
     ↓
🧠 Tradiksyon an Kreyòl       → output/traduction.txt
     ↓
🎧 Kreyasyon Liv Odyo         → output/audiobook.mp3
```

---

## ⏱️ Tan Egzekisyon / Execution Time

| Etap / Step | Tan / Time | Premye Fwa / First Time |
|-------------|-----------|------------------------|
| Extraction | 30s - 2min | 30s - 2min |
| Tradiksyon | 5min - 20min | 5min - 20min + telechajman modèl (~1.5GB) |
| Odyo | 1min - 5min | 1min - 5min |

**Total:** ~6-27 minit (premye fwa: +10min pou telechaje modèl)

---

## 🎯 Kondisyon Sistem / System Requirements

- **Python:** 3.8+
- **RAM:** 4GB minimum, 8GB rekòmande
- **Espas Disk:** 3GB pou modèl ak depandans
- **Entènèt:** Sèlman pou premye enstàlasyon ak premye egzekisyon

---

## 💡 Konsèy Rapid / Quick Tips

### Pou PDF gwo
Si PDF w gen plis pase 100 paj, tradiksyon ap pran plis tan. Swa pasyans!

### Pou evite problèm memwa
Fèmen lòt aplikasyon pandan w ap egzekite script la.

### Si modèl la twò gwo
Modifye `main.py` liy 36 pou itilize:
```python
model_name="facebook/m2m100_1.2B"  # Modèl pi gwo, pi bon rezilta
# oswa / or
model_name="Helsinki-NLP/opus-mt-mul-ht"  # Modèl pi piti, pi rapid
```

---

## 🆘 Sipò Rapid / Quick Support

### Erè: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Erè: "out of memory"
- Fèmen lòt aplikasyon
- Itilize yon modèl pi piti
- Divize PDF la an moso pi piti

### Erè: "PDF pa jwenn"
Verifye ke PDF la nan:
```
projet_kreyol_IA/data/input.pdf
```

---

## 📊 Egzanp Rezilta / Example Output

```
===================================================
🇭🇹 PWOJÈ KREYÒL IA / HAITIAN CREOLE AI PROJECT
===================================================

⏳ ETAP 1: Ekstraksyon tèks nan PDF...
Extraction PDF: 100%|████████| 45/45 [00:12<00:00, 3.75page/s]
✅ Tèks ekstrè sove nan: data/output_text.txt
   📊 Total karaktè: 125,430

🧠 ETAP 2: Tradiksyon an kreyòl ayisyen...
🌍 Lang orijinal detekte: fr
Tradiksyon an kreyòl: 100%|████| 125/125 [05:23<00:00, 2.59s/chunk]
✅ Tradiksyon sove nan: output/traduction.txt

🎧 ETAP 3: Kreye liv odyo kreyòl...
✅ Liv odyo sove nan: output/audiobook.mp3

===================================================
✅ LIV ODYO AN KREYÒL PARE!
===================================================
📄 Tèks orijinal: data/output_text.txt
🌍 Tèks tradui: output/traduction.txt
🔊 Liv odyo: output/audiobook.mp3
===================================================
```

---

## 🎓 Pou Aprann Plis / Learn More

- **README.md** - Dokimantasyon konplè / Full documentation
- **INSTALL.md** - Gid enstalasyon detaye / Detailed installation guide
- **example.py** - Egzanp kod / Code examples

---

**Fèt ak ❤️ pou kominote Kreyòl Ayisyen**

