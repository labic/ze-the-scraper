# -*- coding: utf-8 -*-
import json
import urllib.parse
import scrapy
from scrapy.http import Request, HtmlResponse
import ze

import GoogleScraper

class ZeSpider(scrapy.Spider):
    
    allowed_domains = []
    parses = {}
    
    def __init__(self, name=None, **kwargs):
        self.args = kwargs
        
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        for key, value in kwargs.items():
            try: kwargs[key] = json.loads(value)
            except Exception: pass # TODO: Add debug
                
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        return spider

    def start_requests(self):
        urls = []
        
        if self.args.get('url'):
            urls.append(self.args.get('url'))
        elif self.args['search']['engine'] in ['google']:
            for d in self.allowed_domains:
                self.args['search']['query'] = '%s site:%s' % (self.args['search']['query'], d)
                urls = self.get_urls_from_search_engine(self.args['search'])
        elif self.args['search']['engine'] == 'own':
            self.make_request_from_onw_search_engine()
        else:
            raise ValueError('search.provider is not valid, please search `google` or `own`')
        
        for u in urls:
            yield scrapy.Request(u)
    
    def get_urls_from_search_engine(self, args={}):
        """
        args['config']['last_update']
            Applications: tbm=app
            Blogs: tbm=blg
            Books: tbm=bks
            Discussions: tbm=dsc
            Images: tbm=isch
            News: tbm=nws
            Patents: tbm=pts
            Places: tbm=plcs
            Recipes: tbm=rcp
            Shopping: tbm=shop
            Video: tbm=vid
        """ 
    
        def fix_urls(url):
            url = url.replace('/amp/', '') if '/amp/' in url else url
            url = urllib.parse.urljoin('http://', url) if 'http://' not in url else url
            return url
        
        # TODO: implement quantity arg
        if args.get('engine', 'google') == 'google':
            config = {
                'use_own_ip': 'True',
                'keywords': [args['query']],
                'google_search_url': 'https://www.google.com/search?tbs=qdr:%s&' % args.get('last_update', 'w'),
                'num_results_per_page': args.get('results_per_page', 50),
                'num_pages_for_keyword': args.get('pages', 2),
                'num_workers': 1,
                'search_engines': ['google',],
                'search_type': 'normal',
                'scrape_method': 'http',
                'do_caching': False,
                'print_results': None,
            }
        else:
            raise NotImplementedError('Only Google serch engine is supported at momment')
        
        self.logger.info('Google Search scrapping start with this configuration: %s' % config)
        
        try:
            search = GoogleScraper.scrape_with_config(config)
        except GoogleScraper.GoogleSearchError as e:
            self.logger.error(str(e))
        
        urls = []
        for serp in search.serps:
            [urls.append(fix_urls(r.link)) for r in serp.links]
        
        self.logger.info('Google Search scrapped with success: %d links extracted' % len(urls))
        self.logger.info('List of link extracted from Google Search: %s' % urls)
        
        return urls

    def make_request_from_onw_search_engine(self, args={}):
        raise NotImplementedError

    def parse(self, response):
        for p in self.parses:
            for i, a in p.items():
                ItemClass = ze.utils.import_class(i)
                parse_method = getattr(self, a['parse_method'])
                yield parse_method(response, ItemClass, a)

    def parse_news_article_item(self, response, ItemClass=None, args=None):
        il = ze.items.ItemLoader(item=ItemClass(), response=response)
        
        for field, selectors in args['fields'].items():
            for i, s in enumerate(selectors):
                il.add_css(field, s) if i == 0 else il.add_fallback_css(field, s)
        
        il.add_value('url', response.url)

        return il.load_item()