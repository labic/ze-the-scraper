# -*- coding: utf-8 -*-
import json
try:
    import urlparse
    from urllib import urlencode
except: # Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode
import scrapy
from scrapy.http import Request, HtmlResponse
from scrapy.utils.spider import iterate_spider_output

import GoogleScraper

class ZeSpider(scrapy.Spider):
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        for key, value in kwargs.items():
            try:
                kwargs[key] = json.loads(value)
            except Exception:
                # TODO: Add debug
                pass
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        return spider
    
    def get_urls_from_search_engine(self, args={}):
        """
        args['config']['last_update']
            Applications: tbm=app
            Blogs: tbm=blg
            Books: tbm=bks
            Discussions: tbm=dsc
            Discussions: tbm=dsc
            Images: tbm=isch
            News: tbm=nws
            Patents: tbm=pts
            Places: tbm=plcs
            Recipes: tbm=rcp
            Shopping: tbm=shop
            Video: tbm=vid
        """, 
    
        def fix_urls(url):
            url = url.replace('/amp/', '') if '/amp/' in url else url
            url = 'http://'.join(url) if 'http://' not in url else url
            return url
        
        # TODO: know more of about this posibilites. may can use to profiling
        # def __repr__(self):
        #     return '%s' % (__name__, eof)
        
        config = {}
        
        # TODO: implement quantity arg
        if args.get('engine', 'google') == 'google':
            config = {
                'use_own_ip': 'True',
                'keywords': [args['query']],
                'google_search_url': 'https://www.google.com/search?qdr:%s&' % args.get('last_update', 'w'),
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
        
        print(urls)
        return urls