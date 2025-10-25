#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "🇭🇹 PWOJÈ KREYÒL IA / HAITIAN CREOLE AI PROJECT"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Verifye si Python enstale
if ! command -v python3 &> /dev/null; then
    echo "❌ Python pa enstale! Tanpri enstale Python 3.8+"
    echo "❌ Python not installed! Please install Python 3.8+"
    exit 1
fi

# Verifye si depandans yo enstale
echo "🔍 Verifye depandans / Checking dependencies..."
python3 -c "import pypdf, transformers, torch, gtts, langdetect, tqdm" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Depandans pa enstale! / Dependencies not installed!"
    echo ""
    read -p "Vle w enstale yo kounye a? (y/n): " install
    if [ "$install" = "y" ] || [ "$install" = "Y" ]; then
        echo ""
        echo "📦 Enstalasyon depandans / Installing dependencies..."
        pip3 install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo "❌ Enstalasyon echwe / Installation failed"
            exit 1
        fi
    else
        echo "❌ Depandans nesesè pou egzekite / Dependencies required to run"
        exit 1
    fi
fi

# Verifye si gen PDF
if [ ! -f "data/input.pdf" ]; then
    echo ""
    echo "⚠️  Pa gen fichye PDF nan data/input.pdf"
    echo "⚠️  No PDF file found at data/input.pdf"
    echo ""
    echo "📝 Tanpri mete yon fichye PDF nan dosye 'data' ak non 'input.pdf'"
    echo "📝 Please place a PDF file in the 'data' folder named 'input.pdf'"
    exit 1
fi

echo ""
echo "✅ Tout bagay pare! Ap kòmanse pwosesis la..."
echo "✅ Everything ready! Starting process..."
echo ""

# Egzekite script prensipal
python3 main.py

echo ""
echo "═══════════════════════════════════════════════════════════"
if [ $? -eq 0 ]; then
    echo "✅ Pwosesis la fini! Gade rezilta yo nan dosye 'output'"
    echo "✅ Process complete! Check results in 'output' folder"
else
    echo "❌ Yon erè rive pandan pwosesis la"
    echo "❌ An error occurred during processing"
fi
echo "═══════════════════════════════════════════════════════════"
echo ""

