# TesteGlobo
# Consigo Baixar, não sei como pesquisar
import requests
import sys
import urllib
import json
import ast
import os
from bs4 import BeautifulSoup, Comment
from subprocess import call

search_word = 'lula'
ano = 2017
mes = 7
dia = 25
pag=1
diaStr = str(dia).zfill(2)
mesStr = str(mes).zfill(2)
anoStr = str(ano)
endere='/home/labic-redbull/aprendendo/scrapy/impressoes/oGlobo/'+anoStr+mesStr+diaStr

if not os.path.exists(endere):
    os.makedirs(endere)

page_params = {	'issue':'e610'+anoStr+mesStr+diaStr+'00000000001001',
				'page':'1',
				'paper':'A4'
			}

search_params={
				'srchIn':'ALL',
				'srchOrderBy':'Relevance',
				'srchPage':'0',
				'srchStartDate':'2017-07-22',
				'srchStopDate':'2017-07-26',
				'srchText':search_word
}

searchURL = 'http://oglobodigital.oglobo.globo.com/epaper/services/AdvancedSearch_v2.ashx'
#------------------------------SEARCH----------------------------------------

img = requests.request('GET',pagImgURL)
#----------------------------------------------------------------------------

URL=	'http://oglobodigital.oglobo.globo.com/epaper/services/OnlinePrintHandler.ashx?'
page = requests.request('GET',URL,params = page_params)

print(page.status_code)
print(page.content)

soup = BeautifulSoup(page.text,'html.parser')
pagImgURL = soup.select('img')[0]['src']

print('\n'+pagImgURL)

img = requests.request('GET',pagImgURL)
print('pag  '+str(pag)+'   status code:'+str(img.status_code))
fOut = open(endere+'/'+str(pag)+'.png','wb')
fOut.write(img.content)
fOut.close()
