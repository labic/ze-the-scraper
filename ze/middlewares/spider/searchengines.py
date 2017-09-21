# -*- coding: utf-8 -*-
import math
from time import sleep
from datetime import datetime
from collections import Counter
import urllib
import requests
from pprint import pprint
import logging; logger = logging.getLogger(__name__)

from scrapy.exceptions import NotConfigured
from scrapy import signals
from scrapy.utils.project import data_path

import GoogleScraper


class GoogleSearchMiddleware(object):

    api_rest_base_url = 'https://www.googleapis.com/customsearch/v1?'
    gcse_stats_base = 'google/custom_search/%s'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.stats = crawler.stats
        self.sources = crawler.settings.getlist('SEARCH_MIDDLEWARE_SOURCES', ['googler'])
        
        if not self.sources:
            raise NotConfigured('Search Engine is not enabled, check settings values')
        if 'gcse_api' in self.sources:
            self.gcse_api_key = crawler.settings.get('SEARCH_MIDDLEWARE_GCSE_API_KEY')
            self.gcse_cx = crawler.settings.get('SEARCH_MIDDLEWARE_GCSE_CX')
            self.max_index = crawler.settings.get('SEARCH_MIDDLEWARE_GCSE_MAX_INDEX', 10)
        crawler.signals.connect(self.spider_opened, signal=signals.spider_opened)

    def spider_opened(self, spider):
        if not hasattr(spider, 'search'):
            raise NotConfigured('Spider %s don\'t has search argument'%spider.name)
        if not hasattr(spider, 'query'):
            raise NotConfigured('Spider %s don\'t has query argument'%spider.name)
        
        search_items_ruls = []
        
        if 'gcse_api' in self.sources:
            query_paraments = {
                'key': self.gcse_api_key,
                'cx': self.gcse_cx,
                'fields': 'items(cacheId,link,snippet,title),queries(request)',
                'start': 1,
                'filter': 0,
                'q': spider.query,
                'sort': 'date',
                'dateRestrict': getattr(spider, 'dateRestrict', 'd1'),
            }
            search_items_ruls += self.search_via_gcse_api(query_paraments)
        if 'googler' in self.sources:
            query_paraments = {
                'q': spider.query,
                'sort': 'date',
                'dateRestrict': None,
                'results_per_page': 25,
                'num_pages': 4,
            }
            search_items_ruls += self.search_via_googler(query_paraments)
        
        logger.debug('search_items_urls: \n%s'%search_items_ruls)
        spider.start_urls = search_items_ruls
    
    def search_via_gcse_api(self, query_paraments):
        def get_urls(query_paraments, search_items=[], search_items_urls=[]):
            self.stats.inc_value(self.gcse_stats_base%'requests')
            
            query_paraments_encoded = urllib.parse.urlencode(query_paraments)
            google_custom_search_url = ''.join((self.api_rest_base_url, query_paraments_encoded))
            
            search_results = requests.get(google_custom_search_url).json()
            
            search_error = search_results.get('error')
            if search_error:
                logger.error(search_error)
                return []
            
            if 'items' in search_results:
                current_search_itens = search_results['items']
                search_items += search_results['items']
                search_items_urls += [i['link'] for i in current_search_itens]
            
            search_request = search_results['queries']['request'][0]
            search_total_results = int(search_request['totalResults'])
            search_total_pages = math.ceil(search_total_results/10)
            search_start_index = int(search_request['startIndex'])
            search_unique_urls = list(set(search_items_urls))
            
            if search_total_pages > search_start_index \
            and search_start_index < self.max_index:
                query_paraments['start'] += 1
                get_urls(query_paraments, search_items, search_items_urls)
            
                self.stats.set_value(self.gcse_stats_base%'results', search_total_results)
                self.stats.set_value(self.gcse_stats_base%'urls', len(search_items_urls))
                self.stats.set_value(self.gcse_stats_base%'unique_urls', len(search_unique_urls))
            
            unique_search_items = list({v['cacheId']:v for v in search_items}.values())
            return unique_search_items, search_unique_urls
        
        logger.debug('Making search with Google Custom Search API with configuration: {}'
                    .format(query_paraments))
        unique_search_items, unique_urls = get_urls(query_paraments)
        return unique_urls
    
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
        
        def fix_urls(url):
            url = url.replace('/amp/', '') if '/amp/' in url else url
            url = url.replace('/amp.html', '') if '/amp.html' in url else url
            url = urllib.parse.urljoin('http://', url) if 'http://' not in url else url
            return url
        
        google_search_url = 'https://www.google.com/search?tbs=qdr:%s&'
        dateRestrict = query_paraments.get('dateRestrict', 'd')
        config = {
            'use_own_ip': 'True',
            'keywords': [query_paraments['q']],
            'google_search_url': google_search_url % dateRestrict,
            'num_results_per_page': query_paraments.get('results_per_page', 25),
            'num_pages_for_keyword': query_paraments.get('num_pages', 4),
            'num_workers': 2,
            'search_engines': ['google',],
            'search_type': 'normal',
            'scrape_method': 'http',
            'do_caching': False,
            'print_results': None,
        }
        
        logger.debug('Making search with Googler lib with configuration: {}'
                     .format(config))
        
        try:
            google_search = GoogleScraper.scrape_with_config(config)
            
            urls_without_fix = []
            urls = []
            for serp in google_search.serps:
                urls_without_fix= [r.link for r in serp.links]
                urls = [fix_urls(r.link) for r in serp.links]
            
            logger.debug(('Google Search fixed links successfully extracted with ' 
                          'query "{}": {:d} links extracted').format(query_paraments['q'], 
                                                                     len(urls)))
            logger.debug(('Google Search links without fix successfully extracted ' 
                          'with query "{}":\n{}').format(query_paraments['q'], 
                                                         urls_without_fix))
            logger.debug(('List of link extracted from Google Search with the ' 
                          'query "{}":\n{}').format(query_paraments['q'], urls))
            
            return urls
        except GoogleScraper.GoogleSearchError as e:
            logger.error(str(e))
