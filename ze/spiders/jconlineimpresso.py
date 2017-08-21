# -*- coding: utf-8 -*-
import re
import json
import datetime
import dateparser
import unidecode


from urllib.parse import urlparse
import urllib

from scrapy import Spider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

from ze.spiders import ZeSpider

from ..items.creativework import NewsArticleItem


class JCOnlineImpresso(ZeSpider):
	name = 'jconlineimpresso'

	search_url = 'http://jconlinedigital.ne10.uol.com.br/bibliotecas/php/Busca.class.php'

	search_params={
		'action':'listarResultados',
		# 'termo':'falta',
		'pagina':'1',
		'quantidadePorPagina':'50'

	}

	def start_requests(self):
		if hasattr(self, 'keywords'):
			query = getattr(self, 'keywords') # ['enem', 'inep', ...]

		self.search_params['termo']=query
		yield Request(self.search_url+'?'+urllib.parse.urlencode(self.search_params), callback=self.get_search_result)

	def get_search_result(self,resp):
		search_data = json.loads(resp.text).get('resultado')
		tipos_cadernos=[]


		for result in search_data:
			# print('Data:',result.get('data'))
			today_date_str = datetime.datetime.now().strftime('%d/%m/%Y')
			year = datetime.datetime.now().year
			month = datetime.datetime.now().month
			day = datetime.datetime.now().day
			# print('month', type(month))
			# print('today_str',today_date_str)
			if result.get('caderno') not in tipos_cadernos:
				tipos_cadernos.append(result.get('caderno'))
			if result.get('data')==today_date_str:
				# print('ta dando certo')
				print(result.get('caderno'))
				temp={}
				temp['pag']=result.get('pagina').zfill(2)
				temp['cad']=unidecode.unidecode(result.get('caderno')).lower()
				temp['CAD']=temp['cad'].upper()[0:3]
				temp['dia']=result.get('data')[0:2]
				temp['mes']=result.get('data')[3:5]
				temp['ano']=result.get('data')[6:10]

				export_url= 'http://jconlinedigital.ne10.uol.com.br/restrito/edicoes/'+str(year)+'/'+str(month)+'/'+str(day)+'/1/'+temp['cad']+'/'+temp['mes']+temp['dia']+'_01_'+temp['CAD']+'_'+temp['pag']+'/'+temp['mes']+temp['dia']+'_01_'+temp['CAD']+'_'+temp['pag']+'.jpg'
				newArticleItem = NewsArticleItem()
				newArticleItem['url'] = export_url
				yield newArticleItem