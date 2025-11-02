# 🔄 Update Existing Render Service

**Pou update fanerstudio-1.onrender.com pou itilize nouvo API**

---

## 📋 Steps

### **1. Ale nan Render Dashboard:**
```
https://dashboard.render.com
→ Select "fanerstudio-1" service
```

### **2. Go to Settings:**
```
Settings tab (left sidebar)
```

### **3. Update Build & Deploy:**

#### **Build Command:**
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

#### **Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### **4. Update Environment Variables:**

Add/Update:
```
PYTHON_VERSION = 3.11.0
HUGGINGFACE_API_KEY = your_token_here (optional)
ALLOWED_ORIGINS = *
```

### **5. Manual Deploy:**
```
Manual Deploy → Deploy latest commit
```

---

## 📊 After Update

Your service will have:

```
✅ /health - Health check
✅ /api/status - System status
✅ /api/info - API information
✅ /api/translate - NLLB translation
✅ /docs - Interactive API docs
✅ /redoc - Alternative docs
```

---

## 🧪 Test After Deploy:

```bash
# Health check
curl https://fanerstudio-1.onrender.com/health

# Status
curl https://fanerstudio-1.onrender.com/api/status

# API docs (in browser)
https://fanerstudio-1.onrender.com/docs
```

---

## 💡 Or Create New Service

If you prefer a fresh start:

1. Keep `fanerstudio-1` as is (frontend/landing)
2. Create `faner-ai-backend` for API
3. Both services can coexist

**Advantages:**
- Frontend separate from backend
- Better architecture
- Independent scaling
- Clear separation of concerns

---

**Chwazi sa ki pi bon pou ou!** 🚀

