# Projet P2

# Boucle sur la liste des catégories de livres identifiée via BeautifulSoup
# Pour chaque catégorie, on appelle la fonction listebooks() de la v2
# Et la fonction listebooks() appelle elle-même chaque livre de la catégorie via la fonction infobook()

import csv
import os
import re
# importation des modules nécessaires à l'ETL
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from requests import get


def listebooks(url):
    # recense l'url associée à chaque page web de description d'un livre de la catégorie
    # si il y a plusieurs pages web pour cette catégorie, la fonction boucle récursivement
    page_cat = get(url)
    soup_cat = BeautifulSoup(page_cat.content, 'html.parser')
    liste_cat_books = soup_cat.find_all("article")
    for i in liste_cat_books:
        url_book = urljoin(url, i.find("a")["href"])
        infobook(url_book)
    if (soup_cat.find("li", class_="next")):
        suffixe = soup_cat.find("li", class_="next").find_next("a")["href"]
        url_cat = f"http://books.toscrape.com/catalogue/category/books/{nom_cat}/{suffixe}"
        listebooks(url_cat)
    else:
        return

def infobook(url):
    # utilisation du package BeautifulSoup pour récupérer le contenu parsé de la page HTML
    # récupération des différentes infos du livre via les méthodes de BeautifulSoup
    # il est parfois nécessaire de récupérer une valeur dans une balise qui suit une balise dont la valeur est connue
    global nom_cat
    # dictionnaire de correspondance nombre texte/valeur pour le 'view_rating'
    dico_number = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    
    page = get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
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

    # récupération du fichier image
    
    print(nom_image)
    for i in nom_image:
        if i in '<>\/:"|?*':
            nom_image = nom_image.replace(i, "_")
    print(nom_image)

    file_images = urllib.request.urlretrieve(urljoin(url, soup.find("img")["src"]), f"./Webscrapper/{nom_cat}/{nom_image}.jpg")
    liste_file_images.append(os.path.join(os.getcwd(), file_images[0]))

def listecateg():
    # cette première fonction défibit une certain nombre de variables utilisées ultérieurement dans les fonctions listebooks() et infobook()
    # on les déclare donc en global
    global product_page_url, \
       universal_product_code, \
       title, \
       price_including_tax,\
       price_excluding_tax,\
       number_available,\
       product_description,\
       category,\
       review_rating,\
       image_url,\
       nom_cat,\
       liste_file_images
        
    # on récupère dans la page 'home' la liste des catégories de livres
    # le programme va itérer sur cette liste
    url_allcat = "http://books.toscrape.com"
    page_allcat = get(url_allcat)
    soup_allcat = BeautifulSoup(page_allcat.content, 'html.parser')
    liste_allcat = soup_allcat.find_all("a", href = re.compile("catalogue/category/books/"))

    for i in liste_allcat:
        nom_cat = i["href"].split("/")[3]
        # création d'un répertoire correspondant à la catégorie explorée (si il n'existe pas)
        # on y stocke le fichier csv avec les infos du livre
        # et le fichier image du livre
        os.makedirs("./Webscrapper/" + nom_cat, exist_ok=True)
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

        # on débute par la page 1 identifiée comme 'index'
        # si il y a plusieurs pages web de la même catégorie, on remplacera 'index' par 'page-x'
        suffixe = "index"
        url_cat = f"http://books.toscrape.com/catalogue/category/books/{nom_cat}/{suffixe}.html"
        listebooks(url_cat)

        # écriture dans le fichier csv
        # toutes les variables ci-dessous devront constituer les en-têtes d'un fichier csv
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
            "file_image"
            ])

        with open(f'./Webscrapper/{nom_cat}/P2books_{nom_cat}.csv', 'w', encoding='utf8') as fichier_csv:
            writer = csv.writer(fichier_csv, delimiter=',')
            writer.writerow(liste_en_tetes)
            for c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11 in zip(product_page_url,
                                                                    universal_product_code,
                                                                    title,
                                                                    price_including_tax,
                                                                    price_excluding_tax,
                                                                    number_available,
                                                                    product_description,
                                                                    category,
                                                                    review_rating,
                                                                    image_url,
                                                                    liste_file_images
                                                                    ):
                ligne = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11]
                writer.writerow(ligne)

def main():
    # fonction centrale du programme
    # main() appelle listecateg(), qui recense toutes les catégories de livres
    listecateg()



if __name__ == "__main__":
    main()