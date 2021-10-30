## OR_OC_ProjectsDAP

### Présentation du script

Le programme bookscraper.py utilise la technique de Web scraping pour le site [books.toscrape.com](http://books.toscrape.com).  

Le script parcourt toutes les catégories de livres du site.  

Pour chaque catégorie, il parcourt la page web de chaque livre de la catégorie et en extrait différentes informations via le module BeautifulSoup.  

Les informations extraites sont enregistrées dans un fichier csv à raison d'un fichier csv par catégorie.  

Un répertoire est créé dans le répertoire de travail de l'utilisateur pour chaque catégorie de livres.  

Sont enregistrés dans ce répertoire :
* le fichier csv avec les data de tous les livres de la catégorie
* le fichier image de chaque livre de la catégorie

Le script propose initialement à l'utilisateur de choisir si il souhaite extraire des données pour un seul livre, une catégorie de livres, ou pour tous les livres du site.
      
### Création et activation d'un environnement virtuel (procédure sous linux)

Se placer dans le répertoire de travail (existant ou à créer).  
  
Créer un clone du repository au moyen de la commande `git clone https://github.com/Olrio/OR_OC_ProjectsDAP`  

Créer un environnement virtuel au moyen de la commande : `python -m venv env` 

Activer cet environnement virtuel  avec : `source env/bin/activate`    

Y installer les modules nécessaires à partir du fichier *requirements.txt* : `pip install -r requirements.txt` 

Lancer l'exécution du programme *bookscraper.py* au moyen de la commande : `python bookscraper.py`  
