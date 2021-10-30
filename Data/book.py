from Data.bs import DataBook
from Data.transfo import TransformDataBook


class Book:
    """Management of methods related to a book"""

    def __init__(self, url):
        """Initiate a book defined by its url"""
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
        self.title = DataBook(self.product_page_url).get_book_title()
        self.upc = DataBook(self.product_page_url).get_book_upc()
        self.price_including_tax = DataBook(self.product_page_url).get_book_price_including_tax()
        self.price_excluding_tax = DataBook(self.product_page_url).get_book_price_excluding_tax()
        self.number_available = DataBook(self.product_page_url).get_number_available()
        self.product_description = DataBook(self.product_page_url).get_product_description()
        self.category = DataBook(self.product_page_url).get_category()
        self.category_dir = DataBook(self.product_page_url).get_category_dir()
        self.review_rating = DataBook(self.product_page_url).get_review_rating()
        self.image_url = DataBook(self.product_page_url).get_image_url()
        self.file_image = TransformDataBook(self.product_page_url).transform_file_image_name(
            self.title, self.image_url, self.category_dir)
        print(self.title)  # enables to follow the execution of the script
