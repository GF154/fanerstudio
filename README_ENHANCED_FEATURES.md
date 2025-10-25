## 🚀 Enhanced Features / Fonksyonalite Amelyore

Comprehensive guide for all enhanced features in the Haitian Creole AI Project.

## 📑 Table of Contents

1. [Batch Processing](#batch-processing)
2. [Email Notifications](#email-notifications)
3. [Web Interface](#web-interface)
4. [Metadata System](#metadata-system)
5. [Enhanced Workflow](#enhanced-workflow)

---

## 1. 📚 Batch Processing / Traitement Multiple

Trete plizyè liv an menm tan / Process multiple books at once.

### Features:
- ✅ Process multiple PDFs in sequence
- ✅ Automatic error handling
- ✅ Progress tracking
- ✅ JSON result reports
- ✅ Email notifications for batch completion

### Usage:

#### Method 1: Using Configuration File

1. **Edit `books_config.json`:**

```json
{
  "books": [
    {
      "name": "liv1",
      "input_pdf": "input/liv1.pdf",
      "metadata": {
        "title": "First Book",
        "author": "Author 1",
        "language": "fr",
        "year": 2024
      }
    },
    {
      "name": "liv2",
      "input_pdf": "input/liv2.pdf",
      "metadata": {
        "title": "Second Book",
        "author": "Author 2"
      }
    }
  ]
}
```

2. **Run batch processing:**

```bash
python run_batch.py
```

#### Method 2: Programmatic

```python
from batch_processor import BatchProcessor

bucket = "your-bucket-name"
processor = BatchProcessor(bucket)

books = [
    {
        'name': 'book1',
        'input_pdf': 'input/book1.pdf',
        'metadata': {'title': 'Book 1', 'author': 'Author'}
    }
]

results = processor.process_batch(books)
```

### Output:

Batch results are saved in:
- Local: `output/batch_results/batch_results_TIMESTAMP.json`
- GCS: `gs://bucket/batch_results/`

---

## 2. 📧 Email Notifications / Notifikasyon Email

Automatic email notifications for processing completion.

### Features:
- ✅ HTML formatted emails
- ✅ Book completion notifications
- ✅ Batch completion summaries
- ✅ Error notifications
- ✅ Public links included

### Configuration:

Add to your `.env` file:

```bash
# Email Configuration
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=recipient@email.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**Important:** For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password.

### Usage:

```python
from utils.email_notifier import EmailNotifier

notifier = EmailNotifier()

# Notify book completion
urls = {
    'text': 'https://...text.txt',
    'audio': 'https://...audio.mp3',
    'podcast': 'https://...podcast.mp3'
}
notifier.notify_book_complete("book_name", urls)

# Notify batch completion
notifier.notify_batch_complete(results, duration=120.5)

# Notify error
notifier.notify_error("book_name", "Error message")
```

### Email Templates:

Emails include:
- 📚 Book name and title
- 🔗 Public download links
- 📊 Processing statistics
- ⏱️ Timestamp
- 🎨 Beautiful HTML formatting

---

## 3. 🌐 Web Interface / Entèfas Web

Beautiful Streamlit web interface for easy book processing.

### Features:
- ✅ Drag-and-drop PDF upload
- ✅ Real-time progress tracking
- ✅ Metadata input form
- ✅ Public link display
- ✅ Previous results viewer
- ✅ Batch processing mode

### Usage:

1. **Start the web app:**

```bash
streamlit run web_app.py
```

2. **Open browser:**

The app will automatically open at `http://localhost:8501`

3. **Upload and process:**
   - Click "Browse files" to upload PDF
   - Fill in book metadata
   - Click "Start Processing"
   - Wait for completion
   - Get public links

### Interface Modes:

#### 📤 Upload & Process
Upload and process a single book with metadata.

#### 📚 Batch Processing
Upload multiple PDFs for batch processing.

#### 📊 View Results
View all previously processed books with links.

### Screenshots:

```
┌─────────────────────────────────────┐
│  🇭🇹 Pwojè Kreyòl IA               │
│  Haitian Creole AI Project          │
├─────────────────────────────────────┤
│ ⚙️ Settings                         │
│ ✅ Bucket: your-bucket              │
│                                     │
│ Mode: 📤 Upload & Process           │
├─────────────────────────────────────┤
│ [Upload PDF]                        │
│                                     │
│ Book Name: ____________             │
│ Author: _______________             │
│ Title: ________________             │
│                                     │
│ [🚀 Start Processing]               │
└─────────────────────────────────────┘
```

---

## 4. 📋 Metadata System / Sistèm Metadone

Comprehensive metadata management for all processed books.

### Features:
- ✅ Structured metadata storage
- ✅ Processing step tracking
- ✅ File information (size, URLs)
- ✅ Statistics (characters, duration)
- ✅ Custom fields support
- ✅ Upload metadata to GCS
- ✅ Search and filter
- ✅ Report generation

### Usage:

```python
from utils.metadata_manager import MetadataManager

manager = MetadataManager(bucket_name="your-bucket")

# Create metadata
metadata = manager.create_metadata(
    book_name="book1",
    title="My Book",
    author="Author Name",
    year=2024,
    genre="Fiction"
)

# Save metadata
manager.save_metadata(metadata, "book1")

# Add processing step
manager.add_processing_step(
    "book1",
    "translation",
    "completed",
    details={'duration': 120.5}
)

# Add file metadata
manager.add_file_metadata(
    "book1",
    "audio",
    "output/book1/audio.mp3",
    file_url="https://...",
    file_size=5242880
)

# Add statistics
manager.add_statistics("book1", {
    'characters': 50000,
    'words': 10000,
    'duration_minutes': 45
})

# Upload to GCS
manager.upload_metadata_to_gcs("book1")

# Generate report
report = manager.generate_metadata_report("book1")
print(report)

# Search metadata
results = manager.search_metadata(author="Author Name")
```

### Metadata Structure:

```json
{
  "book_name": "book1",
  "title": "My Book",
  "author": "Author Name",
  "created_at": "2024-10-13T10:30:00",
  "language": {
    "source": "fr",
    "target": "ht"
  },
  "files": {
    "text": {
      "path": "output/book1/text.txt",
      "url": "https://...",
      "size_mb": 0.5
    },
    "audio": {
      "path": "output/book1/audio.mp3",
      "url": "https://...",
      "size_mb": 5.2
    }
  },
  "processing": {
    "status": "completed",
    "steps_completed": [
      {
        "name": "extraction",
        "status": "completed",
        "timestamp": "2024-10-13T10:31:00"
      }
    ]
  },
  "statistics": {
    "characters": 50000,
    "words": 10000,
    "duration_seconds": 300
  }
}
```

---

## 5. ⚡ Enhanced Workflow / Workflow Amelyore

Complete end-to-end processing with all features integrated.

### Usage:

```bash
python process_book_enhanced.py
```

Or programmatically:

```python
from process_book_enhanced import EnhancedBookProcessor

bucket = "your-bucket-name"
processor = EnhancedBookProcessor(bucket)

result = processor.process_book(
    book_name="mybook",
    input_pdf_remote="input/mybook.pdf",
    title="My Book Title",
    author="Author Name",
    year=2024,
    genre="Education",
    description="Book description"
)

print(f"Status: {result['status']}")
print(f"URLs: {result['urls']}")
```

### What it does:

1. 📝 **Creates metadata** with book information
2. 📥 **Downloads PDF** from GCS
3. 📄 **Extracts text** from PDF
4. 🌍 **Translates** to Haitian Creole
5. 🎧 **Generates audiobook** (MP3)
6. 🎙️ **Creates podcast** version
7. ☁️ **Uploads all files** to GCS (with public URLs)
8. 💾 **Uploads metadata** to GCS
9. 📧 **Sends email** notification
10. 📊 **Generates report** with all information

### Output:

```
╔══════════════════════════════════════════════════════════╗
║                  METADATA REPORT                         ║
╚══════════════════════════════════════════════════════════╝

📚 BOOK INFORMATION
────────────────────────────────────────────────────────────
Book Name:    mybook
Title:        My Book Title
Author:       Author Name
Created:      2024-10-13 10:30:00
Version:      1.0

🌍 LANGUAGE
────────────────────────────────────────────────────────────
Source:       fr
Target:       ht

📁 FILES
────────────────────────────────────────────────────────────
TEXT:
  Path: output/mybook/mybook_kreyol.txt
  Size: 0.5 MB
  URL:  https://storage.googleapis.com/.../text.txt

AUDIO:
  Path: output/mybook/mybook_audio.mp3
  Size: 5.2 MB
  URL:  https://storage.googleapis.com/.../audio.mp3

⚙️  PROCESSING
────────────────────────────────────────────────────────────
Status: completed

Steps Completed:
  ✅ download (2024-10-13 10:30:15)
  ✅ extraction (2024-10-13 10:31:20)
  ✅ translation (2024-10-13 10:35:40)
  ✅ audio_generation (2024-10-13 10:40:10)

📊 STATISTICS
────────────────────────────────────────────────────────────
  original_characters: 50000
  translated_characters: 52000
  processing_duration_minutes: 12.5
```

---

## 🔧 Configuration Summary

### Required Environment Variables:

```bash
# Cloud Storage (Required)
GCS_BUCKET_NAME=your-bucket-name
GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json

# Email Notifications (Optional)
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=recipient@email.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### File Structure:

```
projet_kreyol_IA/
├── batch_processor.py          # Batch processing
├── run_batch.py               # Run batch from config
├── books_config.json          # Batch configuration
├── web_app.py                 # Streamlit web interface
├── process_book_enhanced.py   # Enhanced single book processor
├── utils/
│   ├── email_notifier.py      # Email notifications
│   └── metadata_manager.py    # Metadata management
├── output/
│   ├── batch_results/         # Batch processing results
│   ├── web_results/           # Web app results
│   └── metadata/              # Book metadata files
```

---

## 🚀 Quick Start Guide

### 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp cloud_env_template.txt .env
nano .env  # Edit with your values

# Setup cloud storage
./setup_cloud.sh  # or setup_cloud.bat on Windows

# Test connection
python test_cloud_storage.py
```

### 2. Process Single Book (Enhanced)

```bash
python process_book_enhanced.py
```

### 3. Batch Processing

```bash
# Edit books_config.json first
python run_batch.py
```

### 4. Web Interface

```bash
streamlit run web_app.py
```

---

## 📚 Examples

### Example 1: Simple Book Processing

```python
from process_book_enhanced import EnhancedBookProcessor

processor = EnhancedBookProcessor("my-bucket")
result = processor.process_book(
    book_name="book1",
    input_pdf_remote="input/book1.pdf",
    title="My First Book",
    author="John Doe"
)
```

### Example 2: Batch with Email Notifications

```python
from batch_processor import BatchProcessor

processor = BatchProcessor("my-bucket", enable_email=True)
books = [...]  # Your book list
results = processor.process_batch(books)
```

### Example 3: Metadata Management

```python
from utils.metadata_manager import MetadataManager

manager = MetadataManager()

# Create and save
metadata = manager.create_metadata("book1", "Title", "Author")
manager.save_metadata(metadata, "book1")

# Update
manager.add_processing_step("book1", "translation", "completed")

# Search
results = manager.search_metadata(status="completed")
```

---

## 🆘 Troubleshooting

### Email not working?
- Check Gmail App Password (not regular password)
- Verify SMTP settings
- Check spam folder

### Metadata not uploading?
- Verify bucket permissions
- Check GCS authentication
- Ensure metadata file exists

### Batch processing slow?
- Process books in smaller batches
- Check internet connection
- Monitor cloud storage quotas

---

## 📝 License

Same as main project license.

## 🤝 Contributing

See main README for contribution guidelines.

---

**Bon travay! / Good work! 🇭🇹**

