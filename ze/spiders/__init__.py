# -*- coding: utf-8 -*-
from copy import copy
import json
import scrapy
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.spider import spidercls_for_request
from scrapy.http import Request, HtmlResponse
import urllib
import ze

class ZeSpider(scrapy.Spider):
    
    allowed_domains = []
    parses = []
    
    def start_requests(self):
        if hasattr(self, 'url'):
            self.start_urls.append(self.url)
        
        for url in self.start_urls:
            yield Request(url, dont_filter=False)
    
    def parse(self, response):
        for p in self.parses:
            for i, a in p.items():
                ItemClass = ze.utils.import_class(i)
                load_method = self[a.get('load_method')] if a.get('load_method') else self.load_item
                yield load_method(response, ItemClass, a)

    def load_item(self, response, ItemClass, parse):
        spider_name = self.name if not parse.get('spider_name') else parse.get('spider_name')
        il = ze.items.ItemLoader(
            item=ItemClass(), 
            response=response, 
            spider_name=spider_name)
        
        for field, selectors in parse['fields'].items():
            for i, s in enumerate(selectors):
                il.add_css(field, s) if i == 0 else il.add_fallback_css(field, s)
        
        il.add_value('url', response.url)
        return il.load_item()

    def make_request_from_onw_search_engine(self, args={}):
        raise NotImplementedError


# TAKEALOOK https://github.com/scrapy/scrapy/blob/master/scrapy/commands/shell.py
class AllSpiders(ZeSpider):

    name = 'all'
    allowed_domains = []
    domains_parses = {}
    start_urls = []
    spiders_ignored = [name, 'correiopopularimpreso']
    
    def prepare_domains_parses(self):
        spider_loader = SpiderLoader.from_settings(self.settings)
        
        if hasattr(self, 'spiders'):
            spider_names = self.spiders.split(',')
        else:
            spider_names = [s for s in spider_loader.list() \
                            if s not in self.spiders_ignored]
        
        for spider_name in spider_names:
            Spider = spider_loader.load(spider_name)
            
            for domain in Spider.allowed_domains:
                for i, parse in enumerate(Spider.parses):
                    for item_class, properties in parse.items():
                        properties['spider_name'] = spider_name
                        Spider.parses[i][item_class] = properties
                
                self.domains_parses[domain] = Spider.parses
            
            self.allowed_domains += Spider.allowed_domains
        
        self.allowed_domains.sort(key=len,reverse=True)
    
    def start_requests(self):
        self.prepare_domains_parses()
        
        for url in self.start_urls:
            yield Request(url, dont_filter=False)
    
    def parse(self, response):
        try:
            response_url = urllib.parse.urlparse(response.url)
            domains_allowed = list(d for d in self.allowed_domains \
                                  if d in response_url.geturl())
           
            # FIXME what do when get 2 domain? For now let some DropItem handler   
            if (len(domains_allowed) > 1):
                self.logger.error('more than one allowed domain %s to url: %s'%(domains_allowed, response.url))
        except IndexError:
            parse_of_domain = None
        
        if domains_allowed:
            for domain_parse in self.domains_parses[domains_allowed[0]]:
                for item_class, parse in domain_parse.items():
                    ItemClass = ze.utils.import_class(item_class)
                    load_method = self[parse.get('load_method')] if parse.get('load_method') else self.load_item
                    yield load_method(response, ItemClass, parse)
        else:
            self.crawler.stats.inc_value('spider/all/url_without_parse_count')
            self.logger.warning('Don\'t exist a parse on spiders with allowed domain that match this url: %s'%response.url)
