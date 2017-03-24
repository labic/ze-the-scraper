# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
try:
    import urlparse
    from urllib import urlencode
except: # Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode
import re
from newspaper.items.article import ArticleItem, ArticleItemLoader

class EstadaoArticlesSpider(scrapy.Spider):

    name = 'newspaper-estadao-web'
    allowed_domains = ['estadao.com.br']
    config = {
        'url': 'http://busca.estadao.com.br/modulos/busca-resultado',
    }

    def __init__(self, query=None, editorial=None, subject=None, when=None, *args, **kwargs):
        super(EstadaoArticlesSpider, self).__init__(*args, **kwargs)
        url_parts = list(urlparse.urlparse(self.config['url']))
        params = {
            'config[busca][page]': 1,
            'config[busca][params]': []
        }
        
        if query:
            params['config[busca][params]'].append('q=' + query)
        if editorial:
            params['config[busca][params]'].append('&editoria[]=' + editorial)
        if subject:
            params['config[busca][params]'].append('&assunto[]=' + subject)
        if when:
            params['config[busca][params]'].append('&quando=' + when)
        
        params['config[busca][params]'] = '&'.join(params['config[busca][params]'])
        
        url_parts[4] = urlencode(params)
        self.start_urls = [urlparse.urlunparse(url_parts)]

        pass


    def parse(self, response):
        pages = int(response.css('.paginacaoultimas :last-child > a::text').extract()[0])

        if 'busca.' in response.url:
            for d in range(1, pages):
                yield scrapy.Request('http://busca.estadao.com.br/?q='+self.config['query']+'&pagina='+str(d), callback=self.parse_urls)
        if '/ultimas' in response.url:
            for d in range(1, pages):
                yield scrapy.Request('http://'+self.config['topic']+'.estadao.com.br/ultimas/='+str(d), callback=self.parse_urls)

        pass


    def parse_urls(self, response):
        for url in response.css('.listadesc a::attr(href)').extract():
            yield scrapy.Request(url, callback=self.parse_article)
        pass


    def parse_article(self, response):
        l = ArticleItemLoader(item=ArticleItem(), response=response)

        l.add_css('name', '[itemprop=headline]::text')
        l.add_fallback_css('name', 'header h1::text')
        l.add_fallback_css('name', '.box-content .titulo::text')
        l.add_fallback_css('name', '.hd h1::text')
        l.add_fallback_css('name', 'header .titulo::text')
        l.add_fallback_css('name', 'header .titulo b::text')
        l.add_fallback_css('name', '#cap1 header .subtitulo::text')
        l.add_fallback_css('name', '.main .main-title::text')
        l.add_fallback_css('name', '.corpoPost h2 a::text')
        l.add_fallback_css('name', 'header .post-title::text')
        l.add_css('authors', '[itemprop=author]::text')
        l.add_fallback_css('authors', '.credito::text')
        l.add_fallback_css('authors', 'header .credito::text')
        l.add_fallback_css('authors', '.nome::text')
        l.add_fallback_css('authors', '.autores strong::text')
        l.add_fallback_css('authors', '.credits span::text')
        l.add_fallback_css('authors', 'header .author::text')
        l.add_fallback_css('authors', '#nome_editor::text')
        l.add_fallback_css('authors', '.infoPost .credito::text')
        l.add_fallback_css('authors', '.bb-md-blogpost .author::text')
        l.add_css('description', '[itemprop=description]::text')
        l.add_fallback_css('description', 'header .chapeu::text')
        l.add_fallback_css('description', 'header .chapeu p::text')
        l.add_fallback_css('description', 'header .linhafina::text')
        l.add_fallback_css('description', '.main > p::text')
        l.add_fallback_css('description', '.box-content .chamada::text')
        l.add_css('date_published', '[itemprop=datePublished]::text')
        l.add_fallback_css('date_published', '.post-date::text')
        l.add_fallback_css('date_published', '.box-content .tit-secao span::text')
        l.add_fallback_css('date_published', '.hd .data::text')
        l.add_fallback_css('date_published', 'header .data::text')
        l.add_fallback_css('date_published', '.main .time::text')
        l.add_fallback_css('date_published', '.infoPost .data::text')
        l.add_css('date_modified', '[itemprop=dateModified]::text')
        l.add_css('keywords', '[itemprop=keywords] a::text')
        l.add_fallback_css('keywords', '.tags a::text')
        l.add_fallback_css('keywords', '.hd .categorias a::text')
        l.add_fallback_css('keywords', '.infoPost .categoria a::text')
        l.add_fallback_xpath('keywords', '//*[@id="content"]//h3/text()')
        l.add_css('text', '[itemprop=articleBody]')
        l.add_fallback_css('text', '.texto')
        l.add_fallback_css('text', '.blocotexto')
        l.add_fallback_css('text', '.blogContent')
        l.add_fallback_css('text', '.box-content .corpo')

        l.add_value('url', response.url)
        if 'blog' in response.url:
            l.add_value('sources_types', ('portal', 'blog'))
        else:
            l.add_value('sources_types', ('portal'))

        yield l.load_item()
