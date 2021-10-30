
import csv
import os
import re
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from requests import get
from what_to_scrape import InputUrl
from Errors_management.get_error import GestError

class Book:
    """Management of data related to one book"""

    def __init__(self, url):
        """Initiate a book defined by its url"""
        self.product_page_url = url

    def get_data_book(self):
        DataBook(self.product_page_url)



            self.soup_book = BeautifulSoup(get(self.product_page_url).content, 'html.parser')
            self.title = self.soup_book.find("title").text.split("|")[0].strip()
            self.upc = self.soup_book.find("th", text="UPC").find_next("td").text
            self.price_including_tax = self.soup_book.find("th", text="Price (excl. tax)").find_next("td").text
            self.price_excluding_tax = self.soup_book.find("th", text="Price (excl. tax)").find_next("td").text
            self.number_available = self.soup_book.find("th", text="Availability").find_next("td").text
            try:
                self.product_description = self.soup_book.find(id="product_description").find_next("p").text
            except AttributeError:
                self.product_description = ""
            self.category = self.soup_book.find("a", text="Books").find_next("a").text
            self.category_dir = self.soup_book.find("a", text="Books").find_next("a")["href"].split("/")[-2]
            self.review_rating = {"One": 1, "Two": 2, "Three": 3, "Four": 4,
                                  "Five": 5}[self.soup_book.find("p",
                                                   {'class': lambda x: "star-rating" in x.split()})["class"].pop()]
            self.image_url = urljoin(self.product_page_url, self.soup_book.find("img")["src"])
            self.file_image_name = re.sub('[<>/:"|?*,\\\\]', "_", self.title)
            os.makedirs("./Web_scraper/" + self.category_dir, exist_ok=True)
            self.file_image = '"' + os.path.join(os.getcwd(),
                                                 urllib.request.urlretrieve(urljoin(self.product_page_url, self.image_url),
                                            f'''./Web_scraper/{self.category_dir}/{self.file_image_name}.jpg''')[0]) + '"'
            self.list_books = [self]
            print(self.title)