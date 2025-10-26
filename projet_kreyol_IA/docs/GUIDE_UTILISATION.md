# 🇭🇹 Guide d'Utilisation - Pwojè Kreyòl IA

## 🎯 Vue d'ensemble

Ce projet vous permet de traduire des documents en **créole haïtien** et de générer des **audiobooks** avec une vraie voix créole native grâce à Hugging Face.

---

## 🚀 Démarrage Rapide

### **Option 1 : Traduction Complète (Recommandé)**

Double-cliquez sur : **`TRADUCTION_COMPLETE.bat`**

Ce script fait **tout automatiquement** :
1. ✅ Crée un document de test
2. ✅ Le traduit en créole haïtien
3. ✅ Génère l'audiobook avec voix native

**Durée totale :** ~3-5 minutes

---

### **Option 2 : Étape par Étape**

#### **Étape 1 : Traduire un document**

```batch
# Pour un fichier texte
python traduire_texte.py data/mon_document.txt

# Pour un fichier PDF
python traduire_document.py data/mon_document.pdf
```

**Résultat :**
- `output/mon_document/mon_document_original.txt`
- `output/mon_document/mon_document_kreyol.txt`

#### **Étape 2 : Créer l'audiobook**

```batch
python generer_audio_huggingface.py output/mon_document/mon_document_kreyol.txt
```

**Résultat :**
- `output/mon_document/mon_document_audio_hf.mp3` (Voix créole native 🇭🇹)

---

## 📊 Comparaison des Technologies

### **Traduction**

| Méthode | Qualité | Vitesse | Offline |
|---------|---------|---------|---------|
| **Hugging Face M2M100** ⭐ | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Moyen | ✅ Oui |
| Google Translator (deep-translator) | ⭐⭐⭐ Bon | ⭐⭐⭐⭐⭐ Rapide | ❌ Non |

### **Text-to-Speech (Audiobook)**

| Méthode | Qualité | Accent | Offline |
|---------|---------|--------|---------|
| **Hugging Face MMS-TTS** ⭐ | ⭐⭐⭐⭐⭐ | 🇭🇹 Créole natif | ✅ Oui |
| gTTS (Google) | ⭐⭐⭐ | 🇫🇷 Français | ❌ Non |

---

## 🎧 Modèles Hugging Face Utilisés

### **1. Traduction : facebook/m2m100_418M**
- 🌍 Supporte 100+ langues dont le créole haïtien
- 💾 Taille : ~1.5 GB
- 🎯 Spécialement entraîné pour les langues sous-représentées
- 📥 Se télécharge automatiquement au premier usage

### **2. Text-to-Speech : facebook/mms-tts-hat**
- 🗣️ Voix créole haïtienne native
- 💾 Taille : ~145 MB
- 🎵 Qualité audio : 16 kHz
- ⚡ Génération : ~3 secondes par phrase
- 📥 Se télécharge automatiquement au premier usage

---

## 📁 Structure des Fichiers

```
projet_kreyol_IA/
│
├── 🎯 SCRIPTS RAPIDES
│   ├── TRADUCTION_COMPLETE.bat      # Tout-en-un
│   ├── CREER_AUDIOBOOK.bat          # Audiobook uniquement
│   └── TRADUIRE.bat                 # Traduction uniquement
│
├── 📝 SCRIPTS PYTHON
│   ├── traduire_texte.py            # Traduction de fichiers texte
│   ├── traduire_document.py         # Traduction de PDF
│   ├── generer_audio_huggingface.py # Audiobook avec voix native ⭐
│   └── generer_audio.py             # Audiobook avec gTTS (fallback)
│
├── 📂 DOSSIERS
│   ├── data/                        # Vos documents sources
│   ├── output/                      # Fichiers générés
│   └── cache/                       # Cache de traduction
│
└── 📚 DOCUMENTATION
    ├── GUIDE_UTILISATION.md         # Ce fichier
    ├── ABOUT.md                     # À propos du projet
    └── README.md                    # Documentation complète
```

---

## 💡 Conseils et Astuces

### **Pour de meilleures traductions :**
1. ✅ Utilisez des textes clairs et bien formatés
2. ✅ Divisez les longs documents en chapitres
3. ✅ Vérifiez l'encodage UTF-8 de vos fichiers

### **Pour de meilleurs audiobooks :**
1. ✅ Utilisez `generer_audio_huggingface.py` pour la voix native
2. ✅ Les phrases courtes donnent de meilleurs résultats
3. ✅ Ajoutez de la ponctuation pour des pauses naturelles

### **Optimisation des performances :**
1. 💾 Le cache évite de retraduire les mêmes textes
2. 🔄 Les modèles se chargent une seule fois
3. ⚡ Première utilisation : téléchargement des modèles (~5-10 min)
4. ⚡ Utilisations suivantes : beaucoup plus rapides!

---

## 🆘 Dépannage

### **Problème : "ModuleNotFoundError"**
```batch
pip install transformers torch torchaudio scipy gtts deep-translator
```

### **Problème : "Model not found"**
- Les modèles se téléchargent automatiquement
- Vérifiez votre connexion Internet pour le premier usage
- Emplacement : `C:\Users\[VotreNom]\.cache\huggingface\`

### **Problème : Audio de mauvaise qualité**
- Utilisez `generer_audio_huggingface.py` au lieu de `generer_audio.py`
- Le modèle Hugging Face donne une voix créole authentique

### **Problème : Traduction lente**
- Normal lors du premier usage (chargement du modèle)
- Utilisez `deep-translator` pour plus de rapidité :
  ```python
  # Dans traduire_texte.py, c'est déjà configuré pour être rapide
  ```

---

## 🌟 Exemples d'Utilisation

### **Exemple 1 : Livre pour enfants**
```batch
python traduire_document.py "data/histoire_enfants.pdf"
python generer_audio_huggingface.py "output/histoire_enfants/histoire_enfants_kreyol.txt"
```

### **Exemple 2 : Document éducatif**
```batch
python traduire_texte.py "data/cours_math.txt"
python generer_audio_huggingface.py "output/cours_math/cours_math_kreyol.txt"
```

### **Exemple 3 : Article de blog**
```batch
# Copier votre texte dans data/article.txt
python traduire_texte.py "data/article.txt"
python generer_audio_huggingface.py "output/article/article_kreyol.txt"
```

---

## 📊 Statistiques du Projet

### **Ce qui a été créé pour vous :**

✅ **6 scripts automatisés** (.bat)  
✅ **5 scripts Python** optimisés  
✅ **Intégration Hugging Face** complète  
✅ **Voix créole native** 🇭🇹  
✅ **Système de cache** intelligent  
✅ **Documentation** complète  

### **Résultat de la démo :**

📄 **Document original** : 1,378 caractères (216 mots français)  
🇭🇹 **Traduction créole** : 1,139 caractères (241 mots créoles)  
🎧 **Audiobook** : 88 secondes (~1.5 minutes), 539 Ko  
⏱️ **Temps total** : ~3 minutes  

---

## 🎉 Félicitations!

Vous avez maintenant un système complet de traduction et génération d'audiobooks en créole haïtien, propulsé par l'IA de Hugging Face!

### **Points forts de votre système :**

1. ✨ **Voix créole authentique** - Grâce à facebook/mms-tts-hat
2. 🚀 **Traduction de qualité** - Avec facebook/m2m100
3. 💾 **Fonctionne offline** - Après le premier téléchargement
4. 🔄 **Cache intelligent** - Évite les retraitements
5. 🎯 **Scripts automatisés** - Tout en un clic!

---

## 📞 Support et Ressources

- 📚 **Hugging Face Models** : https://huggingface.co/facebook
- 🇭🇹 **Documentation M2M100** : https://huggingface.co/facebook/m2m100_418M
- 🎤 **Documentation MMS-TTS** : https://huggingface.co/facebook/mms-tts-hat

---

**Bon tradiksyon! / Happy translating!** 🇭🇹

