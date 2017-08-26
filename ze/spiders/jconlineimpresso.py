# -*- coding: utf-8 -*-
import re
import json
import datetime
import dateparser
from unidecode import unidecode
from urllib.parse import urlencode

from scrapy import Spider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

from . import ZeSpider
from ..items.creativework import NewsArticleItem


class JCOnlineImpressoSpider(ZeSpider):
    
    name = 'jconlineimpresso'
    search_url = 'http://jconlinedigital.ne10.uol.com.br/bibliotecas/php/Busca.class.php'
    search_params = {
        'action':'listarResultados',
        # 'termo':'falta',
        'pagina':'1',
        'quantidadePorPagina':'50',
    }

    def start_requests(self):
        if hasattr(self, 'keywords'):
            self.search_params['termo'] = getattr(self, 'keywords')
            
            yield Request(self.search_url+'?'+urlencode(self.search_params), 
                          callback=self.get_search_result)

    def get_search_result(self,resp):
        search_data = json.loads(resp.text).get('resultado')
        tipos_cadernos = []


        for result in search_data:
            today_date_str = datetime.datetime.now().strftime('%d/%m/%Y')
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            day = datetime.datetime.now().day
            
            if result.get('caderno') not in tipos_cadernos:
                tipos_cadernos.append(result.get('caderno'))
            
            if result.get('data')==today_date_str:
                temp = {
                    'pag': result.get('pagina').zfill(2),
                    'cad': unidecode(result.get('caderno')).lower(),
                    'CAD': unidecode(result.get('caderno')).upper()[0:3],
                    'dia': result.get('data')[0:2],
                    'mes': result.get('data')[3:5],
                    'ano': result.get('data')[6:10]
                }
                export_url= 'http://jconlinedigital.ne10.uol.com.br/restrito/edicoes/'+str(year)+'/'+str(month)+'/'+str(day)+'/1/'+temp['cad']+'/'+temp['mes']+temp['dia']+'_01_'+temp['CAD']+'_'+temp['pag']+'/'+temp['mes']+temp['dia']+'_01_'+temp['CAD']+'_'+temp['pag']+'.jpg'
                newsArticleItem = NewsArticleItem()
                newsArticleItem['url'] = export_url
                
                yield newsArticleItem
