import requests
import sys
import urllib
import json
import ast
import os
from bs4 import BeautifulSoup, Comment
from subprocess import call

# from scrapy.selector import Selector
# from scrapy.http import HtmlResponse
# import numpy as np

ano = 2017
mes = 7
dia = 25
pag=1
diaStr = str(dia).zfill(2)
mesStr = str(mes).zfill(2)
anoStr = str(ano)
endere='/home/labic-redbull/aprendendo/scrapy/impressoes/correio Braziliense/'+anoStr+mesStr+diaStr

if not os.path.exists(endere):
    os.makedirs(endere)

senha = 'Naovaitercoxinh4!'
senha_errada ='ioioioiooioi'
issue_orinal = '20252017071100000000001001'

loginURL = 'http://acesso.estadao.com.br/login/autenticar'
printURL='http://www.cbdigital.com.br/flip/1/1627/127882/original_prez-1400-*.jpg'
searchURL='http://www.cbdigital.com.br/apps,1,4/flip-search'
access_token = 'G8J_q4BIkAUbddUcdMvWXkh2pNeHsJTLsYx6yXQxvgI40kGfLt1f_auOM_u-9iNuuqSilAwYFWdjqHENXatzWQ!!'


# login_data={
# 		'conectado':'1',
# 		'emaillog':'labic.imprensa@gmail.com',
# 		'login':'1',
# 		'passwordlog':senha_errada
# }
# print(page.content)
# curl 'http://cdn.navdmp.com/req?v=7&id=61a1bcd73a2986733f87a9eb709|2&acc=23902&url=http%3A//www.estadao.com.br/&tit=As%20%DAltimas%20Not%EDcias%20do%20Dia%20no%20Portal%20do%20Estado%20de%20S.%20Paulo&utm=75670346.1499375602.4.3.utmcsr%3Dacesso.estadao.com.br%7Cutmccn%3D%28referral%29%7Cutmcmd%3Dreferral%7Cutmcct%3D/login/versao-digital' -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.5' -H 'Cache-Control: max-age=0' -H 'Connection: keep-alive' -H 'Cookie: ac3=1; nid=61a1bcd735b2f2c590a322b9809|2|209; __cfduid=d9b06194133eaf79d9a7c17c9327a37561488551475' -H 'Host: cdn.navdmp.com' -H 'Referer: http://www.estadao.com.br/' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'

print_data={
		'accessToken':'bJb-I87mK--FSs0bFF84dNQAstfdnGNzb1VLKM-WZGFa5nAXur2jvpIAfXbgiFITgMmfBpgRWo9Pk9BoCPReSg!!',
		'issue':'2025'+anoStr+mesStr+diaStr+'00000000001001',
		'page':'2',
		'paper':'Letter',
		'scale':'false',
		'scaleToLandscape':'false',
		'useContentProxy':'true'

}

# http://www.cbdigital.com.br/flip/1/1574/124528/original_prez-1600-*.jpg


# opções para dia
# Today , Last3Days
search_data = {
		'i':'null',
		'o':'0',
		'q':'economia'
}

# login = requests.request('GET',loginURL,params = login_data)
# print('login '+str(login.status_code))

search = requests.request('GET',searchURL,params = search_data)
print('search '+str(search.status_code))
dados = search.text
dados= json.loads(dados).get('ok').get('matches')

for pag in dados:
	id_edicao = pag.get('id_edicao')
	id_pagina = pag.get('id_pagina')
	npag = pag.get('numeracao')

	data = pag.get('attrs').get('flip_ordem_i')
	print(data)
	ano_img = str(data)[0:4]
	mes_img = str(data)[4:6]
	dia_img = str(data)[6:8]
	if(dia_img==diaStr and mes_img==mesStr and ano_img==anoStr):
		print(dia_img+'/'+mes_img+'/'+ano_img)
		printURL = 'http://www.cbdigital.com.br/flip/1/'+str(id_edicao)+'/'+str(id_pagina)+'/original_prez-1600-*.jpg'
		img = requests.request('GET',printURL)

		fOut = open(endere+'/'+str(npag)+'.jpg','wb')
		fOut.write(img.content)
		fOut.close()

		print(str(id_edicao)+'  '+str(id_pagina)+'  sc:'+str(img.status_code))
print(len(dados))
# pagImgURL = soup.select('img')[0]['src']

