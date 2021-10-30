from urllib.parse import urljoin
from bs4 import BeautifulSoup
from requests import get
from data.category import Category


class Site:
    def __init__(self, url):
        self.site_url = url
        self.soup_site = BeautifulSoup(get(self.site_url).content, 'html.parser')
        for i in self.soup_site.find("ul", class_="nav").find_next("ul").find_all("a"):
            Category(urljoin(self.site_url, i["href"]))
