# 🔍 KOTE POU JWENN DEBUG INFO
# Where to find debug information

---

## 📍 LOCATION:

Paj `/health` la se yon JSON response. Gade nan browser la, w ap wè:

```json
{
  "status": "healthy",
  "message": "✅ Faner Studio API is running!",
  "platform": "Vercel",
  "database": "disconnected",
  "debug": {                           ← SA SE DEBUG INFO LA!
    "DB_AVAILABLE": false,
    "SUPABASE_URL_SET": false,
    "SUPABASE_KEY_SET": false
  },
  "timestamp": "2025-11-05T...",
  "version": "4.1.0",
  "endpoints": { ... }
}
```

---

## 📋 KISA POU W FÈ:

### OPSYON 1: Gade direkteman nan browser

Si browser la afiche JSON la:
- Scroll epi jwenn **"debug"** section
- Li valè yo

### OPSYON 2: View Page Source

Si browser la pa afiche JSON:
- **Right-click** sou paj la
- Click **"View Page Source"** oswa **"Inspect"**
- Gade JSON raw data la

### OPSYON 3: Copy tout text la

- **Ctrl+A** (select all)
- **Ctrl+C** (copy)
- Paste li ba mwen an

---

## 🎯 SA M BEZWEN WÈ:

Jwenn liy sa yo nan JSON la:

```json
"debug": {
  "DB_AVAILABLE": ???,           ← Di m kisa sa ye (true oswa false)
  "SUPABASE_URL_SET": ???,       ← Di m kisa sa ye (true oswa false)
  "SUPABASE_KEY_SET": ???        ← Di m kisa sa ye (true oswa false)
}
```

---

**Copy/paste tout paj JSON la oswa sèlman "debug" section ba mwen!** 📋

