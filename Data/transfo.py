import os
import re
import urllib.request
from urllib.parse import urljoin


class TransformDataBook:
    """Apply transformations to raw data"""

    def __init__(self, url):
        self.url = url
        self.title = None

    @staticmethod
    def transform_review_rating(number):
        """Transform numbers from letters to digits"""
        return {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}[number]

    def transform_file_image_name(self, title, image_url, category):
        self.title = re.sub('[<>/:"|?*,\\\\]', "_", title)
        os.makedirs("./Web_scraper/" + category, exist_ok=True)
        return '"' + os.path.join(
            os.getcwd(), urllib.request.urlretrieve(urljoin(
                self.url, image_url), f'''./Web_scraper/{category}/{self.title}.jpg''')[0]) + '"'
