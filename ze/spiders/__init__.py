# -*- coding: utf-8 -*-
from copy import copy
import json
import scrapy
from scrapy.spiderloader import SpiderLoader
from scrapy.http import Request, HtmlResponse
import ze
from ze.utils.searchengine import SearchEngine


class ZeSpider(scrapy.Spider):
    
    allowed_domains = []
    parses = []
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        for key, value in kwargs.items():
            try: kwargs[key] = json.loads(value)
            # FIXME find a better way to convert JSON input
            except ValueError: pass
        
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        return spider
    
    def start_requests(self):
        if hasattr(self, 'url'):
            self.start_urls.append(self.url)
        elif hasattr(self, 'search'):
            if self.search['engine'] == 'google':
                for d in self.allowed_domains:
                    search = copy(self.search)
                    search['query'] = '%s site:%s' % (search['query'], d)
                    self.start_urls = self.start_urls + SearchEngine.search_for_urls(search)
            elif self.search['engine'] == 'own':
                self.make_request_from_onw_search_engine()
            else:
                raise ValueError('search.engine is not valid, use `google` or `own`')
        else:
            raise ValueError('Must provide "url" or "search" argument')
    
        for url in self.start_urls:
            yield self.make_requests_from_url(url)
    
    def parse(self, response):
        for p in self.parses:
            for i, a in p.items():
                ItemClass = ze.utils.import_class(i)
                load_method = self[a.get('load_method')] if a.get('load_method') else self.load_item
                yield load_method(response, ItemClass, a)

    def load_item(self, response, ItemClass=None, args=None):
        il = ze.items.ItemLoader(
            item=ItemClass(), 
            response=response, 
            spider_name=self.name)
        
        for field, selectors in args['fields'].items():
            for i, s in enumerate(selectors):
                il.add_css(field, s) if i == 0 else il.add_fallback_css(field, s)
        
        il.add_value('url', response.url)

        return il.load_item()

    def make_request_from_onw_search_engine(self, args={}):
        raise NotImplementedError


class AllSpiders(ZeSpider):

    name = 'all'
    allowed_domains = []
    domains_parses = {}
    
    def start_requests(self):
        spider_loader = SpiderLoader.from_settings(self.settings)
        
        spider_names = spider_loader.list()
        spider_names.remove(self.name)
        
        for spider_name in spider_names:
            Spider = spider_loader.load(spider_name)
            
            for domain in Spider.allowed_domains:
                self.domains_parses[domain] = Spider.parses
            
            self.allowed_domains = self.allowed_domains + Spider.allowed_domains
        
        if hasattr(self, 'url'):
            self.start_urls.append(self.url)
        elif hasattr(self, 'search'):
            if self.search['engine'] == 'google':
                for d in self.allowed_domains:
                    search = copy(self.search)
                    search['query'] = '%s site:%s' % (search['query'], d)
                    self.start_urls = self.start_urls + SearchEngine.search_for_urls(search)
            elif self.search['engine'] == 'own':
                self.make_request_from_onw_search_engine()
            else:
                raise ValueError('search.provider is not valid, please search `google` or `own`')
        else:
            raise ValueError('Must provide "url" or "search" argument')
        
        for url in self.start_urls:
            yield self.make_requests_from_url(url)
    
    def parse(self, response):
        domain_parse = None
        for domain, parses in self.domains_parses.items():
            if domain in response.url:
                domain_parse = domain
                break
        
        for domain_parse in self.domains_parses[domain]:
            for i, a in domain_parse.items():
                ItemClass = ze.utils.import_class(i)
                load_method = self[a.get('load_method')] if a.get('load_method') else self.load_item
                yield load_method(response, ItemClass, a)
