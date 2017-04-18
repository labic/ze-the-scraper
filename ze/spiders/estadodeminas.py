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

class EstadodeMinasSpider(scrapy.Spider):

    name = 'em'
    allowed_domains = ['em.com.br','uai.com.br']
    config = {
        'defaultSearchlUrl': '',
        'ajaxSearchUrl': '',
        'args': None
    }


    def __init__(self, url=None, query=None, editorial=None, subject=None, when=None, contentType=None, *args, **kwargs):
        super(EstadodeMinasSpider, self).__init__(*args, **kwargs)

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
            raise NotImplemented
            self.config['args']['source'] = 'defaultSearchlUrl'
            self.start_urls = [self.generateUrl(self.config['args'])]


    def parse(self, response):
        if self.config['args']['source'] == 'url':
            yield scrapy.Request(self.config['args']['url'], callback=self.parse_article)

        if self.config['args']['source'] == 'defaultSearchlUrl':
            raise NotImplemented
            results = [int(s) for s in response.css('.flt-registros::text').extract()[0].split() if s.isdigit()][0]
            self.logger.info('Total of Results: %d', results)
            pages = int(math.ceil(results / 10))
            self.logger.info('Total of Pages: %d', pages)

            self.config['args']['source'] = 'ajaxSearchUrl'

            for p in range(1, pages+1):
                self.config['args']['page'] = p
                yield scrapy.Request(self.generateUrl(self.config['args']), callback=self.parse_article_urls)


    def parse_article_urls(self, response):
        raise NotImplemented
        for i, url in enumerate(response.css('.link-title::attr(href)').extract()):
            yield scrapy.Request(url, meta={'index': i}, callback=self.parse_article)


    def parse_article(self, response):
        l = ArticleItemLoader(item=ArticleItem(), response=response)

        l.add_css('name', '[itemprop=headline]::text')
        l.add_fallback_css('name', '.title-post::text')
        l.add_fallback_css('name', '.entry-title::text')
        l.add_css('authors', '[itemprop=author]::text')
        l.add_fallback_css('authors', '.author a::text')
        l.add_fallback_css('authors', '[href*="mailto"]::text')

        l.add_css('date_published', '[itemprop=datePublished]::attr(content)')
        l.add_fallback_css('date_published', '.entry-date::text')
        l.add_css('date_modified', '[itemprop=dateModified]::attr(content)')
        # l.add__fallback_css('date_modified', '[itemprop=dateModified]::text')
        l.add_css('keywords', '[itemprop=keywords] a::text')
        l.add_fallback_css('keywords', '[rel=tag]::text')
        l.add_fallback_css('keywords', '[onclick*=montaURL]::text')
        l.add_css('text', '[itemprop=articleBody]')
        l.add_fallback_css('text', '.entry-content')
        l.add_value('url', response.url)

        if 'blog' in response.url:
            l.add_value('sources_types', ('portal', 'blog'))
            l.add_fallback_css('description', '.entry-content blockquote p::text')

        else:
            l.add_value('sources_types', ('portal'))

            l.add_css('description', '[itemprop=description]::attr(content)')
            l.add_css('description', '[itemprop=description]::text')
            l.add_fallback_css('description', '.linha-fina::text')
            l.add_fallback_css('description', '.entry-content h2::text')

        yield l.load_item()


    def generateUrl(self, values):
        raise NotImplemented
        url_parts = list(urlparse.urlparse(self.config[values['source']]))
        params = {}

        if values['source'] == 'defaultSearchlUrl':
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

        if values['source'] == 'ajaxSearchUrl':
            params = {
                'config[busca][page]': values['page'],
                'config[busca][params]': []
            }

            if values['query']:
                params['config[busca][params]'].append('q=' + values['query'])
            if values['editorial']:
                params['config[busca][params]'].append('&editoria[]=' + values['editorial'])
            if values['subject']:
                params['config[busca][params]'].append('&assunto[]=' + values['subject'])
            if values['when']:
                params['config[busca][params]'].append('&quando=' + values['when'])

            params['config[busca][params]'] = '&'.join(params['config[busca][params]'])

        url_parts[4] = urlencode(params)

        return urlparse.urlunparse(url_parts)
