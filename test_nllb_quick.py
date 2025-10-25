#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Rapide NLLB - Vérification de l'installation et du fonctionnement
"""

import sys
from pathlib import Path

def test_imports():
    """Tester les imports"""
    print("="*60)
    print("🔍 TEST 1: Vérification des dépendances")
    print("="*60)
    print()
    
    try:
        import transformers
        print(f"✅ transformers: {transformers.__version__}")
    except ImportError as e:
        print(f"❌ transformers: {e}")
        return False
    
    try:
        import torch
        print(f"✅ torch: {torch.__version__}")
        print(f"   GPU disponible: {'Oui 🎉' if torch.cuda.is_available() else 'Non (CPU)'}")
    except ImportError as e:
        print(f"❌ torch: {e}")
        return False
    
    try:
        import sentencepiece
        print(f"✅ sentencepiece: OK")
    except ImportError as e:
        print(f"❌ sentencepiece: {e}")
        return False
    
    try:
        from langdetect import detect
        print(f"✅ langdetect: OK")
    except ImportError as e:
        print(f"⚠️  langdetect: {e} (optionnel)")
    
    try:
        from tqdm import tqdm
        print(f"✅ tqdm: OK")
    except ImportError as e:
        print(f"❌ tqdm: {e}")
        return False
    
    print()
    return True


def test_traducteur():
    """Tester l'initialisation du traducteur"""
    print("="*60)
    print("🔍 TEST 2: Initialisation du traducteur NLLB")
    print("="*60)
    print()
    
    try:
        from traduire_nllb import TraducteurNLLB
        
        print("📦 Chargement du modèle (peut prendre quelques minutes)...")
        print()
        
        traducteur = TraducteurNLLB()
        
        print()
        print("✅ Traducteur initialisé avec succès!")
        print()
        
        return traducteur
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_traduction_simple(traducteur):
    """Tester une traduction simple"""
    print("="*60)
    print("🔍 TEST 3: Traduction simple")
    print("="*60)
    print()
    
    textes_test = [
        "Bonjour, comment allez-vous?",
        "Je suis très content de vous rencontrer.",
        "La langue créole haïtienne est magnifique.",
    ]
    
    for i, texte in enumerate(textes_test, 1):
        print(f"Test {i}/3:")
        print(f"  FR: {texte}")
        
        try:
            traduction = traducteur.traduire(
                texte,
                langue_source='fr',
                langue_cible='ht',
                taille_chunk=100
            )
            print(f"  HT: {traduction}")
            print(f"  ✅ OK")
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
            return False
        
        print()
    
    print("✅ Traductions simples réussies!")
    print()
    return True


def test_fichier():
    """Tester la traduction d'un fichier"""
    print("="*60)
    print("🔍 TEST 4: Traduction de fichier")
    print("="*60)
    print()
    
    fichier_test = Path("data/test_nllb.txt")
    
    if not fichier_test.exists():
        print(f"⚠️  Fichier de test introuvable: {fichier_test}")
        print("   Test ignoré")
        print()
        return True
    
    print(f"📄 Fichier: {fichier_test}")
    print()
    
    try:
        # Lire le fichier
        with open(fichier_test, 'r', encoding='utf-8') as f:
            texte = f.read()
        
        print(f"✅ Fichier lu: {len(texte)} caractères")
        print()
        
        # Afficher un extrait
        print("📝 Extrait du texte original:")
        print("-" * 60)
        print(texte[:200] + "...")
        print("-" * 60)
        print()
        
        print("✅ Test de lecture réussi!")
        print()
        print("💡 Pour tester la traduction complète, lancez:")
        print(f"   python traduire_nllb.py {fichier_test}")
        print()
        
        return True
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


def main():
    """Fonction principale"""
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║  🇭🇹 TEST RAPIDE NLLB - TRADUCTION CRÉOLE HAÏTIEN  🇭🇹   ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()
    
    # Test 1: Imports
    if not test_imports():
        print("\n❌ Tests échoués: Dépendances manquantes")
        print("\nInstallez les dépendances:")
        print("  pip install transformers torch sentencepiece langdetect tqdm")
        return 1
    
    # Test 2: Initialisation
    print("\n⚠️  NOTE: Le test suivant va télécharger le modèle NLLB")
    print("   (~2.5 GB) lors de la première exécution.")
    print()
    input("Appuyez sur ENTRÉE pour continuer (ou Ctrl+C pour annuler)...")
    print()
    
    traducteur = test_traducteur()
    if not traducteur:
        print("\n❌ Tests échoués: Impossible d'initialiser le traducteur")
        return 1
    
    # Test 3: Traduction simple
    if not test_traduction_simple(traducteur):
        print("\n❌ Tests échoués: Traductions simples")
        return 1
    
    # Test 4: Fichier
    if not test_fichier():
        print("\n❌ Tests échoués: Traduction de fichier")
        return 1
    
    # Résumé
    print("="*60)
    print("✅ TOUS LES TESTS RÉUSSIS! 🎉")
    print("="*60)
    print()
    print("📚 Prochaines étapes:")
    print("   1. Lire le guide: NLLB_GUIDE.md")
    print("   2. Tester avec vos fichiers:")
    print("      python traduire_nllb.py votre_fichier.txt")
    print("   3. Ou utiliser le batch file:")
    print("      TRADUIRE_NLLB.bat votre_fichier.txt")
    print()
    print("🎯 Conseils:")
    print("   • Commencez avec le modèle 'distilled' (par défaut)")
    print("   • Utilisez 'medium' pour meilleure qualité")
    print("   • GPU recommandé pour fichiers volumineux")
    print()
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrompus")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

