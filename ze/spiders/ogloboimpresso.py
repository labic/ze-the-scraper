# -*- coding: utf-8 -*-
import re
import json
import datetime
import dateparser
import unidecode
from urllib.parse import urlencode

from scrapy import Spider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from bs4 import BeautifulSoup, Comment

from ze.spiders import ZeSpider
from ..items.creativework import NewsArticleItem


class OGloboImpressoSpider(ZeSpider):
    
    name = 'ogloboimpresso'
    search_url = 'http://oglobodigital.oglobo.globo.com/epaper/services/AdvancedSearch_v2.ashx'
    pre_download_url= 'http://oglobodigital.oglobo.globo.com/epaper/services/OnlinePrintHandler.ashx'
    search_params = {
        'srchIn':'ALL',
        'srchOrderBy':'Relevance',
        'srchPage':'0',
    }
    pre_download_params = {    
        # 'issue':'e610'+anoStr+mesStr+diaStr+'00000000001001',
        # 'page':'1',
        'paper':'A4'
    }
    
    def start_requests(self):
        if hasattr(self, 'keywords'):
            self.search_params['srchText'] = getattr(self, 'keywords')
            today = {
                'year': str(datetime.datetime.now().year),
                'month': str(datetime.datetime.now().month).zfill(2),
                'day': str(datetime.datetime.now().day).zfill(2)
            }
            self.search_params['srchStartDate'] = today['year']+'-'+today['month']+'-'+today['day']
            self.search_params['srchStopDate'] = today['year']+'-'+today['month']+'-'+today['day']
            self.pre_download_params['issue'] = 'e610'+today['year']+today['month']+today['day']+'00000000001001'
            
            yield FormRequest(self.search_url, formdata=self.search_params,
                              callback=self.get_search_result,)

    def get_search_result(self,resp):
        search_result_soup = BeautifulSoup(resp.text, 'lxml')
        result_pages = []
        
        for result in search_result_soup.select('article'):
            page_number = result.select('pagenumber')[0].get_text()
            
            if page_number not in result_pages:
                result_pages.append(page_number)
        
        for page in result_pages:
            self.pre_download_params['page']=page
            
            return Request(self.pre_download_url+'?'+urlencode(self.pre_download_params), 
                           callback=self.get_export_url)

    def get_export_url(self, resp):
        export_url = BeautifulSoup(resp.text, 'html.parser').select('img')[0]['src']
        newArticleItem = NewsArticleItem()
        newArticleItem['url'] = export_url
        
        yield newArticleItem
