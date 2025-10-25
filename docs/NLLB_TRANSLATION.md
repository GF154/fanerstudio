# 🌍 NLLB Translation Service

## Configuration

La plateforme utilise maintenant **NLLB** (No Language Left Behind) via l'API Hugging Face pour des traductions de haute qualité en créole haïtien.

### Avantages de NLLB:
- ✅ **Meilleure qualité** pour le créole haïtien
- ✅ **Léger** - utilise l'API (pas de modèle local lourd)
- ✅ **Gratuit** - API Hugging Face gratuite
- ✅ **Fallback** - bascule sur Google Translate si nécessaire

## Configuration Optionnelle

Pour de meilleures performances, ajoutez une clé API Hugging Face:

1. Créez un compte sur: https://huggingface.co
2. Générez une clé API: https://huggingface.co/settings/tokens
3. Ajoutez-la dans les variables d'environnement Render:

```
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxx
```

**Note:** La clé API est optionnelle. Le service fonctionne sans clé, mais avec une clé vous aurez:
- Plus de requêtes par minute
- Meilleure priorité sur l'API

## Utilisation

### API Endpoint:

```bash
POST /api/translate
```

**Paramètres:**
- `text` - Texte à traduire
- `source_lang` - Langue source (auto, en, fr, es)
- `target_lang` - Langue cible (ht pour créole)
- `use_cache` - Utiliser le cache (true/false)

**Exemple:**
```bash
curl -X POST "https://kreyol-ia.onrender.com/api/translate" \
  -F "text=Hello, how are you?" \
  -F "source_lang=en" \
  -F "target_lang=ht"
```

**Réponse:**
```json
{
  "status": "siksè",
  "message": "Tradiksyon konplete ak NLLB! 🌍✅",
  "original": "Hello, how are you?",
  "translated": "Bonjou, kòman ou ye?",
  "source_language": "en",
  "target_language": "ht",
  "model": "NLLB-200-distilled-600M",
  "method": "Hugging Face API"
}
```

## Langues Supportées

- 🇺🇸 English (`en`)
- 🇫🇷 Français (`fr`)
- 🇪🇸 Español (`es`)
- 🇭🇹 Kreyòl Ayisyen (`ht`)

## Fallback Automatique

Si l'API NLLB est indisponible, le système bascule automatiquement sur Google Translate pour assurer la continuité du service.

## Performance

- ⚡ **API** - ~1-2 secondes par traduction
- 💾 **Cache** - Instantané pour les traductions répétées
- 🔄 **Fallback** - Toujours disponible

