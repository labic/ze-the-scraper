# -*- coding: utf-8 -*-
import re
import json
import datetime
import dateparser

from urllib.parse import urlencode

from scrapy import Spider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

from . import ZeSpider
from ..items.creativework import NewsArticleItem


class EstadaoImpressoSpider(ZeSpider):

    name = 'estadaoimpresso'
    search_url = 'http://services.pressreader.com/se2skyservices/search/GetArticles/'
    pre_image_url = 'http://services.pressreader.com/se2skyservices/print/GetImageByRegion/'

    print_params = {
        'paper':'Letter',
        'scale':'false',
        'scaleToLandscape':'false',
        'useContentProxy':'true',
    }

    search_params = {
        'OrderBy': 'Relevance',
        'PageSize': '20',
        'Range': 'Today',
        'RowNumber': '0',
        'SearchIn': 'ALL',
        'StartDate': '',
        'StopDate': '',
    }

    def start_requests(self):
        if hasattr(self, 'keywords'):
            query = getattr(self, 'keywords')
            
            self.auth = self.settings.get('SPIDERS_AUTH').get('estadao')
            self.search_params['accessToken'] = self.auth['access_token']
            self.search_params['SearchText'] = query
            
            yield Request(self.search_url+'?'+urlencode(self.search_params), 
                          callback=self.get_search_results)

    def get_search_results(self,resp):
        search_data= json.loads(resp.text).get('Items')
        found_pages=[]
        
        for item in search_data:
            page = item.get('Page')
            
            if page not in found_pages:
                found_pages.append(page)
        
        today = {
            'day': str(datetime.datetime.now().day).zfill(2),
            'month': str(datetime.datetime.now().month).zfill(2),
            'year': str(datetime.datetime.now().year)
        }
        
        self.print_params['accessToken'] = self.auth['access_token']
        self.print_params['issue']='2025'+today['year']+today['month']+today['day']+'00000000001001'

        for page in found_pages:
            self.print_params['page']=page
            return Request(self.pre_image_url+'?'+urlencode(self.print_params), 
                          callback=self.get_img_url)

    def get_img_url(self,resp):
        img_url = json.loads(resp.text).get('Data').get('Src')
        export_urls = []
        export_urls.append(img_url)
        
        for export_url in export_urls:
            newsArticleItem = NewsArticleItem()
            newsArticleItem['url'] = export_url
            
            yield newsArticleItem
