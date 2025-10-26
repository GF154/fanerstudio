#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Créer un PDF de test pour démonstration
"""

from pathlib import Path

def creer_pdf_test():
    """Créer un fichier texte de test (si reportlab n'est pas disponible)"""
    
    texte_test = """
HISTOIRE COURTE - UNE BELLE JOURNÉE

C'était une belle matinée de printemps. Le soleil brillait dans le ciel bleu, 
et les oiseaux chantaient joyeusement dans les arbres. Marie se réveilla 
avec un grand sourire.

Elle regarda par la fenêtre et vit que le jardin était magnifique. Les fleurs 
roses et blanches étaient épanouies, et l'herbe verte semblait danser 
doucement dans la brise légère.

"Quelle merveilleuse journée!" s'exclama Marie. "Je vais aller me promener 
dans le parc."

Elle s'habilla rapidement, prit son chapeau de paille, et sortit de la maison. 
Dans la rue, elle rencontra son ami Pierre.

"Bonjour Marie!" dit Pierre avec enthousiasme. "Où vas-tu par cette belle 
journée?"

"Je vais au parc," répondit Marie. "Veux-tu m'accompagner?"

"Avec plaisir!" dit Pierre.

Ensemble, ils marchèrent vers le parc. En chemin, ils parlèrent de leurs rêves 
et de leurs espoirs pour l'avenir. C'était vraiment une belle journée pour 
passer du temps avec un bon ami.

Au parc, ils s'assirent sous un grand arbre et profitèrent de la beauté de la 
nature. Les enfants jouaient, les familles pique-niquaient, et tout le monde 
semblait heureux.

"La vie est belle," dit Marie en souriant.

"Oui," répondit Pierre. "Et les moments comme celui-ci sont précieux."

Ils restèrent au parc jusqu'au coucher du soleil, créant des souvenirs qui 
dureraient toute une vie.

FIN
    """
    
    # Créer le dossier data s'il n'existe pas
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Sauvegarder comme fichier texte
    txt_path = data_dir / "test_document.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(texte_test.strip())
    
    print("✅ Document de test créé:")
    print(f"   {txt_path}")
    print(f"   {len(texte_test)} caractères")
    
    return txt_path


if __name__ == "__main__":
    print("="*60)
    print("🇭🇹 CRÉATION D'UN DOCUMENT DE TEST")
    print("="*60)
    print()
    
    chemin = creer_pdf_test()
    
    print()
    print("📝 Pour traduire ce document:")
    print("   python traduire_texte.py data/test_document.txt")
    print()

