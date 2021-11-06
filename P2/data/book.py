from data.bs import DataBook
from data.transfo import TransformDataBook


class Book:
    """Management of methods related to a book"""

    def __init__(self, url):
        """Initiate a book defined by its url"""
        self.book = None
        self.product_page_url = url
        self.title = None
        self.upc = None
        self.price_including_tax = None
        self.price_excluding_tax = None
        self.number_available = None
        self.product_description = None
        self.category = None
        self.category_dir = None
        self.review_rating = None
        self.image_url = None
        self.file_image = None
        self.get_attributes()

    def get_attributes(self):
        """Define other attributes calling BeautifulSoup"""
        self.book = DataBook(self.product_page_url)
        self.title = self.book.get_book_title()
        self.upc = self.book.get_book_upc()
        self.price_including_tax = self.book.get_book_price_including_tax()
        self.price_excluding_tax = self.book.get_book_price_excluding_tax()
        self.number_available = self.book.get_number_available()
        self.product_description = self.book.get_product_description()
        self.category = self.book.get_category()
        self.category_dir = self.book.get_category_dir()
        self.review_rating = self.book.get_review_rating()
        self.image_url = self.book.get_image_url()
        self.file_image = TransformDataBook(self.product_page_url).transform_file_image_name(
            self.title, self.image_url, self.category_dir)
        print(self.title)  # enables to follow the execution of the script
