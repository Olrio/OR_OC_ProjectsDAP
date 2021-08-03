# Project P2
# This script uses the 'requests' and 'BeautifulSoup' libraries for a web_scraping process
# From the website books.toscrape.com, the script extracts some data on a book.
# Data collected are (UPC, title, price, description, file image, ...)
# This is done for every books of a category and for every categories of the website
# All collected data are registered in a csv file on a local directory on the user's machine
# One subdirectory is created for each category
# The files of the images of all the books in a category are stored in the dedicated subdirectory

import csv
import os
import re
# importation of necessary libraries for ETL
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from requests import get


def get_url_categories(page):
    # get the URL's of all categories of books and store them in a list
    soup_categories = BeautifulSoup(page.content, 'html.parser')
    url_raw_categories = [i["href"] for i in soup_categories.find("ul", class_="nav").find_next("ul").find_all("a")]
    return url_raw_categories


def get_url_books(page, url, books):
    # get the URL's of all books in the category and store them in a list
    soup_books = BeautifulSoup(page.content, 'html.parser')
    books.extend([i.find("a")["href"] for i in soup_books.find_all("article")])
    if soup_books.find("li", class_="next"):
        next_url_raw = soup_books.find("li", class_="next").find_next("a")["href"]
        next_url = transfo_url(url, next_url_raw)
        next_page = get(next_url)
        get_url_books(next_page, next_url, books=books)
    else:
        pass
    return books

def get_data_book(page, url):
    # get all the required data on a book and store them in a dictionary
    soup_book = BeautifulSoup(page.content, 'html.parser')
    book_dict = dict()
    book_dict["product_page_url"] = url
    book_dict["universal_product_code"] = soup_book.find("th", text="UPC").find_next("td").text
    book_dict["title"] = soup_book.find("title").text.split("|")[0].strip()
    book_dict["price_including_tax"] = soup_book.find("th", text="Price (incl. tax)").find_next("td").text
    book_dict["price_excluding_tax"] = soup_book.find("th", text="Price (excl. tax)").find_next("td").text
    book_dict["number_available"] = soup_book.find("th", text="Availability").find_next("td").text
    try:
        book_dict["product_description"] = soup_book.find(id="product_description").find_next("p").text
    except AttributeError:
        book_dict["product_description"] = ""
    book_dict["category"] = soup_book.find("a", text="Books").find_next("a").text

    book_dict["review_rating"] = soup_book.find("p", {'class': lambda x: "star-rating" in x.split()})["class"].pop()
    book_dict["image_url"] = urljoin(url, soup_book.find("img")["src"])
    book_dict["file_image"] = soup_book.find("img")["src"]
    return book_dict


def get_file_image(name, url_image, url, url_category):
    # get the image_file of the book on the web
    # save this in a local directory with an evocative name
    file_image = urllib.request.urlretrieve(urljoin(url, url_image),
                                            f'./Web_scraper/{url_category.split("/")[-2]}/{name}.jpg')
    return file_image


def transfo_url(url, url_raws):
    # transformation of  relative url in absolute url
    if type(url_raws) == list:
        return [urljoin(url, url_raw) for url_raw in url_raws]
    elif type(url_raws) == str:
        return urljoin(url, url_raws)


def transfo_data_book(raw_data_book, url, url_category):
    # modification of the file_image name with no special characters
    # matching literal and numeric numbers for review_rating
    # add quotes to the path of the file_image in csv for further use in terminal
        raw_data_book["image_url"] = transfo_url(url, raw_data_book["image_url"])
        name_image = re.sub('[<>/:"|?*,\\\\]', "_", raw_data_book["title"])
        file_image = get_file_image(name_image, raw_data_book["file_image"], url, url_category)
        raw_data_book["file_image"] = '"' + os.path.join(os.getcwd(), file_image[0]) + '"'
        number_dict = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        raw_data_book["review_rating"] = number_dict[raw_data_book["review_rating"]]
        return raw_data_book


def create_directory(name):
    # create a directory where all files related to a category are stored
    os.makedirs("./Web_scraper/" + name.split("/")[-2], exist_ok=True)


def create_csv(dictionary, name):
    # write in a new csv_file
    # all variables under are headers in the created file
    nom_cat = name.split("/")[-2]

    list_headers = ["product_page_url",
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
                    ]

    with open(f'./Web_scraper/{nom_cat}/P2books_{nom_cat}.csv', 'w', encoding='utf8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(list_headers)
        for book in dictionary.values():
            writer.writerow(book.values())


def main():
    # main function of the program
    URL_HOME = "http://books.toscrape.com"
    page_categories = get(URL_HOME)
    url_raw_categories = get_url_categories(page_categories)
    url_categories = transfo_url(URL_HOME, url_raw_categories)
    for url_category in url_categories:
        category_raw_dict = dict()
        category_dict = dict()
        page_books = get(url_category)
        create_directory(url_category)
        url_raw_books = get_url_books(page_books, url_category, books=[])
        url_books = transfo_url(url_category, url_raw_books)
        for url_book in url_books:
            page_book = get(url_book)
            category_raw_dict[url_books.index(url_book)] = get_data_book(page_book, url_book)
            category_dict[url_books.index(url_book)] = transfo_data_book(category_raw_dict[url_books.index(url_book)],
                                                                         url_book, url_category)
            print(url_book)
        create_csv(category_dict, url_category)


if __name__ == "__main__":
    # entry of the program
    main()
