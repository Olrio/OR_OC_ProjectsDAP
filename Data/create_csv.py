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