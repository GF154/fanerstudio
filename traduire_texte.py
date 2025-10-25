#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Traduction de Fichiers Texte - Pwojè Kreyòl IA
"""

import sys
from pathlib import Path
from deep_translator import GoogleTranslator
from tqdm import tqdm

def lire_fichier(chemin):
    """Lire un fichier texte"""
    print(f"📄 Lecture de: {chemin}")
    
    try:
        with open(chemin, 'r', encoding='utf-8') as f:
            texte = f.read()
        
        print(f"✅ Fichier lu: {len(texte)} caractères")
        return texte
    
    except Exception as e:
        print(f"❌ Erreur de lecture: {e}")
        return None


def traduire_avec_progress(texte, langue_cible='ht', taille_chunk=4500):
    """Traduire avec barre de progression"""
    print(f"\n🌍 Traduction en créole haïtien...")
    print(f"   Source: {len(texte)} caractères")
    
    try:
        translator = GoogleTranslator(source='auto', target=langue_cible)
        
        # Diviser en chunks
        chunks = []
        for i in range(0, len(texte), taille_chunk):
            chunk = texte[i:i + taille_chunk]
            chunks.append(chunk)
        
        print(f"   Division en {len(chunks)} partie(s)")
        print()
        
        # Traduire avec barre de progression
        texte_traduit = []
        
        with tqdm(total=len(chunks), desc="Traduction", unit="partie") as pbar:
            for chunk in chunks:
                try:
                    traduction = translator.translate(chunk)
                    texte_traduit.append(traduction)
                except Exception as e:
                    print(f"\n⚠️  Erreur: {e}")
                    texte_traduit.append(chunk)
                
                pbar.update(1)
        
        print()
        print(f"✅ Traduction terminée: {len(''.join(texte_traduit))} caractères")
        return "\n\n".join(texte_traduit)
    
    except Exception as e:
        print(f"❌ Erreur de traduction: {e}")
        return None


def sauvegarder_fichier(texte, chemin):
    """Sauvegarder le texte"""
    print(f"\n💾 Sauvegarde dans: {chemin}")
    
    try:
        chemin.parent.mkdir(parents=True, exist_ok=True)
        
        with open(chemin, 'w', encoding='utf-8') as f:
            f.write(texte)
        
        taille_ko = len(texte.encode('utf-8')) / 1024
        print(f"✅ Fichier sauvegardé: {taille_ko:.2f} Ko")
        return True
    
    except Exception as e:
        print(f"❌ Erreur de sauvegarde: {e}")
        return False


def main():
    """Fonction principale"""
    print("="*60)
    print("🇭🇹 TRADUCTION EN CRÉOLE HAÏTIEN")
    print("="*60)
    print()
    
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("Usage: python traduire_texte.py <fichier.txt>")
        print()
        print("Exemple:")
        print("  python traduire_texte.py data/test_document.txt")
        return 1
    
    fichier_path = Path(sys.argv[1])
    
    # Vérifier que le fichier existe
    if not fichier_path.exists():
        print(f"❌ Fichier introuvable: {fichier_path}")
        return 1
    
    print(f"📖 Fichier source: {fichier_path.name}")
    print()
    
    # ÉTAPE 1: Lecture
    texte_original = lire_fichier(fichier_path)
    if not texte_original:
        return 1
    
    # ÉTAPE 2: Traduction
    texte_traduit = traduire_avec_progress(texte_original, langue_cible='ht')
    if not texte_traduit:
        return 1
    
    # ÉTAPE 3: Sauvegarde
    nom_base = fichier_path.stem
    output_dir = Path("output") / nom_base
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Sauvegarder original et traduction
    original_path = output_dir / f"{nom_base}_original.txt"
    traduit_path = output_dir / f"{nom_base}_kreyol.txt"
    
    with open(original_path, 'w', encoding='utf-8') as f:
        f.write(texte_original)
    
    if not sauvegarder_fichier(texte_traduit, traduit_path):
        return 1
    
    # Résumé final
    print("\n" + "="*60)
    print("✅ TRADUCTION RÉUSSIE!")
    print("="*60)
    print(f"📄 Fichier original: {original_path}")
    print(f"🇭🇹 Fichier créole: {traduit_path}")
    print()
    print(f"📊 Statistiques:")
    mots_original = len(texte_original.split())
    mots_traduit = len(texte_traduit.split())
    print(f"   - Mots originaux: {mots_original:,}")
    print(f"   - Mots traduits: {mots_traduit:,}")
    print(f"   - Caractères originaux: {len(texte_original):,}")
    print(f"   - Caractères traduits: {len(texte_traduit):,}")
    print("="*60)
    
    # Afficher un extrait
    print("\n📝 Extrait de la traduction:")
    print("-" * 60)
    extrait = texte_traduit[:500]
    print(extrait + ("..." if len(texte_traduit) > 500 else ""))
    print("-" * 60)
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Traduction interrompue")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

