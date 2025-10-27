# 🎵 Nouvelles Fonctionnalités Musicales - Faner Studio

## Vue d'ensemble

Faner Studio intègre maintenant un **générateur de musique IA** et un **éditeur audio professionnel** avec des fonctionnalités spécialement conçues pour la musique haïtienne.

---

## 🎼 Générateur de Musique IA

### Styles Musicaux Disponibles

Le générateur supporte **6 styles musicaux haïtiens** :

| Style | BPM | Description | Instruments |
|-------|-----|-------------|-------------|
| **Konpa** | 120 | Style konpa traditionnel pour danser | Basse, batterie, guitare, clavier |
| **Rara** | 140 | Ambiance festive de rue | Batterie, trompette, bambou, vocaux |
| **Racine** | 100 | Musique roots authentique | Batterie, basse, vocaux, percussion |
| **Twoubadou** | 90 | Musique folk traditionnelle | Guitare, maracas, vocaux |
| **Zouk** | 130 | Style zouk moderne | Basse, batterie, synthé, guitare |
| **Rap Kreyòl** | 95 | Beats pour rap en créole | Basse, batterie, synthé |

### Fonctionnalités

#### 1. Génération de Musique Complète
```python
from src.music_generator import HaitianMusicGenerator

generator = HaitianMusicGenerator()
music_path = generator.generate_music(
    style='konpa',
    duration=30,  # secondes
    add_melody=True,
    add_bass=True,
    add_drums=True
)
```

**API Endpoint:**
```bash
POST /api/music/generate
{
  "style": "konpa",
  "duration": 30,
  "add_melody": true,
  "add_bass": true,
  "add_drums": true
}
```

#### 2. Création de Beats
```python
beat_path = generator.create_beat(
    style='rap_kreyol',
    bars=8  # nombre de mesures
)
```

**API Endpoint:**
```bash
POST /api/music/beat
{
  "style": "rap_kreyol",
  "bars": 8
}
```

#### 3. Mixage Voix + Musique
```python
mixed_path = generator.mix_music_with_voice(
    voice_path='mon_enregistrement.mp3',
    style='konpa',
    music_volume=-20  # dB
)
```

**API Endpoint:**
```bash
POST /api/music/mix
# FormData avec:
# - voice_file: fichier audio
# - style: style musical
# - music_volume: volume de la musique
```

#### 4. Templates Prédéfinis
6 templates prêts à utiliser :
- **Konpa Dance** - 120 BPM, 3 minutes
- **Rara Festival** - 140 BPM, 4 minutes
- **Racine Roots** - 100 BPM, 3m20
- **Rap Kreyòl Beat** - 95 BPM, 3 minutes
- **Twoubadou Folk** - 90 BPM, 2m30
- **Zouk Love** - 130 BPM, 3m30

**API Endpoint:**
```bash
GET /api/music/templates
POST /api/music/generate-from-template/konpa_dance
```

---

## 🎛️ Éditeur Audio Professionnel

### Effets Disponibles

#### 1. Normalisation
Ajuste le volume audio à un niveau cible.
```python
from src.audio_editor import AudioEditor

editor = AudioEditor()
normalized = editor.normalize_audio(
    'input.mp3',
    target_dbfs=-20.0
)
```

#### 2. Compression Dynamique
Réduit l'écart entre les sons forts et faibles.
```python
compressed = editor.apply_compression(
    'input.mp3',
    threshold=-20.0,
    ratio=4.0
)
```

#### 3. Égalisation (3 bandes)
Ajuste basses, médiums et aigus.
```python
equalized = editor.apply_eq(
    'input.mp3',
    bass_gain=2.0,
    mid_gain=0.0,
    treble_gain=-1.0
)
```

#### 4. Réverbération
Ajoute un effet d'espace.
```python
reverb = editor.apply_reverb(
    'input.mp3',
    room_size=0.5,
    damping=0.5
)
```

#### 5. Fondus (Fade In/Out)
```python
faded = editor.apply_fade(
    'input.mp3',
    fade_in_ms=1000,
    fade_out_ms=1000
)
```

#### 6. Changement de Vitesse
```python
faster = editor.change_speed(
    'input.mp3',
    speed_factor=1.5  # 1.5x plus rapide
)
```

#### 7. Changement de Hauteur (Pitch)
```python
pitched = editor.change_pitch(
    'input.mp3',
    semitones=2  # +2 demi-tons
)
```

### Presets Professionnels

4 presets optimisés pour différents usages :

#### 1. Preset **Podcast**
- Normalisation à -16 dBFS
- Compression (seuil: -20dB, ratio: 3:1)
- EQ : +2dB basses, +1dB médiums, -1dB aigus

```python
from src.audio_editor import apply_preset

processed = apply_preset('input.mp3', 'podcast')
```

#### 2. Preset **Music**
- Normalisation à -14 dBFS
- EQ : +3dB basses, 0dB médiums, +2dB aigus
- Compression (seuil: -18dB, ratio: 2.5:1)

#### 3. Preset **Voice**
- Normalisation à -18 dBFS
- EQ : -2dB basses, +3dB médiums, +1dB aigus
- Compression (seuil: -22dB, ratio: 4:1)

#### 4. Preset **Radio**
- Normalisation à -16 dBFS
- Compression forte (seuil: -18dB, ratio: 5:1)
- EQ : -3dB basses, +4dB médiums, +2dB aigus

**API Endpoint:**
```bash
POST /api/audio-editor/preset/podcast
# Avec fichier audio en multipart/form-data
```

### Effets Multiples
Appliquez plusieurs effets en séquence :
```python
effects = [
    {'type': 'normalize', 'params': {'target_dbfs': -16.0}},
    {'type': 'compression', 'params': {'threshold': -20.0, 'ratio': 3.0}},
    {'type': 'eq', 'params': {'bass_gain': 2.0}},
    {'type': 'reverb', 'params': {'room_size': 0.3}}
]

result = editor.apply_multiple_effects('input.mp3', effects)
```

---

## 🖥️ Interface Utilisateur

### Accès
- **Interface complète** : `http://localhost:8000/pages/music_generator.html`
- **Page d'outils** : `http://localhost:8000/tools.html` (nouvelle section "Mizik & Editè")

### Fonctionnalités de l'Interface
- 🎨 Design moderne et réactif
- 🎵 Sélection visuelle des styles musicaux
- 🎚️ Contrôles intuitifs pour chaque paramètre
- 📊 Aperçu audio en temps réel
- ⬇️ Téléchargement direct des fichiers générés
- 📱 Compatible mobile et desktop

---

## 📋 API Endpoints

### Musique

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/music/styles` | Liste des styles disponibles |
| POST | `/api/music/generate` | Génère une piste musicale |
| POST | `/api/music/beat` | Crée un beat instrumental |
| POST | `/api/music/mix` | Mixe voix et musique |
| GET | `/api/music/templates` | Liste des templates |
| POST | `/api/music/generate-from-template/{id}` | Génère depuis un template |
| POST | `/api/music/quick-generate/{style}` | Génération rapide |
| GET | `/api/music/download?path={path}` | Télécharge un fichier |

### Éditeur Audio

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/audio-editor/normalize` | Normalise l'audio |
| POST | `/api/audio-editor/fade` | Applique des fondus |
| POST | `/api/audio-editor/compression` | Compresse l'audio |
| POST | `/api/audio-editor/eq` | Égalisation |
| POST | `/api/audio-editor/reverb` | Ajoute réverbération |
| POST | `/api/audio-editor/preset/{name}` | Applique un preset |
| GET | `/api/audio-editor/presets` | Liste des presets |
| POST | `/api/audio-editor/info` | Infos sur un fichier |
| GET | `/api/audio-editor/download?path={path}` | Télécharge un fichier |

---

## 🔧 Installation

### Dépendances Requises
Les nouvelles fonctionnalités nécessitent :
```bash
pip install pydub soundfile scipy numpy
```

### FFmpeg
**Important** : `pydub` nécessite FFmpeg pour le traitement audio.

**Windows:**
```bash
# Télécharger depuis: https://ffmpeg.org/download.html
# Ajouter au PATH système
```

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# Mac (avec Homebrew)
brew install ffmpeg
```

### Configuration
Aucune configuration supplémentaire nécessaire. Les nouvelles routes sont chargées automatiquement au démarrage de l'application.

---

## 🚀 Utilisation

### 1. Démarrer l'application
```bash
python app/main.py
```

Vous verrez :
```
✅ Music routes loaded!
🎵 NOUVELLES FONCTIONNALITÉS MUSICALES:
   • Générateur de musique: 6 styles
   • Éditeur audio: 5 effets
   • Presets: podcast, music, voice, radio
   • Interface: http://localhost:8000/music-generator
```

### 2. Accéder à l'interface
Ouvrez votre navigateur : `http://localhost:8000/pages/music_generator.html`

### 3. Générer de la musique
1. Choisissez un style (Konpa, Rara, etc.)
2. Réglez la durée
3. Sélectionnez les éléments (mélodie, basse, batterie)
4. Cliquez sur "Jenere Mizik"
5. Écoutez et téléchargez!

### 4. Éditer de l'audio
1. Uploadez votre fichier audio
2. Choisissez un preset ou des effets individuels
3. Appliquez et téléchargez le résultat

---

## 📝 Exemples de Code

### Exemple 1: Créer une piste Konpa de 60 secondes
```python
from src.music_generator import HaitianMusicGenerator

generator = HaitianMusicGenerator()
music = generator.generate_music(
    style='konpa',
    duration=60,
    output_path='ma_musique_konpa.mp3'
)
print(f"Musique créée: {music}")
```

### Exemple 2: Mixer un podcast avec de la musique Rara
```python
mixed = generator.mix_music_with_voice(
    voice_path='mon_podcast.mp3',
    style='rara',
    music_volume=-25
)
print(f"Podcast mixé: {mixed}")
```

### Exemple 3: Optimiser un enregistrement vocal
```python
from src.audio_editor import apply_preset

optimized = apply_preset(
    'enregistrement_brut.mp3',
    'voice'
)
print(f"Audio optimisé: {optimized}")
```

### Exemple 4: Créer une boucle de beat Rap
```python
generator = HaitianMusicGenerator()
beat = generator.create_beat(
    style='rap_kreyol',
    bars=16
)
print(f"Beat créé: {beat}")
```

---

## 🎯 Cas d'Usage

### 1. Production de Podcast
- Générer une intro musicale en style Konpa
- Mixer avec la voix du podcast
- Appliquer le preset "podcast" pour optimiser

### 2. Création de Contenu YouTube
- Créer une musique de fond unique
- Mixer avec narration
- Ajouter des effets (reverb, EQ)

### 3. Production Musicale
- Générer des beats pour rap en créole
- Créer des boucles instrumentales
- Éditer et optimiser les pistes

### 4. Radio/Streaming
- Produire des jingles en styles haïtiens variés
- Normaliser tous les contenus au même niveau
- Appliquer le preset "radio" pour un son uniforme

---

## 🐛 Dépannage

### Problème: "FFmpeg not found"
**Solution:** Installez FFmpeg et ajoutez-le au PATH système.

### Problème: "Module 'pydub' not found"
**Solution:** `pip install pydub soundfile scipy`

### Problème: Qualité audio faible
**Solution:** Les fichiers sont exportés en 192kbps MP3. Pour une meilleure qualité, modifiez le bitrate dans le code source.

### Problème: Génération lente
**Solution:** La première génération peut être plus lente. Les suivantes seront plus rapides.

---

## 🔮 Améliorations Futures

- [ ] Support de formats audio additionnels (FLAC, OGG)
- [ ] Plus de styles musicaux (Kadans, Méringue, etc.)
- [ ] Paramètres avancés pour personnalisation
- [ ] Intégration d'instruments réels (samples)
- [ ] Éditeur audio visuel (waveform)
- [ ] Support de plugins VST
- [ ] Séquenceur MIDI intégré
- [ ] Collaboration en temps réel

---

## 📄 License

Ces fonctionnalités font partie de Faner Studio et sont disponibles sous la même license que le projet principal.

---

## 🤝 Contribution

Les contributions sont les bienvenues! Domaines d'amélioration prioritaires:
- Nouveaux styles musicaux haïtiens
- Effets audio additionnels
- Optimisation des performances
- Tests unitaires

---

## 📞 Support

Pour toute question ou problème :
- 📧 Email: support@fanerstudio.com
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

---

**Fait avec ❤️ pour la communauté haïtienne** 🇭🇹

