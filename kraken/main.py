import logging
import sys

from kraken.models import Scraper, Website

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    website = Website('https://lafleche.io')
    scraper = Scraper(website)
    scraper.start()
    sys.exit(0)