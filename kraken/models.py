import datetime
import logging
import os
from itertools import chain
from urllib.parse import urlparse, urljoin

import kraken.utils as utils


class Scraper:
    """
    This class represents the scraper that will contains informations and parameters to perform the website copy.
    """
    def __init__(self, website, simultaneous_connexion=4, ignored_files=None, requests_per_s=0, download_file=True, download_external=False):
        self.website = website
        self.simultaneous_connexion = simultaneous_connexion
        self.ignored_files = ignored_files
        self.requests_per_s = requests_per_s  # 0 means no limit
        self.download_file = download_file
        self.download_external = download_external
        self.save_directory = self._create_save_directory()

    def start(self):
        logging.debug(f'Starting scraping for url {self.website.url}')
        self.treat_url(self.website.url)
        while self.website.to_visit:
            self.treat_url_to_visit()

    def _create_save_directory(self):
        """
        Create a directory to store the website copied in the current directory.
        :return: the name of the directory created.
        """
        now_str = datetime.datetime.strftime(datetime.datetime.now(), '%d_%m_%y_%H_%M')
        # replace beginning and slashes to allow creating good folder names
        address = utils.get_domain_name(self.website.url)
        dir_name = f'{address}_{now_str}'

        if os.path.exists(dir_name):
            logging.debug(f'Directory {dir_name} already exists ')
            # TODO: remove not empty directory
            os.rmdir(dir_name)
        os.mkdir(dir_name)
        return dir_name

    def has_already_scraped(self, link):
        """
        Tells if a link has already been scraped before.
        :return: True or False
        """
        return link in chain(self.website.pages_visited, self.website.to_visit)

    def treat_url_to_visit(self):
        url = self.pick_url_to_visit()
        self.treat_url(url)

    def pick_url_to_visit(self):
        # TODO : Make a proper implementation to select efficiently next url
        return self.website.to_visit[-1]

    def treat_url(self, url):
        logging.debug(f'Treating url : {url}')
        url = self.get_absolute_link(url)
        page = utils.get_page(url)

        # links that have not been treated nor are already in the to visit list
        new_links = [self.get_absolute_link(link)for link in utils.find_links(page.content) if not self.has_already_scraped(self.get_absolute_link(link))]
        if not self.download_external:
            new_links = [self.get_absolute_link(link) for link in new_links if not utils.is_external_link(url, link)]
        self.website.to_visit.extend(new_links)

        self._save_page(page)
        if url in self.website.to_visit:
            self.website.to_visit.remove(url)
        self.website.pages_visited.append(url)

    def _save_page(self, page):
        logging.debug(f'_save_page for url : {page.url}')
        self.create_multi_folders_using_url(page.url)

        folders = utils.get_folders_structure(page.url)
        print(f'folders :{folders}')
        name = page.url.rsplit('/', 1)[-1]
        filename = name + '.html' if name and "." not in name else name or 'index.html'
        filepath = os.path.join(self.save_directory, folders, filename)

        if filename.split('.')[-1] in ['png', 'jpg', 'jpeg', 'avi', 'pdf']:
            with open(f'{filepath}', 'wb') as file:
                file.write(page.content)
        else:
            with open(f'{filepath}', 'w') as file:
                page_content = utils.replace_aboslute_link_with_relative(page.text)
                file.write(page_content)

    def create_multi_folders_using_url(self, url):
        """ Method used to create directories to store the webpage."""
        folders = utils.get_folders_structure(url)
        folder_path = os.path.join(self.save_directory, folders)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def get_absolute_link(self, link):
        if link.startswith('/'):
            link = urljoin(self.website.url, link)
        return link


class Website:
    """
    Represents a website.
    """
    def __init__(self, url, login_url=None, login=None, password=None):
        self.url = self._get_base_url(url)
        self.login_url = login_url
        self.login = login
        self.password = password
        self.pages_visited = []
        self.to_visit = []

    @staticmethod
    def _get_base_url(url):
        """ Return the base url of a given address.
        >>> Website._get_base_url('https://github.com/sorasful/kraken')
        'https://github.com'
        >>> Website._get_base_url('http://localhost:8000/admin')
        'http://localhost:8000'
        >>> Website._get_base_url('mysite.fr')
        'https//mysite.fr'
        """
        scheme, address, *_ = urlparse(url)
        return f'{scheme}://{address}'


if __name__ == "__main__":
    import doctest
    doctest.testmod()
