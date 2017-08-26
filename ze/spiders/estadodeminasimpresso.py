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


class EstadodeMinasImpressoSpider(ZeSpider):

    name = 'estadodeminasimpresso'
    search_url='http://digital.em.com.br/apps,1,4/flip-search'
    search_params = {
        'i': 'null',
        'o': '0',
    }

    def start_requests(self):
        if hasattr(self, 'keywords'):
            self.search_params['q'] = getattr(self, 'keywords')
            
            yield Request(self.search_url+'?'+urlencode(self.search_params), callback=self.get_export_urls)

    def get_export_urls(self, resp):
        search_data= json.loads(resp.text).get('ok').get('matches')
        export_urls =[]
        
        for page in search_data:
            id_edicao = page.get('id_edicao')
            id_pagina = page.get('id_pagina')
            num_pag = page.get('numeracao')
            date_str = str(page.get('attrs').get('flip_ordem_i'))
            date = dateparser.parse(date_str,date_formats=['%Y%m%d'])
            # today_date= datetime.date(2017,8,4)
            
            if(datetime.datetime.now().date()==date.date()):
                export_urls.append('http://digital.em.com.br/flip/1/'+str(id_edicao)+'/'+str(id_pagina)+'/original_prez-1600-*.jpg')
        
        for export_url in export_urls:
            newsArticleItem = NewsArticleItem()
            newsArticleItem['url'] = export_url
            
            yield newsArticleItem
