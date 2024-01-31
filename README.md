# e-Karoka
Moteur de recherche pour les theses malagasy, base sur le modele vectoriel et du Traitement du Langage Naturel (TLN).

Developpe avec Python utilisant le framework Django, et la librairie Spacy du TLN.

## Installation
### Pre-requis

- Python > 3 installe
- Pip
- MySQL > 5 ou MariaDB > 10

### Etape d'installation

1. Cloner le depot git
```bash
git clone https://github.com/rod-car/search-engine.git
```

2. Installer les dependances
```bash
cd sri
pip install -r requirements.txt
```

3. Migrer la base de donnees
```bash
python manage.py migrate
```

### Demarrer l'application
```bash
python manage.py runserver
```

## Fonctionnalites

### Deposer un document
Permet aux utilisateurs connecte de deposer directement leurs documents sur le plateforme, et de passer la validation de l'administrateur.

### Telecharger un document
Permet aux utilisateurs connecte de telecharcger les documents directement sur son appareil.

### Recherche avec filtres
Recherche avec la possibilite de filtrer par annee de soutenance, par universite, ainsi qu'une recherche par titre, auteur et contenu.

### Indexation des documents
Permet d'indexer les documents au format PDF, WORD et OpenOffice Word.

### Authentification et inscription
Permet aux utilisateurs d'avoir un acces total dans le systeme.

## Licence
MIT