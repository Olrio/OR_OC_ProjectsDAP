from Data.choice import InputUrl
from Errors_management.error import ResponseError
from Data.book import Book
from Data.result import FileCsv
from Data.category import Category
from Data.site import Site


def main():
    """main for poo version"""

    url_scrap = InputUrl().display_choice()
    ResponseError(url_scrap).test_url()

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
