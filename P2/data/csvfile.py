import csv


class FileCsv:
    def __init__(self, class_books, category):
        self.Books = class_books
        self.category = category
        self.create_csv()

    def create_csv(self):
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
