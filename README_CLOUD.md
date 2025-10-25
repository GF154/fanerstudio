# 📦 Cloud Storage Integration / Entegrasyon Stockage Cloud

This document explains how to use the cloud storage features for processing Haitian Creole books.

## 🎯 Objektif / Goals

Automate the entire book processing pipeline:
1. 📥 Download PDF from cloud storage
2. 📄 Extract text
3. 🌍 Translate to Haitian Creole
4. 🎧 Generate audiobook
5. 🎙️ Create podcast
6. ☁️ Upload results back to cloud

## 🚀 Quick Start / Kòmanse rapid

### 1. Installation

**Linux/Mac:**
```bash
chmod +x setup_cloud.sh
./setup_cloud.sh
```

**Windows:**
```cmd
setup_cloud.bat
```

Or manually:
```bash
pip install google-cloud-storage boto3 python-dotenv
```

### 2. Configuration

Edit `.env` file:
```bash
cp cloud_env_template.txt .env
nano .env  # or notepad .env on Windows
```

Set your bucket name:
```
GCS_BUCKET_NAME=your-bucket-name
```

### 3. Authentication

**Option A: Application Default Credentials** (easiest for development)
```bash
gcloud auth application-default login
```

**Option B: Service Account Key** (for production)
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

### 4. Test

```bash
python test_cloud_storage.py
```

### 5. Process a book

```bash
python process_book.py
```

## 📁 Structure / Estrikti fichye

```
projet_kreyol_IA/
├── utils/                      # Utility modules
│   ├── cloud_storage.py       # GCS upload/download
│   ├── text_extraction.py     # PDF text extraction
│   ├── translate.py           # Translation wrapper
│   ├── audio_gen.py           # Audio generation
│   └── podcast_mix.py         # Podcast mixing
│
├── input/                      # Input files (downloaded from cloud)
│   └── liv1.pdf
│
├── output/                     # Output files (uploaded to cloud)
│   ├── liv1_kreyol.txt        # Translated text
│   ├── liv1_audio.mp3         # Audiobook
│   └── podcast_final.mp3      # Final podcast
│
├── process_book.py            # Main processing script
├── test_cloud_storage.py      # Test script
├── cloud_env_template.txt     # Environment template
└── CLOUD_STORAGE_GUIDE.md     # Detailed guide
```

## 🔧 Available Modules / Modil disponib

### cloud_storage.py

```python
from utils.cloud_storage import upload_to_gcs, download_from_gcs

# Upload
upload_to_gcs(
    local_path="output/file.txt",
    remote_path="output/file.txt",
    bucket_name="my-bucket"
)

# Download
download_from_gcs(
    remote_path="input/file.pdf",
    local_path="input/file.pdf",
    bucket_name="my-bucket"
)
```

### text_extraction.py

```python
from utils.text_extraction import extract_text_from_pdf

text = extract_text_from_pdf("input/book.pdf")
```

### translate.py

```python
from utils.translate import translate_text

translated = translate_text(text, target_lang="ht")
```

### audio_gen.py

```python
from utils.audio_gen import generate_audio

audio_path = generate_audio(
    text=translated,
    output_path="output/audiobook.mp3",
    language="ht"
)
```

### podcast_mix.py

```python
from utils.podcast_mix import mix_voices

podcast = mix_voices(
    audio_files=["output/audio1.mp3", "output/audio2.mp3"],
    output_path="output/podcast.mp3"
)
```

## 🎬 Full Example / Egzanp konplè

```python
import os
from utils.cloud_storage import upload_to_gcs, download_from_gcs
from utils.text_extraction import extract_text_from_pdf
from utils.translate import translate_text
from utils.audio_gen import generate_audio

bucket = os.getenv("GCS_BUCKET_NAME")

# 1. Download PDF
download_from_gcs("books/input.pdf", "input/book.pdf", bucket)

# 2. Extract text
text = extract_text_from_pdf("input/book.pdf")

# 3. Translate
translated = translate_text(text, "ht")

# 4. Save and upload translation
with open("output/translated.txt", "w", encoding="utf-8") as f:
    f.write(translated)
upload_to_gcs("output/translated.txt", "books/translated.txt", bucket)

# 5. Generate audio
audio = generate_audio(translated, "output/audiobook.mp3")
upload_to_gcs(audio, "books/audiobook.mp3", bucket)

print("✅ Done!")
```

## 🔐 Security / Sekirite

### Best Practices

1. **Never commit credentials:**
   - `.env` is in `.gitignore`
   - Service account keys (*.json) are ignored
   
2. **Use least privilege:**
   - Service accounts should only have necessary permissions
   - Read-only for downloads, write for uploads

3. **Rotate keys regularly:**
   ```bash
   # Create new key
   gcloud iam service-accounts keys create new-key.json \
     --iam-account=SERVICE_ACCOUNT@PROJECT.iam.gserviceaccount.com
   
   # Delete old key
   gcloud iam service-accounts keys delete KEY_ID \
     --iam-account=SERVICE_ACCOUNT@PROJECT.iam.gserviceaccount.com
   ```

4. **Use encryption:**
   - Enable encryption at rest in GCS bucket
   - Use HTTPS for data transfer (default)

## 🆘 Troubleshooting / Depanaj

### ❌ "GCS_BUCKET_NAME not defined"

**Solution:**
```bash
# Create .env file
cp cloud_env_template.txt .env
# Edit and set GCS_BUCKET_NAME
nano .env
```

### ❌ "Could not authenticate"

**Solution:**
```bash
# Check authentication
gcloud auth list

# Re-authenticate
gcloud auth application-default login

# Or set service account key
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
```

### ❌ "Bucket not found"

**Solution:**
```bash
# List buckets
gsutil ls

# Create bucket
gsutil mb gs://your-bucket-name

# Set permissions
gsutil iam ch allUsers:objectViewer gs://your-bucket-name
```

### ❌ "Permission denied"

**Solution:**
```bash
# Add Storage Object Admin role
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:SERVICE_ACCOUNT@PROJECT.iam.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"
```

### ❌ "Module not found"

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Or specific packages
pip install google-cloud-storage boto3 python-dotenv
```

## 📊 Performance Tips / Konsèy pèfòmans

1. **Use parallel processing:**
   - Translation uses parallel chunks by default
   - Configure in `src/config.py`

2. **Enable caching:**
   - Cache translations to avoid re-processing
   - Saves time and API costs

3. **Optimize chunk size:**
   - Larger chunks = fewer API calls
   - Smaller chunks = better parallelism
   - Default: 500 characters

4. **Use regional buckets:**
   - Place bucket in same region as compute
   - Reduces latency and costs

## 📚 Resources / Resous

- [Google Cloud Storage Docs](https://cloud.google.com/storage/docs)
- [GCS Python Client](https://googleapis.dev/python/storage/latest/index.html)
- [Authentication Guide](https://cloud.google.com/docs/authentication)
- [Boto3 Docs](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Project Main README](README.md)

## 🤝 Contributing / Kontribisyon

Pour contribuer:
1. Fork le projet
2. Créer une branche (`git checkout -b feature/cloud-storage`)
3. Commit vos changements (`git commit -am 'Add feature'`)
4. Push vers la branche (`git push origin feature/cloud-storage`)
5. Créer une Pull Request

## 📝 License

Voir le fichier LICENSE principal du projet.

## ✨ Authors / Otè

- **Kreyol AI Team** - Initial work
- See [CONTRIBUTORS.md](CONTRIBUTORS.md) for full list

---

**Note:** Pou plis enfòmasyon sou modil prensipal la, gade [README.md](README.md)

