"""
Project P2
This script uses the 'requests' and 'BeautifulSoup' libraries for a web_scraping process
From the website books.toscrape.com, the script extracts some data on a book.
Data collected are (UPC, title, price, description, file image, ...)
This is done for every books of a category and for every categories of the website
All collected data are registered in a csv file on a local directory on the user's machine
One subdirectory is created for each category
The files of the images of all the books in a category are stored in the dedicated subdirectory
"""

import csv
import os
import re
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from requests import get
from what_to_scrape import InputUrl
from Errors_management.get_error import GestError
from scrap_book import Book


def main():
    """main for poo version"""

    class Category:
        def __init__(self, url, books=None, Books=None):
            if Books is None:
                Books = []
            if books is None:
                books = []
            self.category_url = url
            self.category_dir = url.split("/")[-2]
            self.books = books
            self.Books = Books
            self.soup_category = BeautifulSoup(get(self.category_url).content, 'html.parser')
            self.books.extend([i.find("a")["href"] for i in self.soup_category.find_all("article")])
            self.Books.extend([Book(urljoin(self.category_url, i.find("a")["href"])) for i in self.soup_category.find_all("article")])

            if self.soup_category.find("li", class_="next"):
                self.next_url = urljoin(self.category_url, self.soup_category.find("li", class_="next").find_next("a")["href"])
                Category(self.next_url, self.books, self.Books)
            else:
               pass
            File_csv(self.Books, self.category_dir)

    class Site:
        def __init__(self, url):
            self.site_url = url
            self.soup_site = BeautifulSoup(get(self.site_url).content, 'html.parser')
            for i in self.soup_site.find("ul", class_="nav").find_next("ul").find_all("a"):
                Category(urljoin(self.site_url, i["href"]))


    class FileCsv:
        def __init__(self, Books, category):
            self.Books = Books
            self.category = category
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

            with open(f'./Web_scraper/{self.category}/P2books_{self.category}.csv', 'w', encoding='utf8') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(list_headers)
                for book in self.Books:
                    writer.writerow([book.product_page_url,
                             book.upc,
                             book.title,
                             book.price_including_tax,
                             book.price_excluding_tax,
                             book.number_available,
                             book.product_description,
                             book.category,
                             book.review_rating,
                             book.image_url,
                             book.file_image])

    url_scrap = InputUrl().display_choice()
    GestError(url_scrap).test_url()

    if url_scrap == "https://books.toscrape.com" \
            or url_scrap == "https://books.toscrape.com/index.html"\
            or "/category/books_1" in url_scrap:  # scraping the whole site
        Site("https://books.toscrape.com")
    elif "category/books/" not in url_scrap:  # scraping only one book on the site
        book = Book(url_scrap)
        FileCsv([book], book.category_dir)
    else:
        Category(url_scrap)


if __name__ == "__main__":
    """Entry of the program"""
    main()
