from pip.req import parse_requirements
from setuptools import setup, find_packages

setup(
    name = 'ze-the-scraper',
    version = '0.0.19.dev1',
    url = 'http://github.com/labic/ze-the-scraper',
    description = 'Scaper to lager portal of news in Brazil.',
    keywords = ['scrapy scraper spider crawler brazil news estadao veja folha-de-sp'],
    author = '@gustavorps, @ligiaiv',
    author_email = 'email+labic.net@gustavorps.net, ligiaiv@gmail.com',
    license = 'MIT',
    packages = find_packages(),
    entry_points = {'scrapy': ['settings = ze.settings']},
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
    
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
    
        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: Academic Free License (AFL)',
    
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
    ],
)
