#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Traduction avec NLLB - Pwojè Kreyòl IA
Tradiksyon ak modèl Meta NLLB pou pi bon kalite

Utilise le modèle NLLB (No Language Left Behind) de Meta
pour des traductions de haute qualité vers le créole haïtien.
"""

import sys
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tqdm import tqdm
import torch

class TraducteurNLLB:
    """Traducteur utilisant le modèle NLLB de Meta"""
    
    def __init__(self, modele="facebook/nllb-200-distilled-600M"):
        """
        Initialiser le traducteur NLLB
        
        Modèles disponibles:
        - facebook/nllb-200-distilled-600M (600M params - recommandé, ~2.5GB)
        - facebook/nllb-200-1.3B (1.3B params - meilleure qualité, ~5GB)
        - facebook/nllb-200-3.3B (3.3B params - excellente qualité, ~13GB)
        """
        print(f"🔄 Chargement du modèle NLLB: {modele}")
        print("   (Première utilisation: téléchargement automatique)")
        print()
        
        self.tokenizer = AutoTokenizer.from_pretrained(modele)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(modele)
        
        # Utiliser GPU si disponible
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        
        print(f"✅ Modèle chargé sur: {self.device.upper()}")
        if self.device == "cpu":
            print("   ⚠️  GPU non disponible - traduction plus lente sur CPU")
        print()
        
        # Codes de langue NLLB
        self.codes_langue = {
            'fr': 'fra_Latn',  # Français
            'en': 'eng_Latn',  # Anglais
            'ht': 'hat_Latn',  # Créole Haïtien
            'es': 'spa_Latn',  # Espagnol
            'pt': 'por_Latn',  # Portugais
            'de': 'deu_Latn',  # Allemand
        }
    
    def traduire(self, texte, langue_source='auto', langue_cible='ht', 
                 taille_chunk=500):
        """
        Traduire un texte
        
        Args:
            texte: Texte à traduire
            langue_source: Code langue source ('fr', 'en', 'auto')
            langue_cible: Code langue cible ('ht' pour créole)
            taille_chunk: Taille des segments (en mots)
        
        Returns:
            str: Texte traduit
        """
        # Détecter langue source si auto
        if langue_source == 'auto':
            langue_source = self._detecter_langue(texte)
        
        # Convertir en codes NLLB
        src_lang = self.codes_langue.get(langue_source, 'fra_Latn')
        tgt_lang = self.codes_langue.get(langue_cible, 'hat_Latn')
        
        print(f"🌍 Traduction: {src_lang} → {tgt_lang}")
        print(f"   Texte: {len(texte)} caractères, {len(texte.split())} mots")
        
        # Diviser en chunks par phrases
        chunks = self._diviser_texte(texte, taille_chunk)
        print(f"   Division en {len(chunks)} segment(s)")
        print()
        
        # Traduire chaque chunk
        traductions = []
        with tqdm(total=len(chunks), desc="🔄 Traduction", unit="segment") as pbar:
            for chunk in chunks:
                try:
                    traduction = self._traduire_chunk(chunk, src_lang, tgt_lang)
                    traductions.append(traduction)
                except Exception as e:
                    print(f"\n⚠️  Erreur sur segment: {e}")
                    traductions.append(chunk)  # Garder l'original en cas d'erreur
                
                pbar.update(1)
        
        texte_final = " ".join(traductions)
        print(f"\n✅ Traduction terminée: {len(texte_final)} caractères")
        
        return texte_final
    
    def _detecter_langue(self, texte):
        """Détecter la langue du texte"""
        try:
            from langdetect import detect
            lang_detectee = detect(texte[:1000])  # Analyser les 1000 premiers caractères
            
            if lang_detectee in self.codes_langue:
                print(f"🔍 Langue détectée: {lang_detectee.upper()}")
                return lang_detectee
            else:
                print(f"🔍 Langue détectée: {lang_detectee} (non supportée)")
                print("   Utilisation du français par défaut")
                return 'fr'
        except ImportError:
            print("⚠️  langdetect non installé - utilisation du français par défaut")
            print("   Installez avec: pip install langdetect")
            return 'fr'
        except Exception as e:
            print(f"⚠️  Erreur de détection: {e}")
            print("   Utilisation du français par défaut")
            return 'fr'
    
    def _diviser_texte(self, texte, taille_chunk):
        """Diviser le texte en chunks intelligents par phrases"""
        import re
        
        # Séparer par phrases (conserve les délimiteurs)
        phrases = re.split(r'([.!?]+\s+)', texte)
        
        chunks = []
        chunk_actuel = []
        mots_actuel = 0
        
        for i, phrase in enumerate(phrases):
            mots = len(phrase.split())
            
            # Si on dépasse la taille, créer un nouveau chunk
            if mots_actuel + mots > taille_chunk and chunk_actuel:
                chunks.append("".join(chunk_actuel))
                chunk_actuel = []
                mots_actuel = 0
            
            chunk_actuel.append(phrase)
            mots_actuel += mots
        
        # Ajouter le dernier chunk
        if chunk_actuel:
            chunks.append("".join(chunk_actuel))
        
        return chunks if chunks else [texte]
    
    def _traduire_chunk(self, texte, src_lang, tgt_lang):
        """Traduire un segment de texte"""
        # Préparer l'entrée
        self.tokenizer.src_lang = src_lang
        inputs = self.tokenizer(
            texte, 
            return_tensors="pt", 
            padding=True, 
            truncation=True, 
            max_length=512
        )
        
        # Déplacer sur le device (GPU/CPU)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Générer la traduction
        with torch.no_grad():  # Désactiver le calcul des gradients
            translated_tokens = self.model.generate(
                **inputs,
                forced_bos_token_id=self.tokenizer.lang_code_to_id[tgt_lang],
                max_length=512,
                num_beams=5,  # Beam search pour meilleure qualité
                early_stopping=True
            )
        
        # Décoder
        traduction = self.tokenizer.batch_decode(
            translated_tokens, 
            skip_special_tokens=True
        )[0]
        
        return traduction


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


def afficher_aide():
    """Afficher l'aide"""
    print("="*60)
    print("🇭🇹 TRADUCTION NLLB - CRÉOLE HAÏTIEN")
    print("="*60)
    print()
    print("Usage: python traduire_nllb.py <fichier.txt> [options]")
    print()
    print("Arguments:")
    print("  <fichier.txt>    Fichier texte à traduire")
    print()
    print("Options:")
    print("  --modele MODEL   Modèle NLLB à utiliser")
    print("                   - distilled (défaut, ~2.5GB)")
    print("                   - medium (~5GB)")
    print("                   - large (~13GB)")
    print()
    print("  --chunk SIZE     Taille des segments (défaut: 500 mots)")
    print()
    print("Exemples:")
    print("  python traduire_nllb.py data/test_document.txt")
    print("  python traduire_nllb.py mon_livre.txt --modele medium")
    print("  python traduire_nllb.py texte.txt --chunk 300")
    print()
    print("Modèles NLLB disponibles:")
    print("  • distilled : facebook/nllb-200-distilled-600M (rapide)")
    print("  • medium    : facebook/nllb-200-1.3B (meilleure qualité)")
    print("  • large     : facebook/nllb-200-3.3B (excellente qualité)")
    print()


def main():
    """Fonction principale"""
    # Vérifier les arguments
    if len(sys.argv) < 2 or '--help' in sys.argv or '-h' in sys.argv:
        afficher_aide()
        return 0 if '--help' in sys.argv or '-h' in sys.argv else 1
    
    # Parser les arguments
    fichier_path = Path(sys.argv[1])
    
    # Options
    modele_map = {
        'distilled': 'facebook/nllb-200-distilled-600M',
        'medium': 'facebook/nllb-200-1.3B',
        'large': 'facebook/nllb-200-3.3B'
    }
    
    modele = 'facebook/nllb-200-distilled-600M'  # Défaut
    taille_chunk = 500  # Défaut
    
    # Parser options
    for i, arg in enumerate(sys.argv):
        if arg == '--modele' and i + 1 < len(sys.argv):
            modele_key = sys.argv[i + 1]
            if modele_key in modele_map:
                modele = modele_map[modele_key]
            else:
                print(f"⚠️  Modèle inconnu: {modele_key}")
                print(f"   Utilisation du modèle par défaut: distilled")
        
        if arg == '--chunk' and i + 1 < len(sys.argv):
            try:
                taille_chunk = int(sys.argv[i + 1])
            except ValueError:
                print(f"⚠️  Taille de chunk invalide: {sys.argv[i + 1]}")
                print(f"   Utilisation de la taille par défaut: 500")
    
    print("="*60)
    print("🇭🇹 TRADUCTION NLLB - CRÉOLE HAÏTIEN")
    print("="*60)
    print()
    
    # Vérifier que le fichier existe
    if not fichier_path.exists():
        print(f"❌ Fichier introuvable: {fichier_path}")
        print()
        print("Utilisez --help pour voir l'aide")
        return 1
    
    print(f"📖 Fichier source: {fichier_path.name}")
    print(f"🤖 Modèle: {modele.split('/')[-1]}")
    print(f"📦 Taille des segments: {taille_chunk} mots")
    print()
    
    # ÉTAPE 1: Initialiser le traducteur
    try:
        traducteur = TraducteurNLLB(modele=modele)
    except Exception as e:
        print(f"❌ Erreur d'initialisation: {e}")
        print()
        print("Vérifiez que les dépendances sont installées:")
        print("  pip install transformers torch sentencepiece")
        print()
        print("Note: Le modèle sera téléchargé automatiquement")
        print("      lors de la première utilisation.")
        return 1
    
    # ÉTAPE 2: Lecture
    texte_original = lire_fichier(fichier_path)
    if not texte_original:
        return 1
    
    print()
    
    # ÉTAPE 3: Traduction
    try:
        texte_traduit = traducteur.traduire(
            texte_original,
            langue_source='auto',
            langue_cible='ht',
            taille_chunk=taille_chunk
        )
    except Exception as e:
        print(f"❌ Erreur de traduction: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # ÉTAPE 4: Sauvegarde
    nom_base = fichier_path.stem
    output_dir = Path("output") / f"{nom_base}_nllb"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Sauvegarder original et traduction
    original_path = output_dir / f"{nom_base}_original.txt"
    traduit_path = output_dir / f"{nom_base}_kreyol_nllb.txt"
    
    with open(original_path, 'w', encoding='utf-8') as f:
        f.write(texte_original)
    
    if not sauvegarder_fichier(texte_traduit, traduit_path):
        return 1
    
    # Résumé final
    print("\n" + "="*60)
    print("✅ TRADUCTION NLLB RÉUSSIE!")
    print("="*60)
    print(f"📄 Fichier original: {original_path}")
    print(f"🇭🇹 Fichier créole: {traduit_path}")
    print()
    print(f"📊 Statistiques:")
    mots_original = len(texte_original.split())
    mots_traduit = len(texte_traduit.split())
    print(f"   • Mots originaux: {mots_original:,}")
    print(f"   • Mots traduits: {mots_traduit:,}")
    print(f"   • Caractères originaux: {len(texte_original):,}")
    print(f"   • Caractères traduits: {len(texte_traduit):,}")
    print(f"   • Ratio mots: {mots_traduit/mots_original:.2f}x")
    print("="*60)
    
    # Afficher un extrait
    print("\n📝 Extrait de la traduction:")
    print("-" * 60)
    extrait = texte_traduit[:500]
    print(extrait + ("..." if len(texte_traduit) > 500 else ""))
    print("-" * 60)
    print()
    
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

