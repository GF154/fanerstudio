# 🇭🇹 Pwojè Kreyòl IA - Enhanced Edition

## Haitian Creole AI Project - Version 2.0

Automatic translation and audiobook generation for Haitian Creole with cloud storage, batch processing, email notifications, and web interface.

---

## 🌟 What's New in v2.0

### ✨ **4 Major Features Added:**

1. 📚 **Batch Processing** - Process multiple books at once
2. 📧 **Email Notifications** - Get notified when books are done
3. 🌐 **Web Interface** - Beautiful Streamlit UI for easy use
4. 📋 **Metadata System** - Track all book information and stats

Plus:
- ⚡ Enhanced workflow with all features integrated
- 📊 Comprehensive statistics and reporting
- 🔗 Public URL generation for all files
- 💾 Automatic cloud backup
- 🛡️ Better error handling and recovery

---

## 🚀 Quick Start (3 Options)

### Option 1: Web Interface 🌐 (Recommended for beginners)

```bash
streamlit run web_app.py
```

Then drag & drop your PDF!

### Option 2: Enhanced Command Line ⚡ (Most features)

```bash
python process_book_enhanced.py
```

Full workflow with metadata, emails, and reporting.

### Option 3: Batch Processing 📚 (Multiple books)

```bash
# 1. Edit books_config.json
# 2. Run:
python run_batch.py
```

Process multiple books automatically!

---

## 📦 Installation

```bash
# 1. Clone repository
git clone <your-repo-url>
cd projet_kreyol_IA

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp cloud_env_template.txt .env
nano .env  # Add your GCS_BUCKET_NAME

# 4. Setup authentication
gcloud auth application-default login

# 5. Test connection
python test_cloud_storage.py
```

---

## 📖 Documentation

### Quick Start Guides:
- 📘 **[5-Minute Quick Start](QUICK_START_ENHANCED.md)** - Get started fast!
- 📗 **[Enhanced Features Guide](README_ENHANCED_FEATURES.md)** - Complete feature documentation
- 📙 **[Cloud Storage Guide](CLOUD_STORAGE_GUIDE.md)** - GCS setup and usage

### Reference:
- 📕 **[Feature Summary](ENHANCED_FEATURES_COMPLETE.txt)** - What's included
- 📓 **[Original README](README.md)** - Core project information

---

## 🎯 What You Get

Process a book and automatically get:

✅ **Translated Text** (Haitian Creole)
✅ **Audiobook** (MP3 format)
✅ **Podcast Version** (MP3 format)
✅ **Public URLs** for all files
✅ **Metadata** (JSON with all info)
✅ **Email Notification** (optional)
✅ **Statistics Report** (characters, duration, etc.)

All files are automatically uploaded to Google Cloud Storage with public URLs!

---

## ⚙️ Configuration

### Required (.env):
```bash
GCS_BUCKET_NAME=your-bucket-name
GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
```

### Optional (for email):
```bash
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password  # Gmail App Password
RECIPIENT_EMAIL=recipient@email.com
```

---

## 🎨 Features Comparison

| Feature | Simple | Enhanced | Batch | Web |
|---------|--------|----------|-------|-----|
| Translation | ✅ | ✅ | ✅ | ✅ |
| Audiobook | ✅ | ✅ | ✅ | ✅ |
| Cloud Upload | ✅ | ✅ | ✅ | ✅ |
| Metadata | ❌ | ✅ | ✅ | ✅ |
| Email Notify | ❌ | ✅ | ✅ | ❌ |
| Multiple Books | ❌ | ❌ | ✅ | ⚠️ |
| Visual UI | ❌ | ❌ | ❌ | ✅ |
| Statistics | ❌ | ✅ | ✅ | ✅ |

---

## 📁 Project Structure

```
projet_kreyol_IA/
├── 🆕 Batch Processing
│   ├── batch_processor.py
│   ├── run_batch.py
│   └── books_config.json
│
├── 🆕 Web Interface
│   ├── web_app.py
│   ├── run_web.sh
│   └── run_web.bat
│
├── 🆕 Enhanced Workflow
│   └── process_book_enhanced.py
│
├── 🆕 New Utilities
│   ├── utils/email_notifier.py
│   └── utils/metadata_manager.py
│
├── Cloud Processing
│   ├── main_cloud.py
│   ├── process_book.py
│   └── utils/cloud_storage.py
│
└── Core Modules
    ├── src/
    ├── tests/
    └── ...
```

---

## 💡 Usage Examples

### Web Interface
```bash
streamlit run web_app.py
# Opens browser at localhost:8501
# Drag & drop PDF → Fill form → Process!
```

### Enhanced Single Book
```python
from process_book_enhanced import EnhancedBookProcessor

processor = EnhancedBookProcessor("my-bucket")
result = processor.process_book(
    book_name="mybook",
    input_pdf_remote="input/mybook.pdf",
    title="My Book Title",
    author="Author Name"
)

print(result['urls'])  # Get public URLs
```

### Batch Processing
```python
from batch_processor import BatchProcessor

processor = BatchProcessor("my-bucket")
books = [...]  # Your book configs
results = processor.process_batch(books)
```

---

## 📧 Email Notifications

Configure in `.env`:
```bash
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=recipient@email.com
```

Get beautiful HTML emails with:
- 📚 Book title and info
- 🔗 All public download links
- 📊 Processing statistics
- ⏱️ Duration

---

## 📊 Metadata & Reports

Every book gets comprehensive metadata:
- 📖 Book information (title, author, etc.)
- 🌍 Language info (source → target)
- 📁 All file paths and URLs
- ⚙️ Processing steps with timestamps
- 📈 Statistics (characters, duration)
- 🏷️ Custom fields

Generate reports:
```python
from utils.metadata_manager import MetadataManager

manager = MetadataManager()
report = manager.generate_metadata_report("book_name")
print(report)
```

---

## 🔧 Scripts & Commands

```bash
# Web interface
streamlit run web_app.py
./run_web.sh  # or run_web.bat on Windows

# Enhanced processing
python process_book_enhanced.py

# Batch processing
python run_batch.py

# Simple cloud (original)
python main_cloud.py

# Test features
python test_cloud_storage.py
python utils/email_notifier.py
python utils/metadata_manager.py
```

---

## 🆘 Troubleshooting

### Common Issues:

**❌ Bucket not found**
```bash
# Set in .env:
GCS_BUCKET_NAME=your-bucket-name
```

**❌ Authentication failed**
```bash
gcloud auth application-default login
```

**❌ Email not sending**
- Use Gmail App Password (not regular password)
- Go to: https://myaccount.google.com/apppasswords

**❌ Module not found**
```bash
pip install -r requirements.txt
```

See [troubleshooting guide](README_ENHANCED_FEATURES.md#troubleshooting) for more.

---

## 🎓 Learning Path

1. **Start Here:** [Quick Start Guide](QUICK_START_ENHANCED.md) (5 minutes)
2. **Try:** Web interface (`streamlit run web_app.py`)
3. **Read:** [Enhanced Features Guide](README_ENHANCED_FEATURES.md)
4. **Explore:** Run examples and modify code
5. **Advanced:** Batch processing and automation

---

## 🌟 Key Technologies

- **Translation:** Hugging Face Transformers
- **Cloud Storage:** Google Cloud Storage
- **Audio Generation:** gTTS (Google Text-to-Speech)
- **Web Interface:** Streamlit
- **Email:** SMTP (Gmail)
- **Metadata:** JSON storage

---

## 📈 Statistics

- **Files Created:** 15+ new files
- **Lines of Code:** 2000+ new lines
- **Features:** 20+ new capabilities
- **Documentation:** 3 comprehensive guides

---

## 🤝 Contributing

We welcome contributions! Areas to help:

- 🎨 UI improvements
- 🌍 Additional language support
- 🔊 Voice customization
- 📱 Mobile interface
- 🧪 More tests
- 📖 More documentation

---

## 📝 License

See LICENSE file for details.

---

## 🙏 Acknowledgments

- Haitian Creole community
- Open source contributors
- AI/ML community
- Google Cloud Platform

---

## 📞 Support

- 📖 Check documentation first
- 🐛 Report bugs via GitHub issues
- 💬 Join community discussions
- 📧 Email for private inquiries

---

## 🎯 Roadmap

### Coming Soon:
- [ ] Advanced voice customization
- [ ] Multiple voice support for podcasts
- [ ] Real-time translation
- [ ] Mobile app
- [ ] API endpoints
- [ ] More language pairs

### Ideas:
- Batch web upload
- Translation memory
- Custom vocabulary
- Voice cloning
- Chapter detection

---

## ✨ Quick Links

- 🚀 [5-Minute Start](QUICK_START_ENHANCED.md)
- 📖 [Full Guide](README_ENHANCED_FEATURES.md)
- ☁️ [Cloud Setup](CLOUD_STORAGE_GUIDE.md)
- 📦 [Features Summary](ENHANCED_FEATURES_COMPLETE.txt)
- 🐛 [GitHub Issues](your-repo-issues-url)

---

## 🇭🇹 Mission

**Promoting Haitian Creole through accessible technology.**

Making translation and audiobook creation easy, fast, and free for everyone.

---

**Bon travay! / Good work! 🚀✨**

---

*Last Updated: October 2024*  
*Version: 2.0 (Enhanced Edition)*  
*Status: ✅ All Features Complete*

