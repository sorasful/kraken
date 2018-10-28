import requests
from lxml import html


def get_page_content(url):
    response = requests.get(url)
    return response.content


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


def is_external_link(link):
    pass


def download_file(link):
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
