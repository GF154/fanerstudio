#!/bin/bash
# Setup script for cloud storage integration

echo "=================================================="
echo "🚀 KONFIGIRASYON CLOUD STORAGE"
echo "   Cloud Storage Configuration"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 pa enstale / not installed"
    exit 1
fi

echo "✅ Python 3 installed"

# Install cloud storage packages
echo ""
echo "📦 Enstalasyon pakèt / Installing packages..."
pip install google-cloud-storage boto3 python-dotenv

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📝 Kreyasyon fichye .env / Creating .env file..."
    cp cloud_env_template.txt .env
    echo "✅ .env file created. Please edit it with your bucket name."
    echo "   Edit: nano .env"
else
    echo ""
    echo "✅ .env file already exists"
fi

# Create directories
echo ""
echo "📁 Kreyasyon repèrtwa / Creating directories..."
mkdir -p input output cache logs

echo ""
echo "=================================================="
echo "✅ Konfigirasyon konplè / Setup complete!"
echo "=================================================="
echo ""
echo "Pwochen etap / Next steps:"
echo "1. Edit .env file with your GCS_BUCKET_NAME"
echo "   nano .env"
echo ""
echo "2. Set up Google Cloud authentication:"
echo "   gcloud auth application-default login"
echo "   OR"
echo "   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json"
echo ""
echo "3. Run test:"
echo "   python test_cloud_storage.py"
echo ""
echo "4. Process a book:"
echo "   python process_book.py"
echo ""

