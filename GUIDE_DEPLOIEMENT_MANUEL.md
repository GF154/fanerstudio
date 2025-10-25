# 🚀 GUIDE DE DÉPLOIEMENT MANUEL - RENDER.COM
# Guide Complet en Kreyòl Ayisyen

## 📋 PRÉREQUIS

### 1. Compte GitHub (gratis)
- Allez sur: https://github.com/signup
- Créez votre compte si vous n'en avez pas

### 2. Compte Render (gratis)
- Allez sur: https://render.com/register
- Inscrivez-vous avec GitHub (recommandé)

---

## 🗂️ ÉTAPE 1: CRÉER LE REPOSITORY GITHUB

### A. Créer un nouveau repository

1. Allez sur: https://github.com/new

2. Remplissez les informations:
   - **Repository name:** `kreyol-ia-deploy`
   - **Description:** "Kreyòl IA - Translation & TTS Platform"
   - **Visibility:** Public ✅
   - **Ne pas** initialiser avec README

3. Cliquez: **"Create repository"**

### B. Copier l'URL du repository

Vous verrez une URL comme:
```
https://github.com/VOTRE_USERNAME/kreyol-ia-deploy.git
```

**Notez cette URL!** Vous en aurez besoin.

---

## 📁 ÉTAPE 2: PRÉPARER LES FICHIERS LOCALEMENT

### A. Créer un nouveau dossier

```powershell
# Windows PowerShell
cd Documents
mkdir kreyol-ia-deploy
cd kreyol-ia-deploy
```

### B. Créer les fichiers essentiels

#### Fichier 1: `requirements.txt`

Créez un fichier nommé `requirements.txt` avec ce contenu:

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6
python-dotenv==1.0.0
httpx==0.26.0
```

#### Fichier 2: `main.py`

Créez un fichier nommé `main.py` avec ce contenu:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kreyòl IA - Ultra-Minimal API
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI(title="Kreyòl IA API", version="1.0")

@app.get("/")
def root():
    return {"status": "live", "message": "Kreyòl IA fonksyone!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/translate")
async def translate(text: str, target: str = "ht"):
    """NLLB Translation"""
    try:
        url = "https://api-inference.huggingface.co/models/facebook/nllb-200-distilled-600M"
        headers = {}
        key = os.getenv("HUGGINGFACE_API_KEY")
        if key:
            headers["Authorization"] = f"Bearer {key}"
        
        langs = {"en": "eng_Latn", "fr": "fra_Latn", "ht": "hat_Latn"}
        payload = {
            "inputs": text,
            "parameters": {
                "src_lang": "eng_Latn",
                "tgt_lang": langs.get(target, "hat_Latn")
            }
        }
        
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(url, json=payload, headers=headers)
            if r.status_code == 200:
                result = r.json()
                translated = result[0]["translation_text"] if isinstance(result, list) else text
                return {"success": True, "original": text, "translated": translated}
            else:
                return {"success": False, "error": "API error", "original": text}
    except Exception as e:
        return {"success": False, "error": str(e), "original": text}
```

#### Fichier 3: `Procfile`

Créez un fichier nommé `Procfile` (sans extension) avec ce contenu:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### Fichier 4: `runtime.txt`

Créez un fichier nommé `runtime.txt` avec ce contenu:

```
python-3.11.0
```

---

## 🔄 ÉTAPE 3: POUSSER LE CODE VERS GITHUB

### A. Initialiser Git

```powershell
git init
git add .
git commit -m "Initial commit: Kreyòl IA minimal setup"
```

### B. Connecter au repository GitHub

Remplacez `VOTRE_USERNAME` par votre nom d'utilisateur GitHub:

```powershell
git remote add origin https://github.com/VOTRE_USERNAME/kreyol-ia-deploy.git
git branch -M main
git push -u origin main
```

**Si on vous demande de vous connecter:**
- Username: Votre nom d'utilisateur GitHub
- Password: Utilisez un **Personal Access Token** (pas votre mot de passe)

### C. Créer un Personal Access Token (si nécessaire)

1. Allez sur: https://github.com/settings/tokens
2. Cliquez: **"Generate new token (classic)"**
3. Nom: "Render Deployment"
4. Permissions: Cochez **"repo"**
5. Cliquez: **"Generate token"**
6. **Copiez le token immédiatement!** (Vous ne pourrez plus le voir)

Utilisez ce token comme mot de passe lors du push.

---

## 🌐 ÉTAPE 4: DÉPLOYER SUR RENDER

### A. Connexion à Render

1. Allez sur: https://dashboard.render.com
2. Connectez-vous avec votre compte

### B. Créer un nouveau Web Service

1. Cliquez: **"New +"** → **"Web Service"**

2. Connectez votre repository GitHub:
   - Cliquez: **"Connect account"** (si pas déjà fait)
   - Autorisez Render à accéder à GitHub
   - Sélectionnez votre repository: `kreyol-ia-deploy`

3. Configurez le service:

   **Name:** `kreyol-ia`
   
   **Region:** Oregon (US West) ou le plus proche
   
   **Branch:** `main`
   
   **Root Directory:** (laissez vide)
   
   **Runtime:** Python 3
   
   **Build Command:**
   ```bash
   pip install --upgrade pip && pip install -r requirements.txt
   ```
   
   **Start Command:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
   
   **Plan:** Free ✅

4. Variables d'environnement (optionnel):
   
   Cliquez: **"Add Environment Variable"**
   
   **Key:** `HUGGINGFACE_API_KEY`
   **Value:** (votre clé API Hugging Face)
   
   *Pour obtenir une clé:*
   - Allez sur: https://huggingface.co/settings/tokens
   - Créez un token "Read"
   - Copiez et collez ici

5. Cliquez: **"Create Web Service"**

### C. Attendre le déploiement

Le déploiement prendra environ **2 minutes**.

Vous verrez:
```
==> Building...
==> Installing dependencies...
==> Starting service...
==> Your service is live!
```

---

## ✅ ÉTAPE 5: TESTER VOTRE API

### A. URL de votre service

Render vous donnera une URL comme:
```
https://kreyol-ia.onrender.com
```

### B. Tester les endpoints

**1. Root endpoint:**
```
GET https://kreyol-ia.onrender.com/
```

Réponse attendue:
```json
{
  "status": "live",
  "message": "Kreyòl IA fonksyone!"
}
```

**2. Health check:**
```
GET https://kreyol-ia.onrender.com/health
```

Réponse attendue:
```json
{
  "status": "healthy"
}
```

**3. Documentation API:**
```
https://kreyol-ia.onrender.com/docs
```

Vous verrez l'interface Swagger UI complète!

**4. Tester la traduction:**

Dans Swagger UI:
- Cliquez sur `POST /translate`
- Cliquez "Try it out"
- Paramètres:
  - `text`: "Hello, how are you?"
  - `target`: "ht"
- Cliquez "Execute"

Réponse attendue:
```json
{
  "success": true,
  "original": "Hello, how are you?",
  "translated": "Bonjou, kòman ou ye?"
}
```

---

## 🔧 DÉPANNAGE

### Problème 1: "Deploy failed"

**Solution:**
1. Cliquez sur le deploy failed
2. Lisez les logs d'erreur
3. Vérifiez que tous les fichiers sont présents
4. Vérifiez le contenu de `requirements.txt`

### Problème 2: "Application failed to respond"

**Solution:**
1. Vérifiez que `Procfile` est correct
2. Vérifiez que le port `$PORT` est utilisé
3. Attendez 30-60 secondes (service en réveil)

### Problème 3: Service "dormant"

Sur le plan gratuit, le service s'endort après 15 minutes d'inactivité.

**Solution:**
- Le premier accès prendra 30-60 secondes
- C'est normal!
- Après, ce sera instantané

---

## 📊 MAINTENANCE

### Mettre à jour le code

```powershell
# Modifiez vos fichiers localement
# Puis:
git add .
git commit -m "Description des changements"
git push origin main
```

Render redéploiera automatiquement!

### Voir les logs

1. Dashboard Render → Votre service
2. Onglet "Logs"
3. Sélectionnez "Deploy Logs" ou "Runtime Logs"

### Redémarrer le service

1. Dashboard Render → Votre service
2. Menu en haut à droite → "Manual Deploy"
3. Cliquez "Deploy latest commit"

---

## 💰 COÛTS

### Plan Gratuit (Free Tier)

✅ **Inclus:**
- 750 heures/mois
- Service dormant après 15 min d'inactivité
- Réveil automatique (30-60s)
- HTTPS automatique
- Domaine .onrender.com

❌ **Limitations:**
- Service s'endort si inactif
- 512 MB RAM
- Pas de domaine personnalisé

### Plan Payant (si besoin)

À partir de $7/mois:
- Service toujours actif (pas de sommeil)
- Plus de RAM (1GB+)
- Domaine personnalisé
- Support prioritaire

---

## 🎯 CHECKLIST FINALE

- [ ] Repository GitHub créé
- [ ] 4 fichiers créés (requirements.txt, main.py, Procfile, runtime.txt)
- [ ] Code poussé vers GitHub
- [ ] Service Render créé
- [ ] Déploiement réussi (statut "Live")
- [ ] Endpoints testés et fonctionnels
- [ ] Documentation accessible (/docs)

---

## 📞 SUPPORT

### Ressources:
- **Render Docs:** https://render.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **GitHub Docs:** https://docs.github.com

### En cas de problème:
- Vérifiez les logs Render
- Vérifiez que GitHub est à jour
- Testez localement d'abord

---

## 🎉 FÉLICITATIONS!

Votre API Kreyòl IA est maintenant déployée et accessible au monde entier!

**URL:** https://votre-service.onrender.com

**Prochaines étapes:**
- Ajoutez plus d'endpoints
- Ajoutez une interface web
- Connectez un domaine personnalisé
- Optimisez les performances

---

**Bon travail! 🚀**

