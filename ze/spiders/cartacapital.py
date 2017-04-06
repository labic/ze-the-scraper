# -*- coding: utf-8 -*-

import math
try:
    import urlparse
    from urllib import urlencode
except: # Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from ze.items.article import ArticleItem, ArticleItemLoader

class CartaCapitalSpider(scrapy.Spider):

    name = 'cartacapital'
    allowed_domains = ['cartacapital.com.br']
    config = {
        'defaultSearchlUrl': '',
        'ajaxSearchUrl': 'cartacapital.com.br',
        'args': None
    }


    def __init__(self, url=None, query=None, editorial=None, subject=None, when=None, contentType=None, *args, **kwargs):
        super(CartaCapitalSpider, self).__init__(*args, **kwargs)
        
        self.config['args'] = {
            'source': 'url', 
            'url': url, 
            'query': query, 
            'editorial': editorial, 
            'subject': subject, 
            'when': when, 
            'contentType': contentType, 
        }
        
        if url:
            self.start_urls = [self.config['args']['url']]
        else:
            self.config['args']['source'] = 'defaultSearchlUrl'
            self.start_urls = self.generateUrls(self.config['args'])


    def parse(self, response):
        if self.config['args']['source'] == 'url':
            yield scrapy.Request(self.config['args']['url'], callback=self.load_article_item)
        
        if self.config['args']['source'] == 'defaultSearchlUrl':
            raise NotImplemented
            results = [int(s) for s in response.css('.flt-registros::text').extract()[0].split() if s.isdigit()][0]
            self.logger.info('Total of Results: %d', results)
            pages = int(math.ceil(results / 10))
            self.logger.info('Total of Pages: %d', pages)
            
            self.config['args']['source'] = 'ajaxSearchUrl'
            
            for p in range(1, pages+1):
                self.config['args']['page'] = p
                yield scrapy.Request(self.generateUrls(self.config['args']), callback=self.load_article_item_urls)


    def load_article_item_urls(self, response):
        raise NotImplemented
        for i, url in enumerate(response.css('.link-title::attr(href)').extract()):
            yield scrapy.Request(url, meta={'index': i}, callback=self.load_article_item)


    def load_article_item(self, response):
        l = ArticleItemLoader(item=ArticleItem(), response=response)

        l.add_css('name', '[itemprop=headline]::text')
        l.add_fallback_css('name', '.documentFirstHeading::text')
        l.add_css('authors', '[itemprop=author]::text')
        l.add_css('authors', '.documentAuthor a::text')
        l.add_css('description', '[itemprop=description]::text')
        l.add_fallback_css('description', '.documentDescription::text')
        l.add_css('date_published', '[itemprop=datePublished]::text')
        l.add_fallback_css('date_published', '.documentPublished::text')
        # l.add_css('date_modified', '[itemprop=dateModified]::text')
        l.add_css('keywords', '[property="rnews:keywords"] a::text')
        l.add_fallback_css('keywords', '#category .link-category a::text')
        l.add_css('text', '[itemprop=articleBody]')
        l.add_fallback_css('text', '#content-core')
        # TODO: Add publisher
        l.add_value('url', response.url)
        
        if 'blog' in response.url:
            l.add_value('sources_types', ('portal', 'blog'))
        else:
            l.add_value('sources_types', ('portal'))

        yield l.load_item()


    def generateUrls(self, values):
        raise NotImplemented
