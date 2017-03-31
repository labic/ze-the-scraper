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

class EstadaoArticlesSpider(scrapy.Spider):

    name = 'g1'
    allowed_domains = ['g1.globo.com']
    config = {
        'searchlUrl': 'http://g1.globo.com/busca/',
        'cdnUrl': 'http://falkor-cda.bastian.globo.com/feeds/{feedId}/posts/page/{page}'
        'args': None,
        'feeds': {
            'educacao': '42f93818-a7ce-41d9-9a3f-57f43df62f03'
        }
    }


    def __init__(self, url=None, query=None, editorial=None, subject=None, when=None, contentType=None, *args, **kwargs):
        super(EstadaoArticlesSpider, self).__init__(*args, **kwargs)
        
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
            self.start_urls = [self.generateUrl(self.config['args'])]


    def parse(self, response):
        if self.config['args']['source'] == 'url':
            yield scrapy.Request(self.config['args']['url'], callback=self.parse_article)
        
        if self.config['args']['source'] == 'defaultSearchlUrl':
            results = [int(s) for s in response.css('.flt-registros::text').extract()[0].split() if s.isdigit()][0]
            self.logger.info('Total of Results: %d', results)
            pages = int(math.ceil(results / 10))
            self.logger.info('Total of Pages: %d', pages)
            
            self.config['args']['source'] = 'ajaxSearchUrl'
            
            for p in range(1, pages+1):
                self.config['args']['page'] = p
                yield scrapy.Request(self.generateUrl(self.config['args']), callback=self.parse_article_urls)


    def parse_article_urls(self, response):
        for i, url in enumerate(response.css('.link-title::attr(href)').extract()):
            yield scrapy.Request(url, meta={'index': i}, callback=self.parse_article)


    def parse_article(self, response):
        l = ArticleItemLoader(item=ArticleItem(), response=response)

        l.add_css('name', '[itemprop=headline]::text')
        l.add_fallback_css('name', '.content-head__title::text')
        l.add_css('authors', '[itemprop=creator]::text')
        # l.add_css('publisher', '[itemprop=publisher]::attr(content)')
        l.add_css('description', '[itemprop=alternativeHeadline]::text')
        l.add_fallback_css('description', '.content-head__subtitle::text')
        l.add_css('date_published', '[itemprop=datePublished]::attr(datetime)')
        l.add_css('date_modified', '[itemprop=dateModified]::attr(datetime)')
        l.add_css('text', '.mc-body')
        l.add_css('keywords', '.entities__list-itemLink::text')
        l.add_value('url', response.url)
        
        if 'blog' in response.url:
            l.add_value('sources_types', ('portal', 'blog'))
        else:
            l.add_value('sources_types', ('portal'))

        yield l.load_item()


    def generateUrl(self, values):
        url_parts = list(urlparse.urlparse(self.config[values['source']]))
        params = {}
        
        if values['query']:
            params['q'] = (values['query'])
        if values['editorial']:
            params['editoria[]'] = (values['editorial'])
        if values['subject']:
            params['assunto[]'] = (values['subject'])
        if values['when']:
            params['quando'] = (values['when'])
        if values['contentType']:
            params['tipo_conteudo'] = (values['contentType'])
        
        url_parts[4] = urlencode(params)
        
        return urlparse.urlunparse(url_parts)
