# 🚀 Guide de Déploiement sur Render.com

## 📋 Pré-requis

- ✅ Compte GitHub (gratuit)
- ✅ Compte Render.com (gratuit)
- ✅ Votre code dans ce dossier

---

## 🎯 Étape 1: Préparer le Code

Votre code est déjà prêt! Les fichiers suivants ont été créés:

- ✅ `render.yaml` - Configuration Render
- ✅ `requirements.txt` - Dépendances Python
- ✅ `runtime.txt` - Version Python
- ✅ `Procfile` - Commande de démarrage
- ✅ `.gitignore` - Fichiers à ignorer

---

## 🔧 Étape 2: Créer un Repository GitHub

### Option A: Via GitHub Desktop (Facile)

1. **Téléchargez GitHub Desktop**: https://desktop.github.com/
2. **Ouvrez GitHub Desktop**
3. **File > Add Local Repository**
4. **Sélectionnez le dossier**: `projet_kreyol_IA`
5. **Create Repository**
6. **Publish repository** (cochez "Keep this code private" si vous voulez)

### Option B: Via Ligne de Commande

```bash
cd "C:\Users\Fanerlink\OneDrive\Documents\liv odyo\projet_kreyol_IA"

# Initialiser Git (si pas déjà fait)
git init

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit - Kreyòl IA Studio"

# Créer le repository sur GitHub (suivez les instructions sur github.com)
# Puis:
git remote add origin https://github.com/VOTRE_USERNAME/kreyol-ia.git
git branch -M main
git push -u origin main
```

---

## 🌐 Étape 3: Déployer sur Render

### 3.1 Créer un Compte

1. Allez sur **https://render.com**
2. Cliquez **"Get Started for Free"**
3. Connectez-vous avec **GitHub**

### 3.2 Créer le Service Web

1. **Dashboard Render** > **"New +"** > **"Web Service"**

2. **Connecter le Repository**:
   - Cliquez **"Connect GitHub"**
   - Sélectionnez votre repository `kreyol-ia`
   - Cliquez **"Connect"**

3. **Configuration** (Render détecte automatiquement render.yaml):
   
   Si auto-détecté:
   - ✅ Vérifiez que tout est correct
   - ✅ Cliquez **"Create Web Service"**
   
   Si manuel:
   ```
   Name: kreyol-ia-studio
   Region: Oregon (US West)
   Branch: main
   Runtime: Python 3
   Build Command: pip install --upgrade pip && pip install -r requirements.txt
   Start Command: uvicorn api_final:app --host 0.0.0.0 --port $PORT
   Plan: Free
   ```

4. **Variables d'Environnement** (optionnel):
   - Cliquez **"Advanced"**
   - Ajoutez si nécessaire:
     ```
     PYTHON_VERSION=3.11.0
     ```

5. **Cliquez "Create Web Service"** 🚀

### 3.3 Attendre le Déploiement

- ⏳ Render va:
  1. Cloner votre code
  2. Installer les dépendances
  3. Démarrer l'application
  
- 📊 Suivez les logs en temps réel
- ⏱️ Durée: 5-10 minutes (première fois)

### 3.4 Votre App est Live! 🎉

Votre URL sera quelque chose comme:
```
https://kreyol-ia-studio.onrender.com
```

---

## 🎨 Étape 4: Tester l'Application

1. **Ouvrez l'URL** fournie par Render
2. **Testez les fonctionnalités**:
   - ✅ Page d'accueil (Studio)
   - ✅ Text to Speech
   - ✅ Créer un audiobook
   - ✅ Créer un podcast
3. **Vérifiez les logs** si problème

---

## 🔄 Étape 5: Mises à Jour Automatiques

Une fois configuré, **chaque push sur GitHub** déploiera automatiquement:

```bash
# Faire des modifications
git add .
git commit -m "Amélioration de l'interface"
git push

# Render détecte et redéploie automatiquement! 🎉
```

---

## 📦 Étape 6: Ajouter du Stockage (Optionnel)

Pour sauvegarder les fichiers audio générés:

1. **Render Dashboard** > Votre service
2. **Aller à "Disks"**
3. **Cliquez "Add Disk"**:
   ```
   Name: kreyol-audio-storage
   Mount Path: /opt/render/project/src/output
   Size: 1 GB (gratuit)
   ```
4. **Sauvegarder**

---

## 🐛 Dépannage

### Problème: Build échoue

**Solution 1**: Vérifier requirements.txt
```bash
# Testez localement d'abord:
pip install -r requirements.txt
```

**Solution 2**: Vérifier la version Python
- Render utilise Python 3.11 par défaut
- Vérifiez `runtime.txt`

### Problème: App ne démarre pas

**Vérifiez**:
1. Les logs Render (onglet "Logs")
2. Que `api_final.py` existe
3. Que le port $PORT est utilisé

**Solution**:
```python
# Dans api_final.py, à la fin:
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### Problème: Modèles IA trop volumineux

**Solution**: Télécharger au démarrage
```python
# Au début de api_final.py
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model_name = "facebook/m2m100_418M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
```

---

## 💰 Limites du Plan Gratuit

**Render Free Tier**:
- ✅ 750 heures/mois
- ✅ 512 MB RAM
- ✅ 0.1 CPU
- ✅ SSL gratuit
- ⚠️ Sleep après 15min d'inactivité
- ⚠️ Build 500 minutes/mois

**Conseils**:
- L'app dort après 15min → premier chargement lent
- Upgrade à $7/mois pour éviter le sleep
- Utilisez un "ping service" pour garder l'app active

---

## 🚀 Améliorer les Performances

### 1. Optimiser les Modèles

```python
# Utiliser des modèles plus légers
model_name = "facebook/m2m100_418M"  # Au lieu de 1.2B
```

### 2. Mettre en Cache

```python
# Cache les traductions
import functools

@functools.lru_cache(maxsize=100)
def traduire_texte(texte: str) -> str:
    # ...
```

### 3. Compression des Fichiers

```python
# Compresser les MP3
quality = "64k"  # Au lieu de 192k
```

---

## 🎯 Checklist Finale

Avant de déployer:

- [ ] Code testé localement
- [ ] Repository GitHub créé
- [ ] Fichiers de config présents
- [ ] .gitignore configuré
- [ ] Secrets/tokens pas dans le code
- [ ] README à jour

Après déploiement:

- [ ] URL fonctionne
- [ ] Toutes les pages chargent
- [ ] API répond correctement
- [ ] Audio se génère
- [ ] Logs sans erreur

---

## 📞 Support

**Render Documentation**: https://render.com/docs
**Status Page**: https://status.render.com
**Community**: https://community.render.com

**Problèmes?** Vérifiez:
1. Logs Render (onglet Logs)
2. Events (onglet Events)
3. Health Check (doit retourner 200)

---

## 🎉 Félicitations!

Votre **Kreyòl IA Studio** est maintenant en ligne et accessible partout dans le monde! 🌍🇭🇹

**Partagez votre URL** avec des utilisateurs pour tester!

---

## 📈 Prochaines Étapes

1. **Domaine Custom**: 
   - Render permet d'ajouter votre domaine (ex: kreyol-ia.com)
   - Settings > Custom Domain

2. **Monitoring**:
   - Render fournit des métriques gratuites
   - CPU, RAM, requêtes, etc.

3. **Scaling**:
   - Upgrade au Starter ($7/mois) quand nécessaire
   - Plus de RAM, pas de sleep

4. **CDN**:
   - Render a un CDN intégré
   - Vos fichiers statiques sont automatiquement cachés

---

**Besoin d'aide?** N'hésitez pas à demander! 🚀

