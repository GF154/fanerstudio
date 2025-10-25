#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Simple de Traduction - Pwojè Kreyòl IA
Simple Translation Script
"""

import sys
from pathlib import Path
from deep_translator import GoogleTranslator
import pypdf

def extraire_texte_pdf(pdf_path):
    """Extraire le texte d'un PDF"""
    print(f"📄 Extraction du texte de: {pdf_path}")
    
    try:
        reader = pypdf.PdfReader(pdf_path)
        texte_complet = []
        
        for i, page in enumerate(reader.pages, 1):
            print(f"   Page {i}/{len(reader.pages)}...", end='\r')
            texte = page.extract_text()
            if texte.strip():
                texte_complet.append(texte)
        
        print(f"\n✅ {len(reader.pages)} pages extraites")
        return "\n\n".join(texte_complet)
    
    except Exception as e:
        print(f"❌ Erreur d'extraction: {e}")
        return None


def traduire_texte(texte, langue_cible='ht', taille_chunk=4500):
    """Traduire le texte en créole haïtien"""
    print(f"\n🌍 Traduction en créole haïtien...")
    print(f"   Taille du texte: {len(texte)} caractères")
    
    try:
        translator = GoogleTranslator(source='auto', target=langue_cible)
        
        # Diviser en chunks pour éviter les limites
        chunks = []
        for i in range(0, len(texte), taille_chunk):
            chunk = texte[i:i + taille_chunk]
            chunks.append(chunk)
        
        print(f"   Traduction en {len(chunks)} parties...")
        
        texte_traduit = []
        for i, chunk in enumerate(chunks, 1):
            print(f"   Partie {i}/{len(chunks)}...", end='\r')
            try:
                traduction = translator.translate(chunk)
                texte_traduit.append(traduction)
            except Exception as e:
                print(f"\n⚠️  Erreur partie {i}: {e}")
                texte_traduit.append(chunk)  # Garder l'original si erreur
        
        print(f"\n✅ Traduction terminée!")
        return "\n\n".join(texte_traduit)
    
    except Exception as e:
        print(f"❌ Erreur de traduction: {e}")
        return None


def sauvegarder_texte(texte, chemin_sortie):
    """Sauvegarder le texte traduit"""
    print(f"\n💾 Sauvegarde dans: {chemin_sortie}")
    
    try:
        chemin_sortie.parent.mkdir(parents=True, exist_ok=True)
        
        with open(chemin_sortie, 'w', encoding='utf-8') as f:
            f.write(texte)
        
        print(f"✅ Fichier sauvegardé: {chemin_sortie}")
        print(f"   Taille: {len(texte)} caractères")
        return True
    
    except Exception as e:
        print(f"❌ Erreur de sauvegarde: {e}")
        return False


def main():
    """Fonction principale"""
    print("="*60)
    print("🇭🇹 TRADUCTION DE DOCUMENT EN CRÉOLE HAÏTIEN")
    print("="*60)
    print()
    
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("Usage: python traduire_document.py <fichier.pdf>")
        print("\nOu placez votre PDF dans data/input.pdf et lancez sans argument")
        
        # Chercher data/input.pdf par défaut
        pdf_defaut = Path("data/input.pdf")
        if not pdf_defaut.exists():
            print(f"\n❌ Aucun fichier trouvé: {pdf_defaut}")
            return 1
        
        pdf_path = pdf_defaut
    else:
        pdf_path = Path(sys.argv[1])
    
    # Vérifier que le fichier existe
    if not pdf_path.exists():
        print(f"❌ Fichier introuvable: {pdf_path}")
        return 1
    
    print(f"📖 Document à traduire: {pdf_path.name}")
    print()
    
    # ÉTAPE 1: Extraction
    texte_original = extraire_texte_pdf(pdf_path)
    if not texte_original:
        return 1
    
    # Sauvegarder le texte original
    nom_base = pdf_path.stem
    output_dir = Path("output") / nom_base
    output_dir.mkdir(parents=True, exist_ok=True)
    
    texte_original_path = output_dir / f"{nom_base}_original.txt"
    with open(texte_original_path, 'w', encoding='utf-8') as f:
        f.write(texte_original)
    
    # ÉTAPE 2: Traduction
    texte_traduit = traduire_texte(texte_original, langue_cible='ht')
    if not texte_traduit:
        return 1
    
    # ÉTAPE 3: Sauvegarde
    texte_traduit_path = output_dir / f"{nom_base}_kreyol.txt"
    if not sauvegarder_texte(texte_traduit, texte_traduit_path):
        return 1
    
    # Résumé final
    print("\n" + "="*60)
    print("✅ TRADUCTION TERMINÉE AVEC SUCCÈS!")
    print("="*60)
    print(f"📄 Texte original: {texte_original_path}")
    print(f"🇭🇹 Texte créole: {texte_traduit_path}")
    print(f"📊 Statistiques:")
    print(f"   - Caractères originaux: {len(texte_original):,}")
    print(f"   - Caractères traduits: {len(texte_traduit):,}")
    print("="*60)
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Traduction interrompue par l'utilisateur")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

