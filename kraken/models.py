import datetime
import os
from urllib.parse import urlparse

import kraken.utils as utils


class Scraper:
    """
    This class represents the scraper that will contains informations and parameters to perform the website copy.
    """
    def __init__(self, website, simultaneous_connexion=4, ignored_files=None, requests_per_s=0, download_file=True):
        self.website = website
        self.simultaneous_connexion = simultaneous_connexion
        self.ignored_files = ignored_files
        self.requests_per_s = requests_per_s  # 0 means no limit
        self.download_file = download_file
        self.save_directory = self.create_save_directory()

    def start(self):
        # while to_visit
        # pick one in to_visit, go to the page, save content, find link, add those who weren't treated yet
        pass

    def create_save_directory(self):
        """
        Create a directory to store the website copied.
        :return: the name of the directory created.
        """
        now_str = datetime.datetime.strftime(datetime.datetime.now(), '%d_%m_%y_%H_%M')
        # replace beginning and slashes to allow creating good folder names
        address = utils.get_domain_name(self.website.url)
        name = f'{address}_{now_str}'

        os.mkdir(name)
        return name

    def has_already_visited(self, link):
        """
        Tells if a link has already been scraped before.
        :return: True or False
        """
        return link in self.website.page_visited

    def pick_url_to_visit(self):
        # TODO : Make a proper implementation to select efficiently next url
        return self.website.to_visit[-1]

    def treat_link(self, link):
        # if it's a file, download it if download_file is True
        # if it's a web page, go to it, find links, add the one not treated yet, save the content and delete the link from the list

        pass

    def save_page(self, page_content):
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
        self.page_visited = []
        self.to_visit = []

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
