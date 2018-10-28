import os
import logging
from urllib.parse import urlparse, urljoin

from lxml import html
import requests


def get_domain_name(url):
    """
    Return only the domain name when given a url.
    Handle url with protocol and without.
    >>> get_domain_name('https://google.fr/lol')
    'google.fr'
    >>> get_domain_name('youtube.com/lol')
    'youtube.com'
    >>> get_domain_name('/no-domain-name.html') is None
    True
    """
    if url.startswith('/'):
        return None
    _, netloc, path, *_ = urlparse(url)
    return netloc or path.split('/')[0]


def get_page(url):
    if url.startswith('/'):
        url = 'https:/' + url
    logging.debug(f'Getting page : {url}')
    response = requests.get(url)
    return response


def find_links(page_content):
    """ Return a list of links in the current page content.
    >>> find_links("<html><a href='https://google.fr'>Google</a></html>")
    ['https://google.fr']
    >>> find_links("<html><a href='https://google.fr'>Google</a><a href='/css/minified.css'>css</a></html>")
    ['https://google.fr', '/css/minified.css']
    >>> find_links('<html><p>Not links ! </p></html>')
    []
    >>> find_links('<html><p>Broken html ! </pl>')
    []
    """
    page = html.fromstring(page_content)
    return page.xpath('//a/@href')


def is_external_link(url, link):
    """ Function to determine if the link points to an external resource or not.
    >>> is_external_link('http://mysite.com/', 'http://google.fr/lol')
    True
    >>> is_external_link('http://mysite.com/', 'https://google.fr/lol/hello')
    True
    >>> is_external_link('http://mysite.com/', 'google.fr/lol')
    True
    >>> is_external_link('http://mysite.com/', '/file.css')
    False
    >>> is_external_link('http://mysite.com/', 'http://mysite.com/file.css')
    False
    """
    return (get_domain_name(url) != get_domain_name(link)) and not link.startswith('/')


def get_folders_structure(url):
    """
    Get a url and return a string of folders to create.
    >>> get_folders_structure('http://mysite.com/articles/css/lol.html')
    'articles/css/'
    >>> get_folders_structure('/articles/css/lol.html')
    'articles/css/'
    >>> get_folders_structure('mysite.fr/lol.html')
    ''
    >>> get_folders_structure('https://mysite.fr/')
    ''
    >>> get_folders_structure('https://mysite.fr/articles/etoile-args-kwargs/')
    'articles/etoile-args-kwargs/'
    """
    # split the path by '/' and ignore the last entry which is the filename
    path = urlparse(url)[2]
    if path == '/':
        return ''
    folders = path.rsplit('/', 1)[0] + '/'
    # FIXME : May not work everytime ... if there is a point, chances are that this is the domain and not folder names
    if "." in folders:
        return ''
    return folders[1:]


def download_file(link):
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
