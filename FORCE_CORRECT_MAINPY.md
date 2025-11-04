# 🔧 Force Render to Use Correct main.py

## Current Situation:
- Local `main.py`: 1461 lines, 28+ endpoints ✅
- Render serving: 4 endpoints only ❌
- Issue: Render using wrong file!

## Solution: Check These in Render Dashboard

### 1. Go to fanerstudio-2 Settings

### 2. General Settings:
```
Branch: master ✅
Root Directory: (MUST BE EMPTY!) ⚠️
```

**If Root Directory has ANYTHING (like "projet_kreyol_IA"):**
- Clear it completely
- Save
- Redeploy

### 3. Build & Deploy:
```
Build Command:
pip install --upgrade pip && pip install -r requirements.txt

Start Command:
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**NOT:**
- `python main.py`
- `gunicorn ...`
- `uvicorn projet_kreyol_IA.main:app`

### 4. Check Procfile (if used):
Should be:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 5. After fixing:
- Manual Deploy
- Clear build cache
- Wait 7 minutes
- Test

---

## If Still Doesn't Work:

### Option A: Delete and Recreate Service
1. Delete fanerstudio-2
2. Create fanerstudio-3
3. Use render.yaml auto-config

### Option B: Use render.yaml
1. Make sure render.yaml is correct
2. Let Render auto-configure from it

---

## Test Command:
```bash
python debug_render.py
```

Should show: **28+ endpoints**, not 4!

