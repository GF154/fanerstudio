# 🎉 Faner Studio

**Plateforme de traduction et génération audio en Kreyòl Ayisyen**

[![Deploy Status](https://img.shields.io/badge/deploy-automated-brightgreen)](https://github.com/GF154/fanerstudio/actions)
[![Render](https://img.shields.io/badge/hosted%20on-Render-46E3B7)](https://faner-studio.onrender.com)

---

## ✨ Fonctionnalités

- 🌍 **Traduction NLLB** - Traduction de haute qualité vers le Kreyòl Ayisyen
- 🎤 **Text-to-Speech** - Génération audio en créole
- 📚 **Création d'Audiobooks** - Conversion de PDF en audiobooks
- 🎙️ **Podcasts** - Création de podcasts automatisés
- 📄 **Documentation API** - Interface Swagger interactive

---

## 🚀 Déploiement Automatique

Ce projet utilise **GitHub Actions** pour un déploiement automatique sur Render.com.

Chaque `git push` sur la branche `main` déclenche automatiquement un déploiement!

---

## 🔗 Liens Utiles

- **API Live:** https://faner-studio.onrender.com
- **Documentation:** https://faner-studio.onrender.com/docs
- **Dashboard Render:** https://dashboard.render.com
- **GitHub Actions:** https://github.com/GF154/fanerstudio/actions

---

## 🛠️ Technologies

- **Backend:** FastAPI, Python 3.11
- **Translation:** NLLB-200 (Hugging Face)
- **Hosting:** Render.com
- **CI/CD:** GitHub Actions

---

## 📝 Configuration Locale

```bash
# Cloner le repository
git clone https://github.com/GF154/fanerstudio.git
cd fanerstudio

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
uvicorn main:app --reload
```

---

## 🔑 Variables d'Environnement

```env
HUGGINGFACE_API_KEY=your_key_here
```

---

## 📊 Statut

- ✅ Déploiement: Automatique via GitHub Actions
- ✅ API: En ligne sur Render
- ✅ Traduction NLLB: Fonctionnelle
- ✅ Documentation: Disponible

---

**Fait avec ❤️ pour la communauté Kreyòl Ayisyen**

