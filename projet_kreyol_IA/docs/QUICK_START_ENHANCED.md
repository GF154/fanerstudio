# 🚀 Quick Start - Enhanced Features

Guide rapid pou itilize nouvo fonksyonalite yo / Quick guide to use new features

## ⚡ 5-Minute Setup

### 1. Install & Configure (2 min)

```bash
# Install packages
pip install -r requirements.txt

# Setup environment
cp cloud_env_template.txt .env

# Edit .env (add your bucket name)
nano .env
```

### 2. Test Connection (1 min)

```bash
# Test GCS connection
python test_cloud_storage.py
```

### 3. Choose Your Method (2 min)

Pick one:

---

## 📖 Option A: Web Interface (Easiest!)

**Best for:** Visual users, beginners

```bash
streamlit run web_app.py
```

Then:
1. 📤 Drag & drop your PDF
2. 📝 Fill in book info
3. 🚀 Click "Start Processing"
4. ⏳ Wait for results
5. 🔗 Get public links!

---

## 📚 Option B: Batch Processing

**Best for:** Processing multiple books

```bash
# 1. Edit books_config.json
nano books_config.json

# 2. Run batch
python run_batch.py

# 3. Check email for results!
```

---

## ⚡ Option C: Enhanced Script

**Best for:** Developers, automation

```bash
python process_book_enhanced.py
```

Or customize:

```python
from process_book_enhanced import EnhancedBookProcessor

processor = EnhancedBookProcessor("your-bucket")

result = processor.process_book(
    book_name="mybook",
    input_pdf_remote="input/mybook.pdf",
    title="My Book",
    author="Author Name"
)

print(result['urls'])
```

---

## 📧 Enable Email Notifications (Optional)

Add to `.env`:

```bash
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password  # Not regular password!
RECIPIENT_EMAIL=recipient@email.com
```

**Get Gmail App Password:**
1. Go to: https://myaccount.google.com/apppasswords
2. Generate password for "Mail"
3. Use that password in `.env`

---

## 🎯 What You Get

After processing, you'll have:

✅ **Translated text** (`.txt` file)
✅ **Audiobook** (`.mp3` file)
✅ **Podcast** version (`.mp3` file)
✅ **Metadata** (`.json` file)
✅ **Public links** for all files
✅ **Email notification** (if configured)

Example output:

```
🎧 --- LYEN PIBLIK YO / PUBLIC LINKS ---
📘 Text: https://storage.googleapis.com/.../text.txt
🔊 Audio: https://storage.googleapis.com/.../audio.mp3
🎙️ Podcast: https://storage.googleapis.com/.../podcast.mp3
```

---

## 📊 View Results

### In Web App:
- Click "📊 View Results" tab
- See all processed books
- Click links to download

### In Terminal:
```bash
# View metadata
python -c "from utils.metadata_manager import MetadataManager; \
m = MetadataManager(); \
print(m.generate_metadata_report('your-book-name'))"
```

### In Files:
- `output/metadata/` - Metadata files
- `output/batch_results/` - Batch results
- `output/web_results/` - Web app results

---

## 🔧 Common Commands

```bash
# Process single book (enhanced)
python process_book_enhanced.py

# Batch processing
python run_batch.py

# Web interface
streamlit run web_app.py

# Test email
python utils/email_notifier.py

# Test metadata
python utils/metadata_manager.py

# Original simple workflow
python main_cloud.py
```

---

## 📁 File Organization

```
Your bucket structure:
├── input/
│   └── yourbook.pdf
├── output/
│   └── yourbook/
│       ├── yourbook_kreyol.txt
│       ├── yourbook_audio.mp3
│       └── yourbook_podcast.mp3
├── metadata/
│   └── yourbook_metadata.json
└── batch_results/
    └── batch_results_TIMESTAMP.json
```

---

## 🎓 Learn More

- 📖 **Full Guide:** `README_ENHANCED_FEATURES.md`
- ☁️ **Cloud Setup:** `CLOUD_STORAGE_GUIDE.md`
- 🆘 **Troubleshooting:** See main README

---

## 🆘 Quick Troubleshooting

**❌ "Bucket not found"**
→ Set `GCS_BUCKET_NAME` in `.env`

**❌ "Authentication failed"**
→ Run: `gcloud auth application-default login`

**❌ "Email not sending"**
→ Use Gmail App Password, not regular password

**❌ "Module not found"**
→ Run: `pip install -r requirements.txt`

---

## ✨ Tips

💡 **Tip 1:** Start with web interface - it's the easiest!

💡 **Tip 2:** Email notifications are optional but very helpful

💡 **Tip 3:** Metadata files help you track everything

💡 **Tip 4:** Use batch processing for multiple books

💡 **Tip 5:** All files are automatically backed up to cloud

---

**Bon chans! / Good luck! 🇭🇹🚀**

