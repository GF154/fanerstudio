#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Déploiement automatique sur GitHub via API
Plus flexible et programmable que GitHub CLI
"""

import os
import sys
import json
import subprocess
from pathlib import Path
import requests
from getpass import getpass

def check_git_installed():
    """Vérifie si Git est installé"""
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def init_git_repo():
    """Initialise le repository Git"""
    if not Path('.git').exists():
        print("📦 Initialisation de Git...")
        subprocess.run(['git', 'init'], check=True)
        print("✅ Git initialisé\n")
    else:
        print("✅ Git déjà initialisé\n")


def add_and_commit():
    """Ajoute et commit les fichiers"""
    print("📝 Ajout des fichiers...")
    subprocess.run(['git', 'add', '.'], check=True)
    
    print("💾 Création du commit...")
    try:
        subprocess.run([
            'git', 'commit', '-m', 
            '🚀 Initial commit - Kreyòl IA Creative Platform'
        ], check=True, capture_output=True)
        print("✅ Commit créé\n")
    except subprocess.CalledProcessError:
        print("⚠️ Aucun changement à commiter\n")


def get_github_token():
    """Récupère ou demande le token GitHub"""
    # Essayer les variables d'environnement
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
    
    if token:
        print("✅ Token GitHub trouvé dans les variables d'environnement\n")
        return token
    
    print("\n" + "="*60)
    print("🔐 AUTHENTIFICATION GITHUB")
    print("="*60)
    print("\nVous avez besoin d'un Personal Access Token (PAT)")
    print("\n📋 Comment l'obtenir:")
    print("  1. Allez sur: https://github.com/settings/tokens")
    print("  2. 'Generate new token' > 'Generate new token (classic)'")
    print("  3. Nom: kreyol-ia-deploy")
    print("  4. Cochez: 'repo' (Full control of private repositories)")
    print("  5. 'Generate token'")
    print("  6. COPIEZ le token (vous ne le reverrez plus!)")
    print("\n" + "="*60 + "\n")
    
    token = getpass("Collez votre token GitHub: ")
    
    if not token:
        print("❌ Token requis!")
        sys.exit(1)
    
    return token.strip()


def test_github_auth(token):
    """Test l'authentification GitHub"""
    print("🔍 Vérification du token...")
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.get('https://api.github.com/user', headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        username = user_data['login']
        print(f"✅ Authentifié en tant que: {username}\n")
        return username
    else:
        print(f"❌ Erreur d'authentification: {response.status_code}")
        print(f"   {response.json().get('message', 'Erreur inconnue')}")
        sys.exit(1)


def create_github_repo(token, username, repo_name='kreyol-ia', private=False):
    """Crée un repository sur GitHub"""
    print(f"📦 Création du repository '{repo_name}'...")
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'name': repo_name,
        'description': '🇭🇹 Professional AI-powered content creation platform for Haitian Creole',
        'private': private,
        'auto_init': False,
        'has_issues': True,
        'has_projects': True,
        'has_wiki': True
    }
    
    response = requests.post(
        'https://api.github.com/user/repos',
        headers=headers,
        json=data
    )
    
    if response.status_code == 201:
        repo_data = response.json()
        print(f"✅ Repository créé: {repo_data['html_url']}\n")
        return repo_data['clone_url'], repo_data['html_url']
    elif response.status_code == 422:
        print(f"⚠️ Le repository '{repo_name}' existe déjà")
        print(f"   Utilisation du repo existant...\n")
        return f'https://github.com/{username}/{repo_name}.git', f'https://github.com/{username}/{repo_name}'
    else:
        print(f"❌ Erreur lors de la création: {response.status_code}")
        print(f"   {response.json().get('message', 'Erreur inconnue')}")
        sys.exit(1)


def push_to_github(clone_url, force=False):
    """Pousse le code sur GitHub"""
    print("🚀 Envoi du code sur GitHub...")
    
    # Supprimer l'ancien remote si existe
    subprocess.run(['git', 'remote', 'remove', 'origin'], 
                   capture_output=True, stderr=subprocess.DEVNULL)
    
    # Ajouter le nouveau remote
    subprocess.run(['git', 'remote', 'add', 'origin', clone_url], check=True)
    
    # Renommer la branche en main
    subprocess.run(['git', 'branch', '-M', 'main'], check=True)
    
    # Push
    push_cmd = ['git', 'push', '-u', 'origin', 'main']
    if force:
        push_cmd.append('--force')
    
    try:
        subprocess.run(push_cmd, check=True, capture_output=True)
        print("✅ Code envoyé avec succès!\n")
    except subprocess.CalledProcessError as e:
        if b'rejected' in e.stderr:
            print("⚠️ Push rejeté. Tentative avec --force...")
            subprocess.run(push_cmd + ['--force'], check=True)
            print("✅ Code envoyé (force push)!\n")
        else:
            print(f"❌ Erreur lors du push: {e.stderr.decode()}")
            sys.exit(1)


def create_render_badge(username, repo_name='kreyol-ia'):
    """Crée un badge Deploy to Render"""
    badge_url = f"https://render.com/deploy?repo=https://github.com/{username}/{repo_name}"
    return badge_url


def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("🇭🇹 KREYÒL IA - Déploiement GitHub via API")
    print("="*60 + "\n")
    
    # Vérifications
    if not check_git_installed():
        print("❌ Git n'est pas installé!")
        print("   Téléchargez: https://git-scm.com/download/win")
        sys.exit(1)
    
    print("✅ Git détecté\n")
    
    # Étapes
    try:
        # 1. Init Git
        init_git_repo()
        
        # 2. Commit
        add_and_commit()
        
        # 3. Authentification
        token = get_github_token()
        username = test_github_auth(token)
        
        # 4. Choix de visibilité
        print("📋 Configuration du repository")
        visibility = input("Repository public ou privé? (public/private) [public]: ").lower()
        private = visibility == 'private'
        
        # 5. Création du repo
        clone_url, html_url = create_github_repo(token, username, private=private)
        
        # 6. Push
        push_to_github(clone_url, force=True)
        
        # 7. Succès!
        print("\n" + "="*60)
        print("✅ DÉPLOIEMENT GITHUB TERMINÉ!")
        print("="*60 + "\n")
        
        print(f"📦 Repository: {html_url}")
        print(f"🔗 Clone URL: {clone_url}")
        print()
        
        # Badge Render
        render_badge = create_render_badge(username)
        print("🎯 Déployer sur Render:")
        print(f"   {render_badge}")
        print()
        
        # Prochaines étapes
        print("="*60)
        print("📋 PROCHAINES ÉTAPES")
        print("="*60)
        print()
        print("Option 1 - Interface Web (Recommandé):")
        print("  1. Allez sur https://render.com")
        print("  2. Connectez-vous avec GitHub")
        print("  3. New > Web Service")
        print("  4. Sélectionnez 'kreyol-ia'")
        print("  5. Deploy!")
        print()
        print("Option 2 - Bouton Deploy:")
        print(f"  Ouvrez: {render_badge}")
        print()
        print("="*60)
        print()
        
        # Ouvrir dans le navigateur
        open_browser = input("Ouvrir le repository dans le navigateur? (o/n) [o]: ").lower()
        if not open_browser or open_browser == 'o':
            import webbrowser
            webbrowser.open(html_url)
        
        print("\n✨ Succès! Votre code est sur GitHub!\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Annulé par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

