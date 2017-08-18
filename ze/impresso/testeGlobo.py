# -*- coding: utf-8 -*-

import requests
import sys
import urllib
import json
import ast
import os
import dateparser
import re
import datetime

from bs4 import BeautifulSoup, Comment
from subprocess import call

page_URL=	'http://oglobodigital.oglobo.globo.com/epaper/services/OnlinePrintHandler.ashx?'



today = datetime.datetime.now()
termo='frente'

ano = today.year
mes = today.month
dia = today.day

pag=1
diaStr = str(dia).zfill(2)
mesStr = str(mes).zfill(2)
anoStr = str(ano)


termo='temer'

currentAddress = os.path.dirname(os.path.abspath('__file__'))
endere=currentAddress+'/impressoes/oGlobo/'+anoStr+mesStr+diaStr
if not os.path.exists(endere):
    os.makedirs(endere)



page_params = {	'issue':'e610'+anoStr+mesStr+diaStr+'00000000001001',
				'page':'1',
				'paper':'A4'
			}

search_data={
				'srchIn':'ALL',
				'srchOrderBy':'Relevance',
				'srchPage':'0',
				'srchStartDate':'2017-08-18',
				'srchStopDate':'2017-08-18',
				'srchText':termo
}
search_data['srchText']=termo
search_data['srchStartDate']=anoStr+'-'+mesStr+'-'+diaStr
search_data['srchStopDate']=anoStr+'-'+mesStr+'-'+diaStr

search_url = 'http://oglobodigital.oglobo.globo.com/epaper/services/AdvancedSearch_v2.ashx'
#------------------------------SEARCH----------------------------------------
search = requests.request('GET',search_url,data=search_data)
soup= BeautifulSoup(search.text, "lxml")
# print(search.text)
print(soup.Article)
print(len(soup.find_all('article')))

selector = 'article'
pages=[]
for el in soup.select(selector):
	page_number = el.select('pagenumber')[0].get_text()
	if page_number not in pages:
		pages.append(page_number)

fSearch = open('globoSearch.xml','wb')
fSearch.write(search.content)
fSearch.close()

for page in pages:
	print(page)
	page_params['page']=page
	pre_download_page = requests.request('GET',page_URL,params = page_params)
	print(pre_download_page.url)
	soup = BeautifulSoup(pre_download_page.text,'html.parser')
	pagImg_URL = soup.select('img')[0]['src']

	print('\n'+pagImg_URL)

	img = requests.request('GET',pagImg_URL)
	print('page number  '+str(page)+'   status code:'+str(img.status_code))
	fOut = open(endere+'/'+str(page)+'.png','wb')
	fOut.write(img.content)
	fOut.close()
