# -*- coding: utf-8 -*-
import math
from time import sleep
from datetime import datetime
from collections import Counter
import urllib
import requests
import logging; logger = logging.getLogger(__name__)
from scrapy.exceptions import NotConfigured
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
        
        if crawler.settings.getbool('GOOGLE_SEARCH_MIDDLEWARE_ENABLED'):
            self.lib = crawler.settings.get('GOOGLE_SEARCH_MIDDLEWARE_LIB', 'google_rest')
            self.api_key = crawler.settings.get('GOOGLE_SEARCH_MIDDLEWARE_API_KEY')
            self.custom_search_engine_key = crawler.settings.get('GOOGLE_SEARCH_MIDDLEWARE_CUSTOM_SEARCH_ENGINE_ID')
            self.max_index = crawler.settings.get('GOOGLE_SEARCH_MIDDLEWARE_MAX_INDEX', 20)
            crawler.signals.connect(self.spider_opened, signal=signals.spider_opened)
        else:
            raise NotConfigured('Search Engine is not enabled, check settings values')

    def spider_opened(self, spider):
        
        if hasattr(spider, 'search'):
            logger.info('Making requests to Google Custom Search')
            
            query_paraments = {
                'key': self.api_key,
                'cx': self.custom_search_engine_key,
                'fields': 'items(cacheId,link,snippet,title),queries',
                'start': 1,
                'q': spider.search,
                'sort': 'date:r:{date}:{date}'.format(date=datetime.now().strftime('%Y%m%d'))
            }
            
            search_items_ruls = self.search_urls_via_api_rest(query_paraments)
            logger.debug('search_items_ruls counter: %s'%search_items_ruls)
            spider.start_urls = search_items_ruls
        else:
            logger.info('Spider %s don\'t has search argument'%spider.name)
    
    def search_urls_via_api_rest(self, query_paraments, search_items=[], search_items_urls=[]):
        self.stats.inc_value('google/custom_search/requests_count')
        
        query_paraments_encoded = urllib.parse.urlencode(query_paraments)
        google_custom_search_url = ''.join((self.api_rest_base_url, query_paraments_encoded))
        
        search_results = requests.get(google_custom_search_url).json()
        
        search_error = search_results.get('error')
        if search_error:
            logger.error(search_error)
            return []
        
        if 'items' in search_results:
            current_search_itens = search_results['items']
            search_items += current_search_itens
            search_items_urls += [i['link'] for i in current_search_itens]
        
        search_request = search_results['queries']['request'][0]
        search_total_results = int(search_request['totalResults'])
        search_total_pages = math.ceil(search_total_results/ 10)
        search_start_index = int(search_request['startIndex'])
        
        # FIXME Bug on Google Custom Search API keep 
        if search_total_pages > search_start_index \
        and search_start_index < self.max_index:
            # sleep(1)
            query_paraments['start'] += 1
            self.search_urls_via_api_rest(query_paraments, search_items, search_items_urls)
        
        self.stats.set_value('google/custom_search/results_count', search_total_results)
        self.stats.set_value('google/custom_search/urls_count', len(search_items_urls))
        
        return search_items_urls
    
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
