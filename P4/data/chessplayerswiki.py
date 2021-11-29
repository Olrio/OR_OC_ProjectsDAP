# -*- coding: utf8 -*-

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "characters_scraper"
    start_urls = [
        "https://fr.wikipedia.org/wiki/Liste_de_joueurs_d'échecs",
    ]

    def parse(self, response):
        for quote in response.xpath("//tbody/tr/td/h2/following-sibling::ul/li"):
            yield {
                "player": quote.xpath("a/text()").extract_first(),
            }
