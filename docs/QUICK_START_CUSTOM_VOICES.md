# 🚀 Démarrage Rapide - Voix Personnalisées

## En 3 Minutes! ⏱️

---

## 🎙️ Ajouter Votre Première Voix

### **Étape 1: Préparer**

Vous avez besoin de:
1. ✅ Un fichier audio (MP3, WAV, etc.)
2. ✅ Le texte qui est dit dans l'audio

### **Étape 2: Lancer l'outil**

```powershell
cd "C:\Users\Fanerlink\OneDrive\Documents\liv odyo\projet_kreyol_IA"
.\venv\Scripts\Activate.ps1
python add_custom_voice.py
```

### **Étape 3: Suivre les instructions**

L'outil vous guide en créole et en anglais!

```
🎙️  AJOUTE YON VWA NATIRÈL / ADD A NATURAL VOICE
============================================================

1. Ajoute yon vwa / Add a voice  ← Choisissez 1
2. Wè tout vwa / List all voices
3. Estatistik / Statistics
4. Kite / Exit

Chwazi / Choose (1-4): 1
```

### **Étape 4: Remplir les infos**

```
📁 Chemen fichye odyo / Audio file path: 
C:\Users\...\ma_voix.mp3

Non vwa a / Voice name [Voice_1]: 
Ma_Premiere_Voix

Non moun ki pale a / Speaker name [Anonymous]: 
Jean Dupont

📄 Tèks ki te di / Text that was spoken:
Bonjou! Kijan ou ye jodi a?
END
```

### **Étape 5: Confirmer**

```
✅ Ajoute vwa sa a? / Add this voice? (yes/no) [yes]: 
yes
```

### **Étape 6: Succès! 🎉**

```
✅ SIKSÈ / SUCCESS!
Vwa ajoute avèk siksè / Voice added successfully!
ID: a3f5b8c91d2e
```

---

## 👀 Voir Vos Voix

### **Dans le Terminal:**

```powershell
python add_custom_voice.py
# Choisissez option 2
```

### **Dans l'Application Web:**

```powershell
streamlit run app.py
```

Allez dans **Sidebar → 🎙️ Custom Voices**

---

## 🎯 Exemple Complet

### **Scénario: Ajouter une voix de narration**

1. **Enregistrez-vous** en lisant:
   ```
   Bonjou zanmi! Kijan ou ye jodi a?
   Mwen espere ou pase yon bon jounen.
   Se mwen ki pral li istwa sa a pou ou.
   ```

2. **Sauvegardez** comme `narration.mp3`

3. **Lancez** `python add_custom_voice.py`

4. **Entrez:**
   - Fichier: `C:\...\narration.mp3`
   - Nom: `Narration_Creole_1`
   - Speaker: `Votre nom`
   - Texte: (copiez le texte ci-dessus)
   - Sexe: `female` ou `male`
   - Âge: `adult`
   - Région: `Haiti`

5. **Confirmez!**

6. **Utilisez** dans vos audiobooks!

---

## 💡 Conseils Rapides

### **Pour un bon enregistrement:**
- 🎤 Parlez clairement
- 🏠 Endroit calme
- 📏 15-20 cm du micro
- 💧 Buvez de l'eau avant
- 🎵 Testez d'abord!

### **Format idéal:**
- MP3, 192 kbps
- 44100 Hz
- Durée: 10-60 secondes

### **Texte:**
- Orthographe créole correcte
- Ponctuation claire
- Exactement ce qui est dit

---

## 🆘 Problèmes?

### **Erreur: Fichier non trouvé**
→ Vérifiez le chemin complet du fichier

### **Erreur: Format non supporté**
→ Convertissez en MP3 avec Audacity

### **Pas de son à la lecture**
→ Vérifiez le volume, testez avec un autre lecteur

---

## 📚 Documentation Complète

Pour plus de détails, consultez:
- **CUSTOM_VOICE_GUIDE.md** - Guide complet
- **src/custom_voice_manager.py** - Code source

---

**C'est tout! Vous êtes prêt! 🎉**

**Ale kreye liv odyo ak vwa natirèl! 🎙️✨**

