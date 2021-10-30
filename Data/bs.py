from urllib.parse import urljoin
from bs4 import BeautifulSoup
from requests import get
from Data.transfo import TransformDataBook


class DataBook:
    """Use BeautifulSoup to get raw data related to a book"""
    """Return data to Book as a definition of its attributes"""

    def __init__(self, url):
        self.url = url
        self.soup_book = BeautifulSoup(get(self.url).content, 'html.parser')
        self.nb_stars = None

    def get_book_title(self):
        return self.soup_book.find("title").text.split("|")[0].strip()

    def get_book_upc(self):
        if self.soup_book.find("th", text="UPC"):
            return self.soup_book.find("th", text="UPC").find_next("td").text
        else:
            return ""

    def get_book_price_including_tax(self):
        if self.soup_book.find("th", text="Price (excl. tax)"):
            return self.soup_book.find("th", text="Price (excl. tax)").find_next("td").text
        else:
            return ""

    def get_book_price_excluding_tax(self):
        if self.soup_book.find("th", text="Price (excl. tax)"):
            return self.soup_book.find("th", text="Price (excl. tax)").find_next("td").text
        else:
            return ""

    def get_number_available(self):
        if self.soup_book.find("th", text="Availability"):
            return self.soup_book.find("th", text="Availability").find_next("td").text
        else:
            return ""

    def get_product_description(self):
        if self.soup_book.find(id="product_description"):
            return self.soup_book.find(id="product_description").find_next("p").text
        else:
            return ""

    def get_category(self):
        if self.soup_book.find("a", text="Books"):
            return self.soup_book.find("a", text="Books").find_next("a").text
        else:
            return ""

    def get_category_dir(self):
        if self.soup_book.find("a", text="Books"):
            return self.soup_book.find("a", text="Books").find_next("a")["href"].split("/")[-2]
        else:
            return "No category"

    def get_review_rating(self):
        if self.soup_book.find("p", class_=lambda x: "star-rating" in x):
            self.nb_stars = TransformDataBook(self.url).transform_review_rating(
                self.soup_book.find("p", class_=lambda x: "star-rating" in x).get("class")[1])
            return self.nb_stars
        else:
            return ""

    def get_image_url(self):
        if self.soup_book.find("img")["src"]:
            return urljoin(self.url, self.soup_book.find("img")["src"])
        else:
            return ""
