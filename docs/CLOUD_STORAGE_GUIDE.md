# Guide Stockage Cloud / Cloud Storage Guide

## 📦 Configuration Google Cloud Storage

### 1. Kreye yon bucket GCS / Create a GCS bucket

```bash
# Create bucket
gsutil mb gs://your-bucket-name

# Set bucket permissions (if needed)
gsutil iam ch allUsers:objectViewer gs://your-bucket-name
```

### 2. Configure authentication

#### Option A: Service Account Key (recommended for production)

1. Kreye yon service account nan Google Cloud Console
2. Telechaje key JSON la
3. Defini environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

#### Option B: Application Default Credentials (development)

```bash
gcloud auth application-default login
```

### 3. Configure bucket name

Kopye `.env.example` to `.env` epi modify:

```bash
cp .env.example .env
# Edit .env and set GCS_BUCKET_NAME
```

## 🚀 Itilizasyon / Usage

### Script senp / Simple script

```python
import os
from utils.cloud_storage import upload_to_gcs, download_from_gcs

bucket = os.getenv("GCS_BUCKET_NAME")

# Upload file
upload_to_gcs("local/file.txt", "remote/file.txt", bucket)

# Download file
download_from_gcs("remote/file.txt", "local/file.txt", bucket)
```

### Process complete book

```bash
python process_book.py
```

This script will:
1. ⬇️ Download PDF from GCS
2. 📄 Extract text
3. 🌍 Translate to Haitian Creole
4. 🎧 Generate audiobook
5. 🎙️ Create podcast
6. ☁️ Upload all results to GCS

## 📁 Structure fichye / File structure

```
input/
  └── liv1.pdf           # PDF original (telechaje depi GCS)

output/
  ├── liv1_kreyol.txt    # Tèks tradui
  ├── liv1_audio.mp3     # Audiobook
  └── podcast_final.mp3  # Podcast final
```

## 🔧 Modules disponib / Available modules

### `utils/cloud_storage.py`
- `upload_to_gcs()` - Upload fichye
- `download_from_gcs()` - Telechaje fichye

### `utils/text_extraction.py`
- `extract_text_from_pdf()` - Ekstrè tèks nan PDF

### `utils/translate.py`
- `translate_text()` - Tradui tèks an Kreyòl

### `utils/audio_gen.py`
- `generate_audio()` - Kreye audiobook

### `utils/podcast_mix.py`
- `mix_voices()` - Melanje fichye odyo

## 📋 Prerequisites

Ensure these packages are installed:

```bash
pip install google-cloud-storage boto3 python-dotenv
```

## 🔐 Security Notes

- Pa janm commit `.env` oswa service account keys nan git
- Use `.gitignore` to exclude sensitive files
- Rotate keys regularly
- Use least privilege principle for service accounts

## 🆘 Troubleshooting

### Error: "GCS_BUCKET_NAME not defined"
```bash
export GCS_BUCKET_NAME=your-bucket-name
# or create .env file
```

### Error: "Could not authenticate"
```bash
# Check credentials
gcloud auth list

# Re-authenticate
gcloud auth application-default login
```

### Error: "Bucket not found"
```bash
# List your buckets
gsutil ls

# Create bucket if needed
gsutil mb gs://your-bucket-name
```

## 📚 Resources

- [Google Cloud Storage Python Client](https://googleapis.dev/python/storage/latest/index.html)
- [GCS Authentication Guide](https://cloud.google.com/docs/authentication)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

