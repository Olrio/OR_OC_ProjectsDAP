# Premiers éléments du script P2

# importation des modules nécessaires à l'ETL
import urllib.request
from requests import get
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.request import urlretrieve
import csv
import os

# récupération dans une variable de l'url de la page HTML à traiter
url = "http://books.toscrape.com/catalogue/red-hoodarsenal-vol-1-open-for-business-red-hoodarsenal-1_729/index.html"


# utilisation du package BeautifulSoup pour récupérer le contenu parsé de la page HTML
page = get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# dictionnaire de correspondance nombre texte/valeur
dico_number = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

# création sous forme de listes des variables correspondant aux champs requis
product_page_url = []
universal_product_code = []
title = []
price_including_tax = []
price_excluding_tax = []
number_available = []
product_description = []
category = []
review_rating = []
image_url = []

# enregistrement du fichier image du livre dans une liste
liste_file_images = []


# récupération des différentes infos du livre via les méthodes de BeautifulSoup
# il est parfois nécessaire de récupérer une valeur dans une balise qui suit une balise dont la valeur est connue


product_page_url.append(url)
universal_product_code.append(soup.find("th", text = "UPC").find_next("td").text)
title.append(soup.find("title").text.split("|")[0].strip())
price_including_tax.append(soup.find("th", text = "Price (incl. tax)").find_next("td").text)
price_excluding_tax.append(soup.find("th", text = "Price (excl. tax)").find_next("td").text)
number_available.append(soup.find("th", text = "Availability").find_next("td").text)
try:
    product_description.append(soup.find(id = "product_description").find_next("p").text)
except AttributeError:
    product_description.append("")
category.append(soup.find("a", text = "Books").find_next("a").text)
review_rating_texte = soup.find("p", {'class': lambda x: "star-rating" in x.split()})["class"].pop()
review_rating.append(dico_number[review_rating_texte])
image_url.append(urljoin(url, soup.find("img")["src"]))

nom_image = soup.find("img")["alt"]
try:
    nom_image = nom_image.replace("/#", "_")
except:
    pass
print(type(nom_image))
print(nom_image)
# toutes les variables ci-dessus devront constituer les en-têtes d'un fichier csv
liste_en_tetes = []
liste_en_tetes.extend([
    "product_page_url",
    "universal_product_code (upc)",
    "title",
    "price_including_tax",
    "price_excluding_tax",
    "number_available",
    "product_description",
    "category",
    "review_rating",
    "image_url",
    ])

#création d'un répertoire correspondant à la catégorie explorée
# on y stocke le fichier csv avec les infos du livre
# et le fichier image du livre
repcat = category[-1]
os.makedirs(repcat, exist_ok=True)

# récupération du fichier image
file_images = urllib.request.urlretrieve(urljoin(url, soup.find("img")["src"]),f"{repcat}/{nom_image}.jpg")
liste_file_images.append(file_images)

# création du fichier csv
with open(f'{repcat}/P2books.csv', 'w', encoding = 'utf8') as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=',')
    writer.writerow(liste_en_tetes)

    for c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 in zip(product_page_url,
                                                       universal_product_code,
                                                       title,
                                                       price_including_tax,
                                                       price_excluding_tax,
                                                       number_available,
                                                       product_description,
                                                       category,
                                                       review_rating,
                                                       image_url):
        ligne = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]
        writer.writerow(ligne)
    
