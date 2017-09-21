# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import scrapy
from scrapy.spiderloader import SpiderLoader
from scrapy.http import Request

import ze
from ze import utils


class ZeSpider(scrapy.Spider):

    allowed_domains = []

    def start_requests(self):
        if hasattr(self, 'url'):
            self.start_urls.append(self.url)
        
        for url in self.start_urls:
            yield Request(url, dont_filter=False)

    def parse(self, response):
        for item_ref in self.items_refs:
            yield self.load_item(item_ref, response)

    def load_item(self, item_def, response):
        def parse_item_ref(item_def, response, spider_name):
            ItemClass = utils.import_class(item_def.get('item'))
            item_load = ze.items.ItemLoader(item=ItemClass(), 
                                            response=response, 
                                            spider_name=spider_name)
            
            for field_name, properties in item_def['fields'].items():
                if not 'item' in properties:
                    # TODO: This will word with 2 fields with some context?
                    item_load.context.update(properties.get('contexts', {}))
                    for i, selector in enumerate(properties['selectors']['css']):
                        if i == 0: item_load.add_css(field_name, selector) 
                        else: item_load.add_fallback_css(field_name, selector)
                else:
                    field_item_load = parse_item_ref(properties, response, spider_name)
                    item_load.add_value(field_name, field_item_load.load_item())
            
            return item_load
        
        spider_name = self.name if not hasattr(item_def, 'spider') \
                                else item_def['spider']['name']
        item = parse_item_ref(item_def, response, spider_name)
        item.add_value('url', response.url)
        
        return item.load_item()

    def search(self, match):
        raise NotImplementedError


# TAKEALOOK https://github.com/scrapy/scrapy/blob/master/scrapy/commands/shell.py
class AllSpiders(ZeSpider):

    name = 'all'
    allowed_domains = []
    domains_items_refs = {}
    start_urls = []
    spiders_ignored = [name, 'atardeimpresso', 'correiobrazilienseimpresso', 
        'correiopopularimpreso', 'estadaoimpresso', 'estadodeminasimpresso',
        'ogloboimpresso', ]
    
    def _prepare_domains_items_refs(self):
        spider_loader = SpiderLoader.from_settings(self.settings)
        
        if hasattr(self, 'spiders'):
            spider_names = getattr(self, 'spiders').split(',')
        else:
            spider_names = [spider_name for spider_name in spider_loader.list() \
                            if spider_name not in self.spiders_ignored]
        
        for spider_name in spider_names:
            Spider = spider_loader.load(spider_name)
            
            for domain in Spider.allowed_domains:
                for i, item_ref in enumerate(Spider.items_refs):
                    item_ref['spider_name'] = spider_name
                    Spider.items_refs[i] = item_ref
                
                self.domains_items_refs[domain] = Spider.items_refs
            
            self.allowed_domains += Spider.allowed_domains
        
        self.allowed_domains.sort(key=len,reverse=True)
    
    def start_requests(self):
        self._prepare_domains_items_refs()
        
        for url in self.start_urls:
            yield Request(url, dont_filter=False)
    
    def parse(self, response):
        try:
            response_url = urlparse(response.url)
            domains_allowed = list(d for d in self.allowed_domains \
                                      if d in response_url.geturl())
           
            # FIXME what do when get 2 domain? For now let some DropItem handler   
            if (len(domains_allowed) > 1):
                self.logger.error('more than one allowed domain %s to url: %s'
                                  %(domains_allowed, response.url))
        except IndexError as error:
            self.logger.error(error)
        
        if domains_allowed:
            for item_ref in self.domains_items_refs[domains_allowed[0]]:
                yield self.load_item(item_ref, response)
        else:
            self.crawler.stats.inc_value('spider/all/url_without_parse_count')
            self.logger.warning('Don\'t exist a parse on spiders with allowed domain that match this url: %s'%response.url)
