from urllib.parse import urljoin
from bs4 import BeautifulSoup
from requests import get
from data.book import Book
from data.result import FileCsv


class Category:
    def __init__(self, url, books=None, class_books=None):
        self.books = books
        self.Books = class_books
        self.category_url = url
        self.category_dir = None
        self.soup_category = None
        self.next_url = None
        self.get_attributes()

    def get_attributes(self):
        if self.books is None:
            self.books = []
        if self.Books is None:
            self.Books = []
        self.category_dir = self.category_url.split("/")[-2]
        self.soup_category = BeautifulSoup(get(self.category_url).content, 'html.parser')
        self.books.extend([i.find("a")["href"] for i in self.soup_category.find_all("article")])
        self.Books.extend([Book(urljoin(self.category_url,
                                        i.find("a")["href"])) for i in self.soup_category.find_all("article")])

        if self.soup_category.find("li", class_="next"):
            self.next_url = urljoin(self.category_url,
                                    self.soup_category.find("li", class_="next").find_next("a")["href"])
            Category(self.next_url, self.books, self.Books)
        else:
            pass
        FileCsv(self.Books, self.category_dir)
