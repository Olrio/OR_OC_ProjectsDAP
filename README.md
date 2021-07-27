## OR_OC_ProjectsDAP

### Présentation du script

Le programme webscrapper_books.py est un webscrapper pour le site [books.toscrape.com](http://books.toscrape.com).  

Le script parcourt toutes les catégories de livres du site.  

Pour chaque catégorie, il parcourt la page web de chaque livre de la catégorie et en extrait différentes informations via le module BeautifulSoup.  

Les informations extraites sont enregistrées dans un fichier csv à raison d'un fichier csv par catégorie.  

Un répertoire est créé pour chaque catégorie de livres.  

Sont enregistrés dans ce répertoire :
* le fichier csv avec les datas de tous les livres de la catégorie
* le fichier image de chaque livre de la catégorie
      
### Création et activation d'un environnement virtuel

Dans le répertoire de travail, créer un environnement virtuel au moyen de la commande : `python -m venv env` 

Activer cet environnement virtuel  avec : `source env/bin/activate`    

Y installer les modules nécessaires à partir du fichier *requirements.txt* : `pip install -r requirements.txt` 

Lancer l'exécution du programme *webscrapper_books.py* au moyen de la commande : `python webscrapper_books.py`  
