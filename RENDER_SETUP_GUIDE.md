# 🚀 Guide: Konekte ak Render Dashboard

**Pou deplwaye Faner Studio sou Render**

---

## 📋 **ETAP 1: Kreye Kont Render**

### **1.1 Ale sou Render:**
```
https://render.com
```

### **1.2 Sign Up (Si ou pa gen kont):**
- Click **"Get Started"**
- Chwazi opsyon:
  - ✅ **Sign up with GitHub** (REKÒMANDE - pi fasil)
  - Oswa: Email/Password

### **1.3 Login (Si ou gen kont deja):**
```
https://dashboard.render.com
```

---

## 🔗 **ETAP 2: Konekte GitHub Repository**

### **2.1 Nan Dashboard:**
- Click **"New +"** (top right)
- Select **"Web Service"**

### **2.2 Connect GitHub:**
- Si premye fwa: Click **"Connect GitHub"**
- Authorize Render pou aksede GitHub ou

### **2.3 Chwazi Repository:**
```
🔍 Search: fanerstudio
📦 Select: GF154/fanerstudio
🔀 Branch: master
```

---

## ⚙️ **ETAP 3: Configure Service**

Render pral detekte `render.yaml` automatikman! ✨

### **Option A: Use render.yaml (REKÒMANDE)** ✅

1. Render pral wè:
   ```
   ✅ Found render.yaml
   📋 Configuration will be applied automatically
   ```

2. Just click **"Apply"** oswa **"Create Web Service"**

3. **C'est tout!** 🎉

### **Option B: Manual Configuration** (Si render.yaml pa detekte)

```yaml
Service Name:     faner-ai-backend
Runtime:          Python 3
Region:           Oregon (US West)
Branch:           master

Build Command:
pip install --upgrade pip && pip install -r requirements.txt

Start Command:
uvicorn main:app --host 0.0.0.0 --port $PORT

Instance Type:    Free
Auto-Deploy:      Yes ✅
```

---

## 🔐 **ETAP 4: Add Environment Variables**

### **4.1 Required Variables:**

```bash
# Basic (Automatically added by Render)
PORT                    = (Auto-generated)
PYTHON_VERSION         = 3.11.0

# Optional (For better features)
HUGGINGFACE_API_KEY    = hf_xxxxxxxxxxxxx
ALLOWED_ORIGINS        = *
```

### **4.2 Kijan pou ajoute yo:**

1. Scroll down to **"Environment Variables"**
2. Click **"Add Environment Variable"**
3. Enter:
   - **Key:** `HUGGINGFACE_API_KEY`
   - **Value:** Your token
4. Click **"Add"**

### **4.3 Kote jwenn HUGGINGFACE_API_KEY:**
```
1. Ale: https://huggingface.co/settings/tokens
2. Click "New token"
3. Name: Faner Studio
4. Type: Read
5. Create & Copy
```

---

## 🚀 **ETAP 5: Deploy!**

### **5.1 Lancman:**
- Click **"Create Web Service"** (bottom)
- Render ap:
  1. ⚙️ Clone repository
  2. 📦 Install dependencies
  3. 🔨 Build application
  4. 🚀 Deploy service
  5. ✅ Start server

### **5.2 Swiv Progress:**
```
Dashboard → Your Service → Logs
```

You'll see:
```
==> Downloading Buildpack...
==> Installing Python 3.11.0
==> Installing requirements...
==> Starting server...
==> Your service is live! ✅
```

---

## 📊 **ETAP 6: Verifye Deployment**

### **6.1 Service URL:**
Render pral ba w yon URL:
```
https://faner-ai-backend.onrender.com
```

### **6.2 Test Endpoints:**

**Health Check:**
```bash
curl https://faner-ai-backend.onrender.com/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Faner Studio",
  "version": "2.0.0"
}
```

**API Docs:**
```
https://faner-ai-backend.onrender.com/docs
```

**Test Translation:**
```bash
curl -X POST https://faner-ai-backend.onrender.com/api/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello world",
    "source": "en",
    "target": "ht"
  }'
```

---

## 🔧 **ETAP 7: Configure GitHub Actions**

Pou automated deployments via GitHub Actions:

### **7.1 Get Render API Key:**
```
Dashboard → Account Settings → API Keys
→ Create API Key
→ Copy token
```

### **7.2 Get Service ID:**
```
Dashboard → Your Service → Settings
→ Look for Service ID: srv-xxxxxxxxxxxxx
```

### **7.3 Add to GitHub Secrets:**
```
GitHub Repo → Settings → Secrets and variables → Actions
→ New repository secret

Name:  RENDER_API_KEY
Value: rnd_xxxxxxxxxxxxx

Name:  RENDER_SERVICE_ID
Value: srv-xxxxxxxxxxxxx

(Optional for health checks)
Name:  RENDER_SERVICE_URL
Value: https://faner-ai-backend.onrender.com
```

---

## 📱 **ETAP 8: Monitor & Manage**

### **8.1 View Logs:**
```
Dashboard → Service → Logs (tab)
```

### **8.2 View Metrics:**
```
Dashboard → Service → Metrics (tab)
```

You'll see:
- 📊 CPU Usage
- 💾 Memory Usage
- 🌐 Request Count
- ⚡ Response Times

### **8.3 Trigger Manual Deploy:**
```
Dashboard → Service → Manual Deploy
→ Click "Deploy latest commit"
```

### **8.4 View Deployments:**
```
Dashboard → Service → Events (tab)
```

---

## 🎯 **Quick Reference**

### **Important URLs:**

| Purpose | URL |
|---------|-----|
| Render Dashboard | https://dashboard.render.com |
| GitHub Actions | https://github.com/GF154/fanerstudio/actions |
| HuggingFace Tokens | https://huggingface.co/settings/tokens |
| Your Service | https://faner-ai-backend.onrender.com |
| API Docs | https://faner-ai-backend.onrender.com/docs |
| Health Check | https://faner-ai-backend.onrender.com/health |

---

## 💡 **Tips & Troubleshooting**

### **Si Build Fail:**
1. Check logs nan Render Dashboard
2. Verify `requirements.txt` is valid
3. Ensure Python version is correct
4. Check for missing dependencies

### **Si Service Pa Start:**
1. Verify start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
2. Check logs for errors
3. Ensure `main.py` exists
4. Test locally first

### **Si Health Check Fail:**
1. Wait 2-3 minutes (service starting)
2. Check if `/health` endpoint exists
3. Verify firewall/CORS settings

### **Pour Better Performance:**
1. Use `HUGGINGFACE_API_KEY` for API rate limits
2. Enable auto-deploy for continuous delivery
3. Monitor metrics regularly
4. Check logs for errors

---

## 🎉 **Félicitations!**

Ou kounye a gen:
- ✅ Service deploye sou Render
- ✅ Auto-deploy configure
- ✅ Health checks active
- ✅ API documentation live
- ✅ Monitoring enabled

**Ou pare pou itilize Faner Studio!** 🇭🇹 🚀

---

## 📞 **Support**

Si ou bezwen èd:
- 📚 Render Docs: https://render.com/docs
- 💬 Render Community: https://community.render.com
- 🐛 GitHub Issues: https://github.com/GF154/fanerstudio/issues
- 📧 Render Support: support@render.com

---

**Bon deplwaman!** 🎊

