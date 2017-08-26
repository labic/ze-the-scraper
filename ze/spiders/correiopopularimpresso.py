# -*- coding: utf-8 -*-

from urllib.parse import urlparse

from scrapy import Spider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

from ..items.creativework import NewsArticleItem

class CorreioPopularImpressoSpider(Spider):
    
    name = 'correiopopularimpreso'
    start_urls = ['http://correiopopular.html5v3.fivepress.com.br/index.php?id=/login.php']
    
    def start_requests(self):
        for u in self.start_urls:
            yield Request(u, callback=self.auth,
                          meta={'dont_cache': True},)
    
    def auth(self, resp):
        auth = self.settings.get('SPIDERS_AUTH').get('correiopopularimpreso')
        return FormRequest.from_response(resp, callback=self.after_auth,
                                         formdata={'email': auth['email'], 
                                                   'senha': auth['senha']},
                                         meta={'dont_cache': True},)

    def after_auth(self, resp):
        return Request('http://correiopopular.html5v3.fivepress.com.br/',
                       callback=self.get_edition,
                       meta={'dont_cache': True},)

    def get_edition(self, resp):
        url = urlparse(resp.url)
        try:
            edition_url = resp.selector.css('.Baixar::attr(href)').extract()[0]
            edition_url = ''.join((url.scheme, '://', url.netloc, edition_url))
            return Request(edition_url, callback=self.download_pdf)
        except Exception as e:
             self.logger.error('Editon URL not found')
    
    def download_pdf(self, resp):
        pdf_url = resp.selector.css('[download]::attr(href)').extract()[0]
        
        newArticleItem = NewsArticleItem()
        newArticleItem['url'] = pdf_url
        
        return newArticleItem