# -*- coding: utf-8 -*-
import math
from datetime import datetime
from pprint import pprint
import urllib
import requests
from weakref import WeakKeyDictionary
import logging; logger = logging.getLogger(__name__)
from scrapy import signals
from scrapy.utils.project import data_path
import GoogleScraper


class GoogleSearchMiddleware(object):
    
    api_rest_base_url = 'https://www.googleapis.com/customsearch/v1?'
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.stats = crawler.stats
        self.lib = crawler.settings.get('GOOGLE_SEARCH_MIDDLEWARE_LIB', 'google_rest')
        self.api_key = crawler.settings.get('GOOGLE_SEARCH_MIDDLEWARE_API_KEY')
        self.custom_search_engine_key = crawler.settings.get('GOOGLE_SEARCH_MIDDLEWARE_CUSTOM_SEARCH_ENGINE_ID')
        self.cache_enabled = crawler.settings.getbool('GOOGLE_SEARCH_MIDDLEWARE_CACHE_ENABLE')
        self._cc_parsed = WeakKeyDictionary()
        
        crawler.signals.connect(self.spider_opened, signal=signals.spider_opened)

    def spider_opened(self, spider):
        # FIXME legacie code
        # elif hasattr(self, 'search'):
        #     if self.search['engine'] == 'google':
        #         for d in self.allowed_domains:
        #             search = copy(self.search)
        #             search['query'] = '%s site:%s' % (search['query'], d)
        #             self.start_urls = self.start_urls + SearchEngine.search_for_urls(search)
        if hasattr(spider, 'search'):
            query_paraments = {
                'key': self.api_key,
                'cx': self.custom_search_engine_key,
                'fields': 'items(cacheId,link,snippet,title),queries',
                'start': 1,
                'q': spider.query,
                'dateRestrict': getattr(spider, 'dateRestrict', 'd1'),
            }
            
            if self.cache_enabled:
                self.retrive_search_results(spider, query_paraments)
            
            search_items = self.search_via_api_rest(query_paraments)
            spider.start_urls = search_items
        else:
            logger.info('Spider %s don\'t has search argument'%spider.name)
    
    def search_via_api_rest(self, query_paraments, search_items=[]):
        query_paraments_encoded = urllib.parse.urlencode(query_paraments)
        google_custom_search_url = ''.join((self.api_rest_base_url, query_paraments_encoded))
        
        search_results = requests.get(google_custom_search_url).json()
        # logger.debug('search.search_search:\n%s'%pprint(search_results))
        self.stats.inc_value('google/custom_search/requests')
        
        if 'items' in search_results:
            search_items += search_results['items']
        search_request = search_results['queries']['request'][0]
        
        search_total_results = int(search_request['totalResults'])
        self.stats.set_value('google/custom_search/total_results', search_total_results)
        search_total_pages = math.ceil(search_total_results/ 10)
        search_start_index = int(search_request['startIndex'])
        
        if search_total_pages < search_start_index:
            query_paraments['start'] += 1
            self.search_via_api_rest(query_paraments, search_items)
        
        return [i['link'] for i in search_items]
    
    def search_via_googler(self, query_paraments):
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
        raise NotImplementedError
        
        def fix_urls(url):
            url = url.replace('/amp/', '') if '/amp/' in url else url
            url = url.replace('/amp.html', '') if '/amp.html' in url else url
            url = urllib.parse.urljoin('http://', url) if 'http://' not in url else url
            return url
        
        google_search_url = 'https://www.google.com/search?tbs=qdr:%s&'
        dateRestrict = query_paraments.get('dateRestrict', 'd')
        config = {
            'use_own_ip': 'True',
            'keywords': [query_paraments['query']],
            'google_search_url': google_search_url % dateRestrict,
            'num_results_per_page': query_paraments.get('results_per_page', 50),
            'num_pages_for_keyword': query_paraments.get('pages', 2),
            'num_workers': 2,
            'search_engines': ['google',],
            'search_type': 'normal',
            'scrape_method': 'http',
            'do_caching': False,
            'print_results': None,
        }
        
        logger.debug('Google Search scrapping start with this configuration: {}'
                    .format(config))
        
        try:
            google_search = GoogleScraper.scrape_with_config(config)
            
            urls_without_fix = []
            urls = []
            for serp in google_search.serps:
                urls_without_fix= [r.link for r in serp.links]
                urls = [fix_urls(r.link) for r in serp.links]
            
            logger.debug('Google Search fixed links successfully extracted with query "{}": {:d} links extracted'.format(
                query_paraments['query'], len(urls)))
            logger.debug('Google Search links without fix successfully extracted with query "{}":\n{}'.format(
                query_paraments['query'], urls_without_fix))
            logger.debug('List of link extracted from Google Search with the query "{}":\n{}'.format(
                query_paraments['query'], urls))
            
            return urls
        except GoogleScraper.GoogleSearchError as e:
            logger.error(str(e))
