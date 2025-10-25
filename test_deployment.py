#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de pré-déploiement
Vérifie que tout est prêt pour Render
"""

import sys
import os
from pathlib import Path

def test_files_exist():
    """Vérifie que tous les fichiers nécessaires existent"""
    required_files = [
        'api_final.py',
        'app_studio_dark.html',
        'requirements.txt',
        'render.yaml',
        'runtime.txt',
        'Procfile',
        '.gitignore',
        'README.md',
        'DEPLOYMENT_GUIDE.md'
    ]
    
    print("🔍 Vérification des fichiers...")
    missing = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MANQUANT!")
            missing.append(file)
    
    if missing:
        print(f"\n❌ Fichiers manquants: {', '.join(missing)}")
        return False
    
    print("\n✅ Tous les fichiers nécessaires sont présents\n")
    return True


def test_python_version():
    """Vérifie la version Python"""
    print("🐍 Vérification de Python...")
    version = sys.version_info
    
    if version.major == 3 and version.minor >= 11:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
        print("     Compatible avec Render\n")
        return True
    else:
        print(f"  ⚠️ Python {version.major}.{version.minor}.{version.micro}")
        print("     Render recommande Python 3.11+")
        print("     Cela devrait quand même fonctionner\n")
        return True


def test_imports():
    """Teste les imports critiques"""
    print("📦 Test des dépendances critiques...")
    
    critical_imports = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('transformers', 'Transformers'),
        ('pypdf', 'PyPDF'),
    ]
    
    failed = []
    
    for module, name in critical_imports:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} - Non installé!")
            failed.append(name)
    
    if failed:
        print(f"\n❌ Dépendances manquantes: {', '.join(failed)}")
        print("   Exécutez: pip install -r requirements.txt\n")
        return False
    
    print("\n✅ Toutes les dépendances critiques sont installées\n")
    return True


def test_api_import():
    """Teste l'import de l'API"""
    print("🔌 Test de l'API...")
    
    try:
        from api_final import app
        print("  ✅ api_final.py importé avec succès")
        print(f"  ✅ FastAPI app trouvée: {app.title}\n")
        return True
    except Exception as e:
        print(f"  ❌ Erreur d'import: {e}\n")
        return False


def test_directories():
    """Vérifie les dossiers nécessaires"""
    print("📁 Vérification des dossiers...")
    
    dirs = ['output', 'src', 'cache']
    
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ⚠️ {dir_name}/ n'existe pas (sera créé automatiquement)")
    
    print()
    return True


def check_git_status():
    """Vérifie le statut Git"""
    print("🔄 Vérification Git...")
    
    if not Path('.git').exists():
        print("  ⚠️ Git n'est pas initialisé")
        print("     Exécutez: git init\n")
        return False
    
    print("  ✅ Repository Git initialisé\n")
    return True


def main():
    """Fonction principale"""
    print("=" * 60)
    print("🇭🇹 KREYÒL IA - Test de Pré-Déploiement")
    print("=" * 60)
    print()
    
    tests = [
        ("Fichiers requis", test_files_exist),
        ("Version Python", test_python_version),
        ("Dépendances", test_imports),
        ("Import API", test_api_import),
        ("Dossiers", test_directories),
        ("Git", check_git_status),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Erreur pendant '{name}': {e}\n")
            results.append((name, False))
    
    # Résumé
    print("=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    print()
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
    
    print()
    print(f"Résultat: {passed}/{total} tests passés")
    print()
    
    if passed == total:
        print("=" * 60)
        print("🎉 TOUT EST PRÊT POUR LE DÉPLOIEMENT!")
        print("=" * 60)
        print()
        print("📋 Prochaines étapes:")
        print("  1. Exécutez: setup_github.bat")
        print("  2. Créez un repo sur GitHub")
        print("  3. Poussez le code")
        print("  4. Déployez sur Render.com")
        print()
        print("📖 Guide détaillé: DEPLOYMENT_GUIDE.md")
        print()
        return 0
    else:
        print("=" * 60)
        print("⚠️ QUELQUES PROBLÈMES À RÉSOUDRE")
        print("=" * 60)
        print()
        print("Corrigez les erreurs ci-dessus avant de déployer.")
        print()
        return 1


if __name__ == "__main__":
    exit_code = main()
    
    print("Appuyez sur Entrée pour fermer...")
    input()
    
    sys.exit(exit_code)

