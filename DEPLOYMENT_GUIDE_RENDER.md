# 🚀 DEPLOYMENT GUIDE - RENDER.COM

Complete step-by-step guide to deploy **Kreyòl IA Platform** to Render.com.

---

## 📋 PREREQUISITES

Before you start, make sure you have:

- ✅ **GitHub Account** (free)
- ✅ **Render.com Account** (free tier available)
- ✅ **Your code pushed to GitHub**
- ✅ **Git installed** on your computer

---

## 🎯 DEPLOYMENT OPTIONS

### **Option 1: FREE TIER** (Recommended for testing)
- **Cost**: $0/month
- **Features**: 15/23 (65%)
- **RAM**: 512MB
- **Storage**: 1GB free
- **Limitations**: Spins down after 15min of inactivity

### **Option 2: STARTER** ($7/month)
- **Cost**: $7/month
- **Features**: 15/23 (65%)
- **RAM**: 512MB
- **Storage**: 1GB included
- **Always on**: No spin down

### **Option 3: STARTER + REDIS** ($17/month) ⭐ **RECOMMENDED**
- **Cost**: $17/month
- **Features**: 23/23 (100%) ✅
- **RAM**: 512MB (web) + Redis
- **All features enabled**: Video processing, background jobs, caching

---

## 📝 STEP-BY-STEP DEPLOYMENT

### **STEP 1: Prepare Your GitHub Repository**

1. **Open PowerShell in your project directory:**
```powershell
cd "C:\Users\Fanerlink\OneDrive\Documents\liv odyo\projet_kreyol_IA"
```

2. **Initialize git (if not already done):**
```powershell
git init
```

3. **Create .gitignore to exclude sensitive files:**
```powershell
# Already exists, but verify it contains:
# .env
# __pycache__/
# *.pyc
# venv/
# output/
# cache/
# logs/
```

4. **Add all files:**
```powershell
git add .
```

5. **Commit:**
```powershell
git commit -m "Prepare for Render deployment"
```

6. **Create GitHub repository:**
   - Go to https://github.com/new
   - Name: `kreyol-ia-platform`
   - Visibility: Public or Private (your choice)
   - Click "Create repository"

7. **Push to GitHub:**
```powershell
git remote add origin https://github.com/YOUR_USERNAME/kreyol-ia-platform.git
git branch -M main
git push -u origin main
```

---

### **STEP 2: Deploy on Render**

1. **Go to Render Dashboard:**
   - Visit: https://render.com
   - Click "Get Started" (or login if you have an account)
   - Sign up with GitHub (recommended)

2. **Create New Web Service:**
   - Click "New +" button (top right)
   - Select "Web Service"

3. **Connect Repository:**
   - Authorize Render to access your GitHub
   - Find and select `kreyol-ia-platform`
   - Click "Connect"

4. **Configure Service:**
   - **Name**: `kreyol-ia-studio` (or your choice)
   - **Region**: Oregon (US West) - closest to you
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: (auto-detected from render.yaml)
     ```
     pip install --upgrade pip && pip install -r requirements.txt
     ```
   - **Start Command**: (auto-detected from Procfile)
     ```
     gunicorn app.api:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --timeout 120
     ```
   - **Plan**: Free (for testing)

5. **Environment Variables:**
   
   Render will auto-generate:
   - `SECRET_KEY` ✅
   - `PORT` ✅
   - `PYTHON_VERSION` ✅

   **Optional - Add these if you have API keys:**
   - Click "Add Environment Variable"
   - Add one by one:
     ```
     OPENAI_API_KEY = sk-your-key-here
     ELEVENLABS_API_KEY = your-key-here
     ANTHROPIC_API_KEY = your-key-here
     ```

6. **Create Web Service:**
   - Click "Create Web Service"
   - ⏳ Wait 5-10 minutes for build and deployment

---

### **STEP 3: Verify Deployment**

1. **Check Build Logs:**
   - You'll see real-time build logs
   - Look for: ✅ "Build successful"
   - Look for: ✅ "Deploy live"

2. **Test Your Platform:**
   - Render will provide a URL like:
     ```
     https://kreyol-ia-studio.onrender.com
     ```
   - Click the URL to open your platform
   - Test the interface

3. **Test API Endpoints:**
   - Visit: `https://kreyol-ia-studio.onrender.com/docs`
   - You should see the Swagger API documentation
   - Try the `/health` endpoint

4. **Check Health:**
   - Visit: `https://kreyol-ia-studio.onrender.com/health`
   - Should return:
     ```json
     {
       "status": "healthy",
       "version": "4.1.0",
       "features": {...}
     }
     ```

---

## 🔧 STEP 4: ADD REDIS (OPTIONAL - $10/month)

To enable ALL 23 features (including video processing):

1. **Create Redis Instance:**
   - In Render Dashboard, click "New +"
   - Select "Redis"
   - **Name**: `kreyol-ia-redis`
   - **Plan**: Starter ($10/month) or Free (25MB - limited)
   - Click "Create Redis"

2. **Connect Redis to Web Service:**
   - Go back to your Web Service
   - Click "Environment" tab
   - Add new variable:
     ```
     REDIS_URL = [Internal Connection String]
     ```
   - Copy the internal connection string from Redis dashboard
   - Paste it as the value

3. **Redeploy:**
   - Click "Manual Deploy" → "Deploy latest commit"
   - Wait for redeployment
   - ✅ All 23 features now active!

---

## 🎉 DEPLOYMENT COMPLETE!

Your platform is now live! You should have:

### **✅ What's Working:**
- 🌐 Live URL: `https://kreyol-ia-studio.onrender.com`
- 📱 Web Interface
- 📚 API Documentation at `/docs`
- 🔊 Audio tools (6 features)
- 🌍 Translation (2 features)
- 📄 PDF processing
- 🎥 Video tools (if Redis is enabled)

### **⚙️ Platform Status:**

**Without Redis (FREE):**
```
✅ Audio: Audiobook, Podcast, URL-to-Audio, TTS, STT (6)
✅ Translation: Text & Document translation (2)
✅ Document: PDF, TXT, DOCX, EPUB extraction (4)
❌ Video: Requires Redis
❌ Background Jobs: Requires Redis
❌ Advanced Caching: Uses memory cache only
```

**With Redis ($17/month):**
```
✅ All 23 features working
✅ Video processing (7 tools)
✅ AI script generation
✅ Background jobs (no timeouts)
✅ Redis caching (100x faster)
✅ WebSocket progress updates
```

---

## 🔄 AUTOMATIC UPDATES

Your platform will **auto-deploy** when you push to GitHub:

```powershell
# Make changes to your code
git add .
git commit -m "Add new feature"
git push

# Render automatically:
# 1. Detects the push
# 2. Builds the new version
# 3. Deploys it
# 4. Your site updates in 5-10 minutes
```

---

## 📊 MONITORING

### **View Logs:**
1. Go to Render Dashboard
2. Click your Web Service
3. Click "Logs" tab
4. See real-time server logs

### **Monitor Metrics:**
- Visit: `https://kreyol-ia-studio.onrender.com/metrics`
- See Prometheus metrics

### **Check Health:**
- Render automatically pings `/health` every 30 seconds
- If it fails, you'll get an email alert

---

## 🆘 TROUBLESHOOTING

### **Issue 1: Build Failed**
```
Error: No module named 'xxx'
```
**Fix:** Add missing package to `requirements.txt` and push again.

### **Issue 2: Server Timeout**
```
Error: Application failed to respond
```
**Fix:** Increase timeout in Procfile (already set to 120s).

### **Issue 3: Out of Memory**
```
Error: Killed (OOM)
```
**Fix:** 
- Upgrade to Starter plan ($7/month) for more RAM
- Or reduce concurrent workers in Procfile (change `--workers 2` to `--workers 1`)

### **Issue 4: 503 Service Unavailable (Free Tier)**
**Cause:** Service spun down after 15 minutes of inactivity.
**Fix:** 
- Wait 30-60 seconds for it to wake up
- Or upgrade to Starter ($7/month) for always-on

### **Issue 5: Video Tools Not Working**
**Cause:** Need Redis for video processing.
**Fix:** Add Redis as shown in Step 4.

---

## 💰 COST BREAKDOWN

### **Free Tier:**
```
Web Service (Free):  $0/month
Storage (1GB):       $0/month
Features:            15/23 (65%)
Total:               $0/month ✅
```

### **Starter:**
```
Web Service (Starter): $7/month
Storage (1GB):         $0/month
Features:              15/23 (65%)
Total:                 $7/month
```

### **Full Power (Recommended):**
```
Web Service (Starter): $7/month
Redis (Starter):       $10/month
Storage (1GB):         $0/month
Features:              23/23 (100%) ✅
Total:                 $17/month
```

### **If You Need More Storage:**
```
Extra 10GB storage:  $2.50/month
Extra 50GB storage:  $12.50/month
```

---

## 🔐 SECURITY RECOMMENDATIONS

### **1. Environment Variables:**
- ✅ Never commit `.env` to GitHub
- ✅ Use Render's Environment Variables panel
- ✅ Rotate `SECRET_KEY` regularly

### **2. API Keys:**
- ✅ Store in Render Environment Variables
- ✅ Use separate keys for production
- ❌ Never hardcode in source code

### **3. CORS:**
- Update CORS origins in production
- Add your domain to allowed origins

### **4. Rate Limiting:**
- Already configured in the platform
- Will activate when `slowapi` is installed

---

## 📈 SCALING

### **When to Upgrade:**

**From Free to Starter ($7/month):**
- Need always-on service
- Want faster response times

**From Starter to Starter+Redis ($17/month):**
- Need video processing
- Want all 23 features
- Need background jobs
- Handling >100 requests/day

**From Starter to Pro ($25/month):**
- Heavy traffic (>1000 requests/day)
- Need more RAM (4GB)
- Want faster builds

---

## 🎯 NEXT STEPS

1. **✅ Share Your Platform:**
   ```
   https://kreyol-ia-studio.onrender.com
   ```

2. **📊 Monitor Usage:**
   - Check Render dashboard daily
   - Watch build times
   - Monitor errors in logs

3. **🚀 Add Features:**
   - Push updates to GitHub
   - Auto-deploys in minutes

4. **💰 Upgrade When Ready:**
   - Start with free tier
   - Add Redis when you need video tools
   - Scale up as traffic grows

---

## 📞 SUPPORT

### **Render Support:**
- Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

### **Platform Issues:**
- Check logs in Render dashboard
- Test locally first: `python run_server.py`
- Compare local vs production behavior

---

## 🎊 CONGRATULATIONS!

Your **Kreyòl IA Platform** is now live and accessible worldwide! 🌍

**What you've accomplished:**
- ✅ Professional production deployment
- ✅ Automatic updates from GitHub
- ✅ HTTPS encryption (free SSL)
- ✅ Health monitoring
- ✅ Scalable architecture
- ✅ Global CDN

**Your platform can now:**
- 📖 Create audiobooks in Haitian Creole
- 🎙️ Generate podcasts
- 🌍 Translate documents
- 🎥 Process videos (with Redis)
- 🤖 Generate AI scripts
- ...and 18 more features!

---

**🇭🇹 Fèlisitasyon! Platfòm ou an kounye a ap travay sou entènèt! 🎉**

