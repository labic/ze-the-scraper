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

from ze.spiders import ZeSpider

from ..items.creativework import NewsArticleItem

class CorreioBrazilienseImpresso(ZeSpider):


	name = 'correiobrazilienseimpresso'
	# start_urls = ['http://edicaodigital.atarde.uol.com.br/index.xhtml']
	print_url='http://www.cbdigital.com.br/flip/1/1627/127882/original_prez-1400-*.jpg'
	login_url = 'http://www.cbdigital.com.br/apps,1,120/flip-auth'

	search_url='http://www.cbdigital.com.br/apps,1,4/flip-search'
	first_page_url= 'http://www.cbdigital.com.br/correiobraziliense'
	download_text_url='http://www.cbdigital.com.br/apps,1,5/flip-integraa-a-o-jornal-hoje?'

	search_params={
			'i':'null',
			'o':'0',
		}


# http://www.cbdigital.com.br/apps,1,5/flip-integraa-a-o-jornal-hoje?id=20170821+0007+A+eco.pdf&year=2017&month=08&day=21&page=7&id_pagina=129560

	def start_requests(self):

		# login page and get needed cookie

		# for x in xrange(1,50):

		# 	pass

		# if hasattr(self, 'keywords'):
		# 	search_params['q'] = getattr(self, 'keywords') # ['enem', 'inep', ...]
		auth = self.settings.get('SPIDERS_AUTH').get('correiobrazilienseimpresso')

		login_params={
			'e':auth['e'],
			'p':auth['p'],
		}
		yield Request(self.login_url+'?'+urllib.parse.urlencode(login_params), callback=self.get_id_pagina)

	def get_id_pagina(self, resp):

		page_cookie={'__uh':json.loads(resp.text).get('ok')}

		return Request(self.first_page_url, cookies = page_cookie, callback=self.get_export_urls)

	def get_export_urls(self,resp):

		id_pagina_capa = int(re.findall ( 'id_pagina": (.*?),', resp.text, re.DOTALL)[0])
		identificadores=re.findall ( 'identificador": "(.*?)",', resp.text, re.DOTALL)
		# print(identificadores)
		print(str(len(identificadores)))
		export_urls=[]
		for identificador in identificadores:
			date = identificador.split(' ')[0]
			pagina = int(identificador.split(' ')[1])
			print(date)
			print(pagina)

			id_pagina=id_pagina_capa+pagina

			download_text_params = {
				'id':identificador,
				'year':date[0:4],
				'month':date[5:7],
				'day':date[8:10],
				'page':pagina,
				'id_pagina':id_pagina
				}			# pagina=x
			export_urls.append(self.download_text_url+'?'+urllib.parse.urlencode(download_text_params))

		# search_data= json.loads(resp.text).get('ok').get('matches')
		# export_urls =[]
		# for page in search_data:
		# 	id_edicao = page.get('id_edicao')
		# 	id_pagina = page.get('id_pagina')
		# 	num_pag = page.get('numeracao')

		# 	date_str = str(page.get('attrs').get('flip_ordem_i'))

		# 	date=dateparser.parse(date_str,date_formats=['%Y%m%d'])

			# print('//////// GOT IN GET_EXPORT_URLS')
			# if(datetime.datetime.now().date()==date.date()):
			# 	export_urls.append('http://www.cbdigital.com.br/flip/1/'+str(id_edicao)+'/'+str(id_pagina)+'/original_prez-1600-*.jpg')

		for export_url in export_urls:
			newArticleItem = NewsArticleItem()
			newArticleItem['url'] = export_url

			yield newArticleItem

