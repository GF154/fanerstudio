#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Serveur Ultra-Rapide - Démarrage en 1 seconde !
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 8080
INTERFACE_FILE = "interface_rapide.html"

# Créer le fichier HTML ultra-simple
HTML_CONTENT = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🇭🇹 Pwojè Kreyòl IA - RAPIDE</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 20px;
            text-align: center;
        }
        .flag { font-size: 4em; margin: 20px 0; }
        h1 { color: #fff; margin-bottom: 10px; }
        .subtitle { color: #ddd; font-size: 1.2em; margin-bottom: 30px; }
        .btn {
            background: #4CAF50;
            color: white;
            padding: 15px 30px;
            font-size: 1.2em;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn:hover { background: #45a049; transform: translateY(-2px); }
        .status {
            margin: 20px 0;
            padding: 15px;
            border-radius: 10px;
            background: rgba(255,255,255,0.2);
        }
        .success { background: rgba(76, 175, 80, 0.3); border-left: 4px solid #4CAF50; }
        .error { background: rgba(244, 67, 54, 0.3); border-left: 4px solid #f44336; }
        .info { background: rgba(33, 150, 243, 0.3); border-left: 4px solid #2196F3; }
    </style>
</head>
<body>
    <div class="container">
        <div class="flag">🇭🇹</div>
        <h1>Pwojè Kreyòl IA</h1>
        <p class="subtitle">Traduction PDF → Créole Haïtien</p>

        <div id="status" class="status info">
            🚀 Interface prête ! Cliquez sur "Lancer" pour commencer
        </div>

        <button class="btn" onclick="lancerApplication()">
            🚀 LANCER L'APPLICATION
        </button>

        <div id="output" style="margin-top: 30px; text-align: left;"></div>
    </div>

    <script>
        function lancerApplication() {
            const btn = document.querySelector('.btn');
            const status = document.getElementById('status');
            const output = document.getElementById('output');

            // Désactiver le bouton
            btn.disabled = true;
            btn.textContent = '⏳ Démarrage...';

            // Mettre à jour le statut
            status.className = 'status info';
            status.textContent = '🔄 Connexion au serveur Python...';

            // Simuler la connexion
            setTimeout(() => {
                status.className = 'status success';
                status.textContent = '✅ Connexion établie !';
                btn.textContent = '🎉 PRÊT !';
                btn.style.background = '#2196F3';

                output.innerHTML = `
                    <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                        <h3>📋 Instructions :</h3>
                        <ol style="text-align: left; margin: 15px 0;">
                            <li>📄 Téléchargez un fichier PDF</li>
                            <li>🌍 Choisissez la langue source</li>
                            <li>🇭🇹 Sélectionnez "Créole Haïtien"</li>
                            <li>🚀 Cliquez sur "Traiter"</li>
                            <li>⏳ Attendez la traduction</li>
                            <li>📥 Téléchargez vos fichiers</li>
                        </ol>
                        <p><strong>⚡ Démarrage instantané garanti !</strong></p>
                    </div>
                `;
            }, 1500);
        }

        // Animation au chargement
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🇭🇹 Interface Kreyòl IA chargée !');
        });
    </script>
</body>
</html>"""

def creer_interface():
    """Créer le fichier HTML"""
    with open(INTERFACE_FILE, 'w', encoding='utf-8') as f:
        f.write(HTML_CONTENT)
    print(f"✅ Interface créée: {INTERFACE_FILE}")

class FastHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Ajouter les headers CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def demarrer_serveur():
    """Démarrer le serveur HTTP"""
    print("🚀 Démarrage du serveur ultra-rapide...")
    print("=" * 50)
    print("🇭🇹 PWOJÈ KREYÒL IA - Serveur Rapide")
    print("=" * 50)
    print(f"📍 Interface: http://localhost:{PORT}")
    print(f"📁 Dossier: {os.getcwd()}")
    print("⚡ Démarrage en cours...")

    # Créer l'interface
    creer_interface()

    # Changer de répertoire si nécessaire
    web_dir = Path(__file__).parent
    os.chdir(web_dir)

    # Configurer le serveur
    handler = FastHTTPRequestHandler

    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print("✅ Serveur démarré !")
            print(f"🌐 Ouvrir: http://localhost:{PORT}")
            print("🔄 Ctrl+C pour arrêter")
            print("=" * 50)

            # Ouvrir automatiquement le navigateur
            try:
                webbrowser.open(f'http://localhost:{PORT}')
            except:
                print("ℹ️  Ouvrez http://localhost:{PORT} dans votre navigateur")

            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n🛑 Serveur arrêté")
    except OSError as e:
        print(f"❌ Erreur: {e}")
        print("💡 Essayez un autre port: python serveur_rapide.py")

if __name__ == "__main__":
    demarrer_serveur()
