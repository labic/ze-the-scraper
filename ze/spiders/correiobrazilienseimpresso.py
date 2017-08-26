# -*- coding: utf-8 -*-
import re
import json
import datetime
import dateparser

from urllib.parse import urlparse
import urllib

from scrapy import Spider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

from . import ZeSpider
from ..items.creativework import NewsArticleItem


class CorreioBrazilienseImpresso(ZeSpider):

    name = 'correiobrazilienseimpresso'
    print_url='http://www.cbdigital.com.br/flip/1/1627/127882/original_prez-1400-*.jpg'
    login_url = 'http://www.cbdigital.com.br/apps,1,120/flip-auth'

    search_url='http://www.cbdigital.com.br/apps,1,4/flip-search'
    first_page_url= 'http://www.cbdigital.com.br/correiobraziliense'
    download_text_url='http://www.cbdigital.com.br/apps,1,5/flip-integraa-a-o-jornal-hoje?'

    search_params={
        'i': 'null',
        'o': '0',
    }

    def start_requests(self):
        auth = self.settings.get('SPIDERS_AUTH').get('correiobrazilienseimpresso')
        login_params={
            'e':auth['e'],
            'p':auth['p'],
        }
        
        yield Request(self.login_url+'?'+urllib.parse.urlencode(login_params), callback=self.get_id_pagina)

    def get_id_pagina(self, resp):
        page_cookie = {'__uh': json.loads(resp.text).get('ok')}
        return Request(self.first_page_url, 
                       cookies=page_cookie, 
                       callback=self.get_export_urls)

    def get_export_urls(self,resp):
        id_pagina_capa = int(re.findall ( 'id_pagina": (.*?),', resp.text, re.DOTALL)[0])
        identificadores=re.findall ( 'identificador": "(.*?)",', resp.text, re.DOTALL)
        export_urls=[]
        
        for identificador in identificadores:
            date = identificador.split(' ')[0]
            pagina = int(identificador.split(' ')[1])
            
            id_pagina=id_pagina_capa+pagina
            
            download_text_params = {
                'id':identificador,
                'year':date[0:4],
                'month':date[5:7],
                'day':date[8:10],
                'page':pagina,
                'id_pagina':id_pagina
                }            # pagina=x
            export_urls.append(self.download_text_url+'?'+urllib.parse.urlencode(download_text_params))
        
        for export_url in export_urls:
            newsArticleItem = NewsArticleItem()
            newsArticleItem['url'] = export_url
            
            yield newsArticleItem
