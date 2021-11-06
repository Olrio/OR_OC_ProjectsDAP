from requests import get


class ResponseError:
    def __init__(self, url):
        self.url = url
        self.status = None

    def test_url(self):
        self.status = get(self.url).status_code
        print(self.status)
        if self.status != 200:
            print("There seems to be a connection problem with the page you chose")
            print("Please verify your internet connection")
