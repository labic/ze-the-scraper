# -*- coding: utf-8 -*-
import copy
import subprocess
import json
import six
import os

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
    
    def get_urls_from_search_engine(self, search_engine='google', args={}):
        config = {}
        
        # TODO: implement quantity arg
        if search_engine == 'google':
            config = {
                'use_own_ip': 'True',
                'keywords': [args['query']],
                'google_search_url': 'https://www.google.com/search?qdr:%s&' % args.get('time_range', 'w'),
                'num_results_per_page': 10,
                'num_pages_for_keyword': 1,
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
            [urls.append(r.link) for r in serp.links]
        
        self.logger.info('Google Search scrapped with success: %d links extracted' % len(urls))
        self.logger.info('List of link extracted from Google Search: %s' % urls)
        return urls