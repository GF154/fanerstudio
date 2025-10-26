# 🎙️ Guide des Voix Naturelles pour le Créole Haïtien

## 🌟 Nouvelles Fonctionnalités Vocales

J'ai ajouté un système de voix amélioré pour une meilleure prononciation du créole haïtien!

---

## 📊 Options Disponibles

### **Option 1: Microsoft Edge TTS (Meilleure Qualité)** ⭐ RECOMMANDÉ

**Avantages:**
- ✅ Qualité exceptionnelle
- ✅ Voix naturelles et expressives
- ✅ Français canadien disponible (proche du créole)
- ✅ Gratuit et illimité
- ✅ Plusieurs voix au choix

**Installation:**
```powershell
.\venv\Scripts\Activate.ps1
pip install edge-tts
```

**Voix Recommandées:**
- `fr-FR-DeniseNeural` (Femme, claire) ⭐
- `fr-FR-HenriNeural` (Homme, professionnel)
- `fr-CA-SylvieNeural` (Canadienne, femme)
- `fr-CA-AntoineNeural` (Canadien, homme)

---

### **Option 2: Google TTS - Français Canadien (Actuel)**

**Avantages:**
- ✅ Déjà installé
- ✅ Très bonne qualité
- ✅ Prononciation canadienne (meilleure pour le créole)
- ✅ Fonctionne immédiatement

**Utilisation:** Activé automatiquement

---

### **Option 3: pyttsx3 (Hors Ligne)**

**Avantages:**
- ✅ Fonctionne sans internet
- ✅ Gratuit
- ✅ Rapide
- ⚠️ Qualité moyenne

**Installation:**
```powershell
.\venv\Scripts\Activate.ps1
pip install pyttsx3
```

---

## 🚀 Installation Rapide (Recommandé)

### **Pour la Meilleure Qualité:**

```powershell
# Naviguer au dossier du projet
cd "C:\Users\Fanerlink\OneDrive\Documents\liv odyo\projet_kreyol_IA"

# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Installer Edge TTS (voix de qualité supérieure)
pip install edge-tts

# Installer pyttsx3 (voix hors ligne, optionnel)
pip install pyttsx3

# Redémarrer l'application
# Ctrl+C puis:
streamlit run app.py
```

---

## 🎯 Comparaison des Voix

| Moteur | Qualité | Prononciation Créole | Internet Requis | Installation |
|--------|---------|---------------------|-----------------|--------------|
| **Edge TTS** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Oui | `pip install edge-tts` |
| **gTTS (fr-CA)** | ⭐⭐⭐⭐ | ⭐⭐⭐ | Oui | ✅ Déjà installé |
| **gTTS (fr)** | ⭐⭐⭐⭐ | ⭐⭐⭐ | Oui | ✅ Déjà installé |
| **pyttsx3** | ⭐⭐ | ⭐⭐ | Non | `pip install pyttsx3` |

---

## 🔧 Configuration Avancée

### **Choisir une Voix Spécifique (Edge TTS)**

Créez un fichier `.env` avec:

```env
# Voix pour l'audio
TTS_ENGINE=edge
TTS_VOICE=fr-FR-DeniseNeural

# Autres options:
# fr-FR-HenriNeural (homme)
# fr-CA-SylvieNeural (canadienne)
# fr-CA-AntoineNeural (canadien)
```

### **Liste Complète des Voix Françaises:**

```powershell
# Installer edge-tts
pip install edge-tts

# Lister toutes les voix disponibles
edge-tts --list-voices | findstr "fr-"
```

**Voix Disponibles:**

1. **France:**
   - `fr-FR-DeniseNeural` (Femme) ⭐ Recommandé
   - `fr-FR-HenriNeural` (Homme)
   - `fr-FR-AlainNeural` (Homme)
   - `fr-FR-BrigitteNeural` (Femme)
   - `fr-FR-CelesteNeural` (Femme)
   - `fr-FR-ClaudeNeural` (Homme)
   - `fr-FR-CoralieNeural` (Femme)
   - `fr-FR-EloiseNeural` (Femme, enfant)
   - `fr-FR-JacquelineNeural` (Femme)
   - `fr-FR-JeromeNeural` (Homme)
   - `fr-FR-JosephineNeural` (Femme)
   - `fr-FR-MauriceNeural` (Homme)
   - `fr-FR-YvesNeural` (Homme)
   - `fr-FR-YvetteNeural` (Femme)

2. **Canada:**
   - `fr-CA-SylvieNeural` (Femme) ⭐ Recommandé pour Créole
   - `fr-CA-AntoineNeural` (Homme)
   - `fr-CA-JeanNeural` (Homme)
   - `fr-CA-ThierryNeural` (Homme)

3. **Belgique:**
   - `fr-BE-CharlineNeural` (Femme)
   - `fr-BE-GerardNeural` (Homme)

4. **Suisse:**
   - `fr-CH-ArianeNeural` (Femme)
   - `fr-CH-FabriceNeural` (Homme)

---

## 💡 Recommandations Spéciales pour le Créole

### **Meilleure Option:**

**Voice: `fr-CA-SylvieNeural`** (Canadienne)

**Pourquoi?**
- ✅ Accent canadien proche du créole haïtien
- ✅ Prononciation claire et naturelle
- ✅ Rythme adapté
- ✅ Intonation agréable

**Comment l'utiliser:**

```python
# L'application choisit automatiquement la meilleure voix
# Mais vous pouvez forcer une voix dans src/tts_enhanced.py
```

---

## 🎧 Test des Voix

### **Script de Test:**

Créez `test_voices.py`:

```python
import asyncio
from pathlib import Path
from src.tts_enhanced import EnhancedTTS

async def test_voices():
    tts = EnhancedTTS()
    
    text = "Bonjou! Kijan ou ye? Mwen kontan rankontre ou."
    
    voices = [
        "fr-FR-DeniseNeural",
        "fr-CA-SylvieNeural",
        "fr-FR-HenriNeural",
    ]
    
    for voice in voices:
        output = Path(f"test_{voice}.mp3")
        print(f"Testing {voice}...")
        await tts.generate_edge_tts(text, output, voice)
        print(f"✅ Saved to {output}")

# Run test
asyncio.run(test_voices())
```

**Exécuter:**
```powershell
python test_voices.py
```

Écoutez les fichiers MP3 générés et choisissez votre préféré!

---

## 🔄 Comment ça Marche

### **Ordre de Priorité Automatique:**

Quand vous générez de l'audio pour le créole:

1. **Edge TTS** est essayé en premier (si installé)
   - Voix: `fr-FR-DeniseNeural` par défaut
   - Qualité: ⭐⭐⭐⭐⭐

2. **gTTS Canadien** ensuite
   - Langue: `fr-CA` (Français canadien)
   - Qualité: ⭐⭐⭐⭐

3. **gTTS Standard** si échec
   - Langue: `fr` (Français)
   - Qualité: ⭐⭐⭐⭐

4. **pyttsx3** en dernier recours
   - Hors ligne
   - Qualité: ⭐⭐

---

## 📝 Utilisation dans l'Application

### **Avec l'Interface Web:**

1. **Activez Enhanced TTS:**
   ```powershell
   pip install edge-tts
   ```

2. **Redémarrez Streamlit:**
   ```powershell
   Ctrl+C
   streamlit run app.py
   ```

3. **Uploadez votre PDF**

4. **Lors de la génération audio, vous verrez:**
   ```
   🎧 Ap kreye odyo / Generating audio...
   🌟 Using enhanced TTS for better Creole pronunciation
   Engine: Microsoft Edge TTS (fr-FR-DeniseNeural)
   ✅ Liv odyo sove nan / Audiobook saved
   ```

### **Via Code Python:**

```python
from src import Config, AudiobookGenerator

config = Config()
generator = AudiobookGenerator(config, use_enhanced=True)

text = "Bonjou! Sa a se yon tès an kreyòl."
output = generator.generate(text, language='ht')
```

---

## 🎯 Exemples de Prononciation

### **Texte Créole:**
```
Bonjou zanmi! Kijan ou ye jodi a?
Mwen espere ou pase yon bon jounen.
```

### **Avec Edge TTS (fr-CA-SylvieNeural):**
- ✅ Prononciation naturelle
- ✅ Rythme approprié
- ✅ Intonation créole-friendly

### **Avec gTTS standard:**
- ⚠️ Prononciation française standard
- ⚠️ Moins naturel pour le créole

---

## 🆘 Dépannage

### **Edge TTS ne fonctionne pas?**

```powershell
# Réinstaller
pip uninstall edge-tts
pip install edge-tts

# Tester directement
edge-tts --text "Bonjou" --voice fr-CA-SylvieNeural --write-media test.mp3
```

### **Erreur "No module named 'edge_tts'"?**

```powershell
# Vérifier l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Réinstaller dans le bon environnement
pip install edge-tts
```

### **Pas de son dans les fichiers?**

- Vérifiez que FFmpeg est installé
- Testez avec un lecteur MP3 différent
- Vérifiez la taille du fichier (> 0 KB)

---

## 📊 Résultats Attendus

### **Avant (gTTS Standard):**
```
Audio: 558.2KB
Qualité: ⭐⭐⭐⭐
Prononciation: Française standard
```

### **Après (Edge TTS):**
```
Audio: Variable (dépend du texte)
Qualité: ⭐⭐⭐⭐⭐
Prononciation: Plus naturelle pour le créole
Voix: Expressive et claire
```

---

## ✅ Checklist d'Installation

- [ ] Installer Edge TTS: `pip install edge-tts`
- [ ] (Optionnel) Installer pyttsx3: `pip install pyttsx3`
- [ ] Redémarrer l'application
- [ ] Tester avec un petit texte
- [ ] Comparer les voix
- [ ] Choisir votre préférée

---

## 🎉 Prochaines Étapes

1. **Installer Edge TTS** pour la meilleure qualité
2. **Tester différentes voix** avec le script de test
3. **Configurer votre voix préférée** dans `.env`
4. **Profiter d'audio de qualité supérieure!**

---

## 📚 Ressources Supplémentaires

- **Edge TTS Documentation:** https://github.com/rany2/edge-tts
- **Liste des voix:** `edge-tts --list-voices`
- **gTTS Documentation:** https://gtts.readthedocs.io/

---

**Fèt ak ❤️ pou kominote Kreyòl Ayisyen 🇭🇹**

**Maintenant avec des voix encore plus naturelles!** 🎙️✨

