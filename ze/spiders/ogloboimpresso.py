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
from bs4 import BeautifulSoup, Comment


from ze.spiders import ZeSpider

from ..items.creativework import NewsArticleItem


class OGloboImpresso(ZeSpider):
	name = 'ogloboimpresso'
	today={}

	search_url = 'http://oglobodigital.oglobo.globo.com/epaper/services/AdvancedSearch_v2.ashx'
	pre_download_url=	'http://oglobodigital.oglobo.globo.com/epaper/services/OnlinePrintHandler.ashx'

	search_params={
				'srchIn':'ALL',
				'srchOrderBy':'Relevance',
				'srchPage':'0',
				# 'srchStartDate':'2017-07-22',
				# 'srchStopDate':'2017-07-26',
	}
	pre_download_params = {	
				# 'issue':'e610'+anoStr+mesStr+diaStr+'00000000001001',
				# 'page':'1',
				'paper':'A4'
			}
	def start_requests(self):
		today={
			'year':str(datetime.datetime.now().year),
			'month': str(datetime.datetime.now().month).zfill(2),
			'day': str(datetime.datetime.now().day).zfill(2)
		}
		
		self.pre_download_params['issue']='e610'+today['year']+today['month']+today['day']+'00000000001001'
		self.search_params['srchStartDate']= today['year']+'-'+today['month']+'-'+today['day']
		self.search_params['srchStopDate']=today['year']+'-'+today['month']+'-'+today['day']

		if hasattr(self, 'keywords'):
			query = getattr(self, 'keywords') # ['enem', 'inep', ...]

		self.search_params['srchText']=query
		yield FormRequest(self.search_url, callback=self.get_search_result,
			formdata=self.search_params)

	def get_search_result(self,resp):
		# print(resp.text)

		search_result_soup= BeautifulSoup(resp.text, "lxml")

		result_pages=[]

		for result in search_result_soup.select('article'):
			page_number = result.select('pagenumber')[0].get_text()
			if page_number not in result_pages:
				result_pages.append(page_number)

		for page in result_pages:
			self.pre_download_params['page']=page
			return Request(self.pre_download_url+'?'+urllib.parse.urlencode(self.pre_download_params), callback=self.get_export_url)

	def get_export_url(self, resp):
		export_url = BeautifulSoup(resp.text,'html.parser').select('img')[0]['src']
		newArticleItem = NewsArticleItem()
		newArticleItem['url'] = export_url
		yield newArticleItem

				



				# for result in search_data:
		# 	# print('Data:',result.get('data'))
		# 	today_date_str = datetime.datetime.now().strftime('%d/%m/%Y')
		# 	year = datetime.datetime.now().year
		# 	month = datetime.datetime.now().month
		# 	day = datetime.datetime.now().day
		# 	# print('month', type(month))
		# 	# print('today_str',today_date_str)
		# 	if result.get('caderno') not in tipos_cadernos:
		# 		tipos_cadernos.append(result.get('caderno'))
		# 	if result.get('data')==today_date_str:
		# 		# print('ta dando certo')
		# 		print(result.get('caderno'))
		# 		temp={}
		# 		temp['pag']=result.get('pagina').zfill(2)
		# 		temp['cad']=unidecode.unidecode(result.get('caderno')).lower()
		# 		temp['CAD']=temp['cad'].upper()[0:3]
		# 		temp['dia']=result.get('data')[0:2]
		# 		temp['mes']=result.get('data')[3:5]
		# 		temp['ano']=result.get('data')[6:10]

		# 		export_url= 'http://jconlinedigital.ne10.uol.com.br/restrito/edicoes/'+str(year)+'/'+str(month)+'/'+str(day)+'/1/'+temp['cad']+'/'+temp['mes']+temp['dia']+'_01_'+temp['CAD']+'_'+temp['pag']+'/'+temp['mes']+temp['dia']+'_01_'+temp['CAD']+'_'+temp['pag']+'.jpg'
		# 		newArticleItem = NewsArticleItem()
		# 		newArticleItem['url'] = export_url
		# 		yield newArticleItem