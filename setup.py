from pip.req import parse_requirements
from setuptools import setup, find_packages

setup(
    name = 'zethescraper',
    version = '1.0',
    description = 'Scaper to lager portal of news in Brazil.',
    url = 'http://github.com/labic/ze-the-scraper',
    author = 'GustavoRPS',
    author_email = 'email+labic.net@gustavorps.net',
    license = 'MIT',
    packages = find_packages(),
    install_requires = [str(ir.req) for ir in parse_requirements('./requirements.txt')],
    entry_points = {'scrapy': ['settings = newspaper.settings']},
)
