# 🎙️ Guide des Voix Naturelles Personnalisées

## 🌟 Ajouter des Voix Créoles Authentiques

Ce guide vous montre comment ajouter des enregistrements de voix naturelles en créole haïtien à votre plateforme!

---

## 🎯 Pourquoi des Voix Personnalisées?

### **Avantages:**

✅ **Prononciation authentique** - Vraies voix créoles  
✅ **Accent naturel** - Différentes régions d'Haïti  
✅ **Expressions locales** - Parler naturel  
✅ **Qualité supérieure** - Enregistrements professionnels  
✅ **Personnalisation** - Vos propres voix!  

### **Cas d'utilisation:**

- 📚 Livres audio en créole authentique
- 🎓 Matériel éducatif
- 📰 Nouvelles et actualités
- 📖 Contenu religieux ou culturel
- 🗣️ Narration d'histoires

---

## 🚀 Démarrage Rapide

### **Méthode 1: Interface Interactive (RECOMMANDÉ)**

```powershell
cd "C:\Users\Fanerlink\OneDrive\Documents\liv odyo\projet_kreyol_IA"
.\venv\Scripts\Activate.ps1
python add_custom_voice.py
```

**Interface en créole et anglais!**

### **Méthode 2: Interface Web Streamlit**

1. Lancez l'application: `streamlit run app.py`
2. Allez dans l'onglet **🎙️ Custom Voices** dans la sidebar
3. Suivez les instructions

---

## 📝 Comment Préparer Vos Enregistrements

### **Étape 1: Enregistrer la Voix**

#### **Équipement recommandé:**
- 🎤 Microphone USB de qualité (ou téléphone moderne)
- 🎧 Casque pour monitoring
- 🏠 Pièce calme sans écho

#### **Logiciels d'enregistrement:**
- **Windows:** Audacity (gratuit)
- **Mobile:** Voice Recorder, Easy Voice Recorder
- **En ligne:** Vocaroo, Online Voice Recorder

#### **Conseils d'enregistrement:**
1. **Parlez clairement** et naturellement
2. **Rythme normal** - ni trop vite ni trop lent
3. **Distance du micro** - 15-20 cm
4. **Évitez les bruits** de fond
5. **Testez d'abord** avant l'enregistrement final

### **Étape 2: Format du Fichier**

#### **Formats acceptés:**
- ✅ MP3 (recommandé)
- ✅ WAV
- ✅ M4A
- ✅ OGG
- ✅ FLAC

#### **Qualité recommandée:**
- **Bitrate:** 128 kbps minimum (192 kbps idéal)
- **Sample rate:** 44100 Hz
- **Mono ou Stereo:** Les deux OK (mono = fichier plus petit)

### **Étape 3: Préparer le Texte**

Écrivez **exactement** ce qui est dit dans l'enregistrement.

**Exemple:**

```
Bonjou zanmi! Kijan ou ye jodi a?
Mwen rele Marie, e mwen ap ede w aprann kreyòl.
Nou pral li yon istwa enteresan sou kilti ayisyen.
```

**Important:**
- ✅ Orthographe créole correcte
- ✅ Ponctuation appropriée
- ✅ Même texte que l'audio
- ✅ Aucune annotation

---

## 🎬 Guide Pas à Pas

### **Utilisation de l'Outil Interactif**

#### **1. Lancer l'outil:**

```powershell
python add_custom_voice.py
```

#### **2. Menu principal:**

```
🎙️  JESYON VWA NATIRÈL / NATURAL VOICE MANAGER
============================================================

1. Ajoute yon vwa / Add a voice
2. Wè tout vwa / List all voices
3. Estatistik / Statistics
4. Kite / Exit

Chwazi / Choose (1-4):
```

#### **3. Ajouter une voix (Option 1):**

L'outil vous guide étape par étape:

**a) Chemin du fichier audio:**
```
📁 Chemen fichye odyo / Audio file path: 
C:\Users\...\my_voice.mp3
```

**b) Nom de la voix:**
```
Non vwa a / Voice name [Voice_1]: 
Marie_Creole_Story
```

**c) Nom du speaker:**
```
Non moun ki pale a / Speaker name [Anonymous]: 
Marie Duval
```

**d) Texte parlé:**
```
📄 Tèks ki te di / Text that was spoken:
   (Tape ou kolye vwa a, tape 'END' sou yon liy pou fini)

Bonjou zanmi! Kijan ou ye jodi a?
Mwen rele Marie...
END
```

**e) Informations optionnelles:**
- Sexe (male/female/other/unknown)
- Âge (child/young_adult/adult/senior/unknown)
- Région (Haiti, Port-au-Prince, Cap-Haïtien, etc.)
- Notes

**f) Confirmation:**
```
✅ Ajoute vwa sa a? / Add this voice? (yes/no) [yes]:
yes
```

#### **4. Succès!**

```
✅ SIKSÈ / SUCCESS!
============================================================
Vwa ajoute avèk siksè / Voice added successfully!
ID: a3f5b8c91d2e
Fichye sove nan / File saved in: custom_voices/
```

---

## 📊 Gérer Vos Voix

### **Lister toutes les voix:**

Dans le menu principal, choisissez option **2**.

```
📚 VWA DISPONIB / AVAILABLE VOICES (3 total)
============================================================

1. Marie_Creole_Story
   ID: a3f5b8c91d2e
   Moun ki pale / Speaker: Marie Duval
   Sèks / Gender: female
   Rejyon / Region: Port-au-Prince
   Rating: ⭐⭐⭐⭐⭐ (5.0)
   Itilize / Used: 12 fwa / times
   Fichye / File: a3f5b8c91d2e.mp3
   Tèks preview: Bonjou zanmi! Kijan ou ye...
```

### **Voir les statistiques:**

Option **3** du menu principal.

```
📊 ESTATISTIK VWA / VOICE STATISTICS
============================================================

Total vwa / Total voices: 3
Total tan / Total duration: 5.2 minit / minutes
Total gwosè / Total size: 12.3 MB
Rating mwayen / Average rating: 4.5 ⭐
Pi itilize / Most used: Marie_Creole_Story
```

---

## 🔧 Utilisation dans l'Application

### **Automatique:**

Quand vous générez un audiobook, l'application peut utiliser vos voix personnalisées!

### **Dans le Code:**

```python
from src.custom_voice_manager import CustomVoiceManager

# Initialize manager
voice_manager = CustomVoiceManager()

# List available voices
voices = voice_manager.list_voices(language='ht')

# Get best voice for text
best_voices = voice_manager.get_best_voice_for_text(
    "Bonjou! Kijan ou ye?"
)

# Get voice audio path
voice_path = voice_manager.get_voice_path(voice_id)
```

### **Dans Streamlit:**

1. Lancez l'app: `streamlit run app.py`
2. Sidebar → **🎙️ Custom Voices**
3. Voyez toutes vos voix
4. Écoutez les exemples
5. Gérez votre collection

---

## 💡 Conseils pour de Meilleures Voix

### **Qualité d'Enregistrement:**

1. **Environnement calme**
   - Fermez portes et fenêtres
   - Éteignez ventilateurs/climatisation
   - Évitez heures de pointe

2. **Technique de voix**
   - Échauffez votre voix d'abord
   - Buvez de l'eau (pas froide)
   - Respirez correctement
   - Articulez clairement

3. **Position du micro**
   - 15-20 cm de votre bouche
   - Légèrement de côté (évite "pop" sounds)
   - Même distance pendant l'enregistrement

### **Édition Audio (Optionnel):**

Utilisez Audacity (gratuit) pour:
- 🔇 Réduire le bruit de fond (Noise Reduction)
- 📈 Normaliser le volume (Normalize)
- ✂️ Couper silences début/fin (Trim)
- 🎚️ Compression pour son uniforme (Compressor)

### **Types de Contenu:**

#### **Voix de Narration:**
- Histoires
- Livres
- Articles
- Nouvelles

**Style:** Claire, expressive, avec intonation

#### **Voix Éducative:**
- Leçons
- Tutoriels
- Explications

**Style:** Patient, clair, rythme modéré

#### **Voix Conversationnelle:**
- Dialogues
- Interviews
- Discussions

**Style:** Naturel, spontané, varié

---

## 📂 Structure des Fichiers

### **Dossier custom_voices/:**

```
custom_voices/
├── voices_metadata.json       # Métadonnées de toutes les voix
├── a3f5b8c91d2e.mp3          # Fichier audio voix 1
├── b2d4c6e8f1a3.mp3          # Fichier audio voix 2
└── c1e3f5a7b9d2.wav          # Fichier audio voix 3
```

### **Métadonnées (voices_metadata.json):**

```json
{
  "a3f5b8c91d2e": {
    "voice_id": "a3f5b8c91d2e",
    "voice_name": "Marie_Creole_Story",
    "speaker_name": "Marie Duval",
    "text_content": "Bonjou zanmi! Kijan ou ye...",
    "language": "ht",
    "gender": "female",
    "age_range": "adult",
    "region": "Port-au-Prince",
    "audio_file": "a3f5b8c91d2e.mp3",
    "duration_seconds": 45.3,
    "file_size_mb": 1.2,
    "rating": 5.0,
    "times_used": 12,
    "added_date": "2025-10-16T17:30:00"
  }
}
```

---

## 🔐 Sauvegarde et Partage

### **Sauvegarder vos voix:**

```powershell
# Copier tout le dossier
cp -r custom_voices custom_voices_backup

# Ou archiver
Compress-Archive -Path custom_voices -DestinationPath custom_voices_backup.zip
```

### **Partager avec d'autres:**

1. Copiez le dossier `custom_voices/`
2. Partagez avec collègues/amis
3. Ils copient dans leur projet
4. Voix automatiquement disponibles!

### **Exporter le catalogue:**

```python
from src.custom_voice_manager import CustomVoiceManager

manager = CustomVoiceManager()
manager.export_voice_catalog(Path("voice_catalog.json"))
```

---

## ❓ FAQ

### **Q: Quelle est la meilleure qualité pour les enregistrements?**

**R:** MP3 à 192 kbps, 44100 Hz. C'est un bon équilibre entre qualité et taille de fichier.

### **Q: Combien de voix puis-je ajouter?**

**R:** Illimité! L'espace disque est la seule limite.

### **Q: Puis-je supprimer une voix?**

**R:** Oui, utilisez la fonction `delete_voice()` ou supprimez manuellement le fichier du dossier.

### **Q: Les voix fonctionnent-elles hors ligne?**

**R:** Oui! Une fois ajoutées, elles sont stockées localement.

### **Q: Puis-je utiliser des voix de différentes régions?**

**R:** Absolument! C'est encouragé pour la diversité.

### **Q: Quelle longueur d'enregistrement?**

**R:** De 5 secondes à plusieurs minutes. Courts = meilleurs pour matching.

### **Q: Puis-je enregistrer avec mon téléphone?**

**R:** Oui! La plupart des smartphones modernes ont d'excellents microphones.

---

## 🎯 Exemples de Textes à Enregistrer

### **Phrases Courtes (Débutant):**

```
Bonjou! Kijan ou ye?
Mwen byen, mèsi.
Kilè ou prale?
Mwen renmen Ayiti.
Sa a se yon liv enteresan.
```

### **Paragraphes (Intermédiaire):**

```
Ayiti se yon bèl peyi ki sitye nan Karayib la. 
Li gen yon kilti rich ak yon istwa pwisan. 
Kreyòl ayisyen se lang tout moun pale. 
Se yon lang ki gen anpil ekspresyon epi ki rich anpil.
```

### **Histoires (Avancé):**

```
Te gen yon jou, yon ti fi ki te rele Marie. 
Li te renmen ale lekòl chak jou. 
Youn nan bagay li te pi renmen se lè l ap li liv. 
Li te konn li istwa sou zansèt li yo, 
sou kijan yo te batay pou libète Ayiti.
```

---

## 🌟 Projets Communautaires

### **Idées pour enrichir la plateforme:**

1. **Bibliothèque de voix régionales**
   - Différents accents d'Haïti
   - Voix de différents âges
   - Styles variés

2. **Voix thématiques**
   - Religieux
   - Éducatif
   - Storytelling
   - Actualités

3. **Collaboration**
   - Partagez vos meilleures voix
   - Créez une collection communautaire
   - Ratings et feedback

---

## 📞 Support et Ressources

### **Documentation:**
- `CUSTOM_VOICE_GUIDE.md` (ce fichier)
- `src/custom_voice_manager.py` (code source)
- `add_custom_voice.py` (outil interactif)

### **Outils recommandés:**
- **Audacity:** https://www.audacityteam.org/
- **OBS Studio:** Pour enregistrement vidéo + audio
- **Online Voice Recorder:** https://online-voice-recorder.com/

### **Ressources créoles:**
- Orthographe: https://www.haitianrevolution.com/creole-grammar/
- Dictionnaire: http://www.haitiancreole.org/

---

## ✅ Checklist

Avant d'enregistrer:
- [ ] Micro testé et fonctionnel
- [ ] Environnement calme
- [ ] Texte préparé et relu
- [ ] Verre d'eau à proximité
- [ ] Logiciel d'enregistrement prêt

Après enregistrement:
- [ ] Fichier sauvegardé
- [ ] Qualité vérifiée (écoutez)
- [ ] Texte transcrit exactement
- [ ] Métadonnées préparées
- [ ] Ajouté via `add_custom_voice.py`

---

**Fèt ak ❤️ pou kominote Kreyòl Ayisyen 🇭🇹**

**Kreye liv odyo nan vwa natirèl!** 🎙️✨

**Bon anrejistreman! / Happy recording!**

