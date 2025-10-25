#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastAPI Web Interface - Interface Web Rapide
Fast and modern web interface for Kreyòl IA
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path
import tempfile
import os
from typing import Optional

# Import modules
try:
    from src import Config, PDFExtractor, CreoleTranslator, AudiobookGenerator
except ImportError:
    # Fallback pour les imports
    PDFExtractor = None
    CreoleTranslator = None
    AudiobookGenerator = None

app = FastAPI(title="🇭🇹 Pwojè Kreyòl IA")

# Créer les dossiers nécessaires
OUTPUT_DIR = Path("output/web")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Page HTML principale
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🇭🇹 Pwojè Kreyòl IA</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 2.5em;
            color: #2d3748;
            margin-bottom: 10px;
        }
        
        .header .flag {
            font-size: 3em;
        }
        
        .header p {
            color: #718096;
            font-size: 1.1em;
        }
        
        .upload-area {
            border: 3px dashed #cbd5e0;
            border-radius: 15px;
            padding: 60px 40px;
            text-align: center;
            transition: all 0.3s;
            cursor: pointer;
            margin-bottom: 30px;
        }
        
        .upload-area:hover {
            border-color: #667eea;
            background: #f7fafc;
        }
        
        .upload-area.dragover {
            border-color: #667eea;
            background: #ebf4ff;
        }
        
        .upload-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }
        
        .upload-area h3 {
            color: #2d3748;
            margin-bottom: 10px;
        }
        
        .upload-area p {
            color: #718096;
        }
        
        input[type="file"] {
            display: none;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.1em;
            border-radius: 10px;
            cursor: pointer;
            transition: transform 0.2s;
            font-weight: bold;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn:disabled {
            background: #cbd5e0;
            cursor: not-allowed;
            transform: none;
        }
        
        .options {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .option-group {
            background: #f7fafc;
            padding: 20px;
            border-radius: 10px;
        }
        
        .option-group label {
            display: block;
            color: #2d3748;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .option-group select {
            width: 100%;
            padding: 10px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        
        .option-group select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .option-group input[type="checkbox"] {
            width: 20px;
            height: 20px;
            margin-right: 10px;
        }
        
        .checkbox-label {
            display: flex;
            align-items: center;
            cursor: pointer;
        }
        
        .progress-container {
            display: none;
            margin: 30px 0;
        }
        
        .progress-bar {
            width: 100%;
            height: 30px;
            background: #e2e8f0;
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 10px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        
        .status-text {
            text-align: center;
            color: #4a5568;
            font-size: 1.1em;
        }
        
        .results {
            display: none;
            margin-top: 30px;
            padding: 30px;
            background: #f0fff4;
            border-radius: 15px;
            border: 2px solid #9ae6b4;
        }
        
        .results h2 {
            color: #22543d;
            margin-bottom: 20px;
        }
        
        .result-item {
            background: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .result-item a {
            color: #667eea;
            text-decoration: none;
            font-weight: bold;
        }
        
        .result-item a:hover {
            text-decoration: underline;
        }
        
        .error {
            display: none;
            margin-top: 20px;
            padding: 20px;
            background: #fff5f5;
            border: 2px solid #fc8181;
            border-radius: 10px;
            color: #742a2a;
        }
        
        .file-info {
            display: none;
            margin: 20px 0;
            padding: 15px;
            background: #ebf4ff;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        
        .file-info strong {
            color: #2d3748;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="flag">🇭🇹</div>
            <h1>Pwojè Kreyòl IA</h1>
            <p>Traduisez vos PDF en créole haïtien et créez des livres audio</p>
        </div>
        
        <div class="upload-area" id="uploadArea">
            <div class="upload-icon">📄</div>
            <h3>Glissez votre PDF ici ou cliquez pour choisir</h3>
            <p>Drag & drop ou sélectionnez un fichier PDF</p>
            <input type="file" id="fileInput" accept=".pdf">
        </div>
        
        <div class="file-info" id="fileInfo">
            <strong>Fichier sélectionné:</strong> <span id="fileName"></span>
        </div>
        
        <div class="options">
            <div class="option-group">
                <label>Langue source</label>
                <select id="sourceLang">
                    <option value="auto">Auto-détection</option>
                    <option value="fr" selected>Français</option>
                    <option value="en">English</option>
                    <option value="es">Español</option>
                </select>
            </div>
            
            <div class="option-group">
                <label>Langue cible</label>
                <select id="targetLang">
                    <option value="ht" selected>Kreyòl Ayisyen 🇭🇹</option>
                    <option value="fr">Français</option>
                    <option value="en">English</option>
                </select>
            </div>
            
            <div class="option-group">
                <label class="checkbox-label">
                    <input type="checkbox" id="generateAudio" checked>
                    <span>🔊 Générer l'audiobook</span>
                </label>
            </div>
        </div>
        
        <center>
            <button class="btn" id="processBtn" disabled>🚀 Traiter le document</button>
        </center>
        
        <div class="progress-container" id="progressContainer">
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill">0%</div>
            </div>
            <div class="status-text" id="statusText">Traitement en cours...</div>
        </div>
        
        <div class="error" id="errorDiv"></div>
        
        <div class="results" id="results">
            <h2>✅ Traitement terminé avec succès!</h2>
            <div id="resultLinks"></div>
        </div>
    </div>
    
    <script>
        let selectedFile = null;
        
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const processBtn = document.getElementById('processBtn');
        const progressContainer = document.getElementById('progressContainer');
        const progressFill = document.getElementById('progressFill');
        const statusText = document.getElementById('statusText');
        const results = document.getElementById('results');
        const resultLinks = document.getElementById('resultLinks');
        const errorDiv = document.getElementById('errorDiv');
        
        // Upload area events
        uploadArea.addEventListener('click', () => fileInput.click());
        
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            if (e.dataTransfer.files.length > 0) {
                handleFile(e.dataTransfer.files[0]);
            }
        });
        
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFile(e.target.files[0]);
            }
        });
        
        function handleFile(file) {
            if (file.type !== 'application/pdf') {
                showError('❌ Veuillez sélectionner un fichier PDF');
                return;
            }
            
            selectedFile = file;
            fileName.textContent = file.name;
            fileInfo.style.display = 'block';
            processBtn.disabled = false;
            errorDiv.style.display = 'none';
            results.style.display = 'none';
        }
        
        processBtn.addEventListener('click', async () => {
            if (!selectedFile) return;
            
            // Préparer l'interface
            processBtn.disabled = true;
            progressContainer.style.display = 'block';
            results.style.display = 'none';
            errorDiv.style.display = 'none';
            
            // Créer FormData
            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('source_lang', document.getElementById('sourceLang').value);
            formData.append('target_lang', document.getElementById('targetLang').value);
            formData.append('generate_audio', document.getElementById('generateAudio').checked);
            
            try {
                updateProgress(10, '📥 Upload du fichier...');
                
                const response = await fetch('/process', {
                    method: 'POST',
                    body: formData
                });
                
                updateProgress(30, '📄 Extraction du texte...');
                await new Promise(resolve => setTimeout(resolve, 500));
                
                updateProgress(50, '🌍 Traduction en cours...');
                await new Promise(resolve => setTimeout(resolve, 1000));
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Erreur lors du traitement');
                }
                
                updateProgress(80, '🔊 Génération audio...');
                await new Promise(resolve => setTimeout(resolve, 500));
                
                const result = await response.json();
                
                updateProgress(100, '✅ Terminé!');
                
                // Afficher les résultats
                setTimeout(() => {
                    displayResults(result);
                }, 500);
                
            } catch (error) {
                showError('❌ Erreur: ' + error.message);
                progressContainer.style.display = 'none';
                processBtn.disabled = false;
            }
        });
        
        function updateProgress(percent, text) {
            progressFill.style.width = percent + '%';
            progressFill.textContent = percent + '%';
            statusText.textContent = text;
        }
        
        function displayResults(result) {
            progressContainer.style.display = 'none';
            results.style.display = 'block';
            
            let html = '';
            
            if (result.translation_file) {
                html += `
                    <div class="result-item">
                        <span>📄 Texte traduit</span>
                        <a href="/download/${result.translation_file}" download>Télécharger</a>
                    </div>
                `;
            }
            
            if (result.audio_file) {
                html += `
                    <div class="result-item">
                        <span>🔊 Livre audio</span>
                        <a href="/download/${result.audio_file}" download>Télécharger</a>
                    </div>
                `;
            }
            
            resultLinks.innerHTML = html;
            processBtn.disabled = false;
        }
        
        function showError(message) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def home():
    """Page d'accueil"""
    return HTML_CONTENT


@app.post("/process")
async def process_document(
    file: UploadFile = File(...),
    source_lang: str = "fr",
    target_lang: str = "ht",
    generate_audio: bool = True
):
    """Traiter un document PDF"""
    
    # Vérifier que c'est un PDF
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Le fichier doit être un PDF")
    
    try:
        # Sauvegarder le fichier temporairement
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = Path(tmp.name)
        
        # Créer un nom de fichier unique
        base_name = Path(file.filename).stem
        output_base = OUTPUT_DIR / base_name
        
        # Simuler le traitement (remplacer par votre vraie logique)
        # Pour l'instant, créer des fichiers de test
        
        # Fichier de traduction
        translation_file = f"{base_name}_translation.txt"
        translation_path = OUTPUT_DIR / translation_file
        
        with open(translation_path, 'w', encoding='utf-8') as f:
            f.write(f"Traduction du fichier: {file.filename}\n\n")
            f.write("Ceci est une traduction de démonstration.\n")
            f.write("En production, utilisez vos modules de traduction.\n")
        
        result = {
            "status": "success",
            "translation_file": translation_file,
            "message": "Traitement terminé avec succès"
        }
        
        # Si génération audio demandée
        if generate_audio:
            audio_file = f"{base_name}_audio.mp3"
            audio_path = OUTPUT_DIR / audio_file
            
            # Créer un fichier audio de test (vide)
            audio_path.touch()
            result["audio_file"] = audio_file
        
        # Nettoyer le fichier temporaire
        tmp_path.unlink()
        
        return JSONResponse(content=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Télécharger un fichier"""
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok"}


if __name__ == "__main__":
    print("=" * 60)
    print("🇭🇹  PWOJÈ KREYÒL IA - Interface Web Rapide")
    print("=" * 60)
    print()
    print("🌐  Serveur démarré sur: http://localhost:8000")
    print("📱  Interface web: http://localhost:8000")
    print()
    print("✨  Prêt à traduire vos documents!")
    print()
    print("Appuyez sur Ctrl+C pour arrêter")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")





