# 📖 Deployment to Vercel Guide

## 🚀 Quick Deployment

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Deploy
```bash
vercel --prod
```

## 🔧 Configuration

### Environment Variables (Required)

Add these in Vercel Dashboard → Settings → Environment Variables:

1. **DATABASE_URL** (Optional - defaults to SQLite)
   ```
   sqlite:///./data/fanerstudio.db
   ```
   Or use PostgreSQL:
   ```
   postgresql://user:password@host:5432/database
   ```

2. **SECRET_KEY** (Required for production)
   ```
   your-secret-key-here-make-it-long-and-random
   ```

3. **HUGGINGFACE_API_KEY** (Optional but recommended)
   - Get from: https://huggingface.co/settings/tokens
   ```
   hf_xxxxxxxxxxxxxxxxxxxxx
   ```

4. **OPENAI_API_KEY** (Optional)
   - Get from: https://platform.openai.com/api-keys
   ```
   sk-xxxxxxxxxxxxxxxxxxxxx
   ```

5. **ELEVENLABS_API_KEY** (Optional)
   - Get from: https://elevenlabs.io/api
   ```
   xxxxxxxxxxxxxxxxxxxxx
   ```

6. **SUPABASE_URL** (Optional)
   ```
   https://xxxxx.supabase.co
   ```

7. **SUPABASE_KEY** (Optional)
   ```
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

### Add Environment Variables via CLI

```bash
# Example
vercel env add DATABASE_URL production
vercel env add SECRET_KEY production
vercel env add HUGGINGFACE_API_KEY production
```

## 📂 Project Structure

```
faner-studio/
├── main.py                    # Main FastAPI application
├── vercel.json               # Vercel configuration
├── api/
│   └── index.py             # Vercel entry point
├── requirements.txt         # Python dependencies
├── generer_audio_huggingface.py  # TTS engine
├── podcast_fabric.py        # Advanced podcast generator
├── audio_library.py         # Music and SFX library
├── environment_validator.py  # Environment validation
└── ...
```

## ✅ Pre-Deployment Checklist

1. ✅ All dependencies in `requirements.txt`
2. ✅ `vercel.json` configured
3. ✅ Environment variables set
4. ✅ TTS engine available (gtts installed)
5. ✅ Database configured (SQLite or PostgreSQL)

## 🧪 Test Before Deployment

```bash
# Run environment validator
python environment_validator.py

# Test locally
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 Deployment Commands

```bash
# Deploy to preview (test URL)
vercel

# Deploy to production
vercel --prod

# Check deployment status
vercel ls

# View logs
vercel logs <deployment-url>

# Remove deployment
vercel remove <deployment-name>
```

## 🔍 Troubleshooting

### Issue: "Module not found"
**Solution**: Make sure all dependencies are in `requirements.txt`

### Issue: "Function timeout"
**Solution**: Increase `maxDuration` in `vercel.json` (max 300s on Pro plan)

### Issue: "Memory limit exceeded"
**Solution**: Increase `memory` in `vercel.json` (max 3008MB)

### Issue: "Database connection failed"
**Solution**: Check `DATABASE_URL` environment variable

### Issue: "TTS not working"
**Solution**: Verify `gtts` is installed and imported correctly

## 📊 Performance Optimization

1. **Cold Start**: First request may be slow (5-10s)
   - Solution: Use Vercel Pro for faster cold starts

2. **File Size**: Keep deployment < 50MB
   - Solution: Use `.vercelignore` to exclude large files

3. **Memory**: Monitor memory usage
   - Solution: Optimize audio processing in streaming mode

## 🔒 Security

1. **Never commit API keys**
   - Use environment variables only

2. **Use strong SECRET_KEY**
   ```python
   import secrets
   secrets.token_urlsafe(32)
   ```

3. **Enable HTTPS only**
   - Vercel does this automatically

## 📈 Monitoring

Monitor your deployment in Vercel Dashboard:
- Real-time logs
- Request analytics
- Error tracking
- Performance metrics

## 🆘 Support

- Vercel Docs: https://vercel.com/docs
- Vercel Support: https://vercel.com/support
- Faner Studio Issues: https://github.com/GF154/fanerstudio/issues

---

**🎉 Ready to deploy! Run: `vercel --prod`**

