class InputUrl:
    """Interaction with the user who enter the url of the web page to scrap"""

    def __init__(self):
        """Generation of interaction Object"""

    def display_choice(self):
        """Ask the user to choice what to scrap"""
        self.input_url = input("Enter the url of the page(s) you want to scrap : a category page,"
                      "a book page or the home site : ")
        self.verify_url()
        return self.input_url

    def verify_url(self):
        """Verify that the entered url corresponds to an url on books.to.scrape.com"""
        if "https://books.toscrape.com" not in self.input_url:
            print("Please choose a web page on books.toscrape.com")
            self.display_choice()
        else:
            pass