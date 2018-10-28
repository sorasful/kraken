
from urllib.parse import urlparse

class Scraper:
    """
    This class represents the scraper that will contains informations and parameters to perform the website copy.
    """
    def __init__(self, website, simultaneous_connexion=4, ignored_files=None, requests_per_s=0):
        pass


class Website:
    """
    Represents a website.
    """
    def __init__(self, url, login_url=None, login=None, password=None):
        self.url = self._get_base_url(url)
        self.login_url = login_url
        self.login = login
        self.password = password

    @staticmethod
    def _get_base_url(url):
        """ Return the base url of a given address.
        >>> Website._get_base_url('https://github.com/sorasful/kraken')
        'https://github.com'
        >>> Website._get_base_url('http://localhost:8000/admin')
        'http://localhost:8000'
        """
        scheme, address, *_ = urlparse(url)
        return f'{scheme}://{address}'


if __name__ == "__main__":
    import doctest
    doctest.testmod()
