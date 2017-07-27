#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import sys
import urllib
import json
import ast
import os



from subprocess import call
# from scrapy.selector import Selector
# from scrapy.http import HtmlResponse
# import numpy as np

ano = 2017
mes = 7
dia = 13
pag=1
diaStr = str(dia).zfill(2)
mesStr = str(mes).zfill(2)
anoStr = str(ano)
endere='/home/labic-redbull/aprendendo/scrapy/impressoes/folha/'+anoStr+mesStr+diaStr

if not os.path.exists(endere):
    os.makedirs(endere)

username ='labic.imprensa@gmail.com'
senha = 'Naovaitercoxinh4!'
senha_errada ='ioioioiooioi'
issue_orinal = '20252017071100000000001001'
header = {
		'Host': 'sunflower.digitalpages.com.br',
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate, br',
		'X-RDP-Reader': 'X-RDP-Reader',
		'Referer': 'http://edicaodigital.folha.uol.com.br/index.html',
		'Origin': 'http://edicaodigital.folha.uol.com.br',
		# Cookie: CookiesHelper="yYV9Wa5EriPT4++FMK9vtdPOMJD5eCprT7DjJvqxWew="; JSESSIONID=sf01i011kblj89r7byum10x11zpltby6e.sf01i01; AWSELB=A1074B43104F1AA38B159EF2C11EB9186A68B59BD874053C2B3A03638AF87E7F426242D5288E66C101D1E02CEAA13FAD216C9F3DB316C50239A5DDAF5C11A5C00A505B09EC
		'Connection': 'keep-alive'
}

loginURL = 'http://rdpcontroller.digitalpages.com.br/folha/users/sign_in.json?skip_snowplow=true'
# printURL = 'https://sunflower.digitalpages.com.br/html/getEditionJSON?publicationId=8&editionId=67085&timestamp=1501019171&token=78c0001eb52eae9f21eff101e365e0ed&userUid=labic.imprensa%40gmail.com&editionUid=32255&taste=false'
printURL='https://sunflower.digitalpages.com.br/html/getDownloadUrl'
searchURL='https://sunflower.digitalpages.com.br/html/searchOnEdition'


login_data={
			'user[login]' : username,
			'user[password]' : senha,
			'user[remember]' : 'true'
			}
# print(page.content)
# curl 'http://cdn.navdmp.com/req?v=7&id=61a1bcd73a2986733f87a9eb709|2&acc=23902&url=http%3A//www.estadao.com.br/&tit=As%20%DAltimas%20Not%EDcias%20do%20Dia%20no%20Portal%20do%20Estado%20de%20S.%20Paulo&utm=75670346.1499375602.4.3.utmcsr%3Dacesso.estadao.com.br%7Cutmccn%3D%28referral%29%7Cutmcmd%3Dreferral%7Cutmcct%3D/login/versao-digital' -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.5' -H 'Cache-Control: max-age=0' -H 'Connection: keep-alive' -H 'Cookie: ac3=1; nid=61a1bcd735b2f2c590a322b9809|2|209; __cfduid=d9b06194133eaf79d9a7c17c9327a37561488551475' -H 'Host: cdn.navdmp.com' -H 'Referer: http://www.estadao.com.br/' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'

print_data={
		'editionId':"66862",
		'pageSetId':"1788542"
}

search_data = {
			'editionId':'66862',
			'page':'0',
			'per_page':'100',
			'term':'temer'
}
s=requests.session()#config={'verbose': sys.stderr})
login = s.request('POST',loginURL,data = login_data, headers=header)
print('login '+str(login.status_code))
print(json.dumps(json.loads(login.text), indent=4))

login_data = login.text
login_data = json.loads(login_data)# print(data)
login_token = login_data.get('login_token')
authentication_token = login_data.get('authentication_token')

token = login_token


print_data['userUid'] = username
print_data['token'] = token

# print_data['authentication_token'] = authentication_token
# print_data['login_token']=login_token

search = s.request('GET',searchURL,params = search_data,headers=header)
print('search '+str(search.status_code))
# print(search.content)

data = search.text
data = json.loads(data)# print(data)
data = data.get('results')
lista_primeiro=[]
lista_economia=[]
lista_segundo=[]
lista_cotidiano_esporte=[]
lista_cotidiano_nacional=[]
lista_ilustrada=[]
lista_turismo=[]
pages=[]

for found in data:
	page = found.get('Page')
	section = found.get('section_name')
	print(section)
	# # POSSÍVEIS
	# 'page_label': '1',
	# 'edition_id': 57949,
	# 'page_id': 3214717,
	#  'page_index': 0
	pagina = int(found.get('page_id'))
	print (pagina)
	if (section=='Primeiro Caderno'):
		if pagina not in lista_primeiro:
			lista_primeiro.append(pagina)
	if (section=='Economia & Negócios'):
		if pagina not in lista_economia:
			lista_economia.append(pagina)
	if (section=='Caderno 2'):
		if pagina not in lista_segundo:
			lista_segundo.append(pagina)
	if (section=='Cotidiano e Esporte'):
		if pagina not in lista_cotidiano_esporte:
			lista_segundo.append(pagina)
	if (section=='Ilustrada'):
		if pagina not in lista_ilustrada:
			lista_segundo.append(pagina)
	if (section=='Turismo'):
		if pagina not in lista_turismo:
			lista_segundo.append(pagina)
	if (section=='Cotidiano - Edição Nacional'):
		if pagina not in lista_cotidiano_nacional:
			lista_segundo.append(pagina)
	pages.append(pagina)
# 	if page not in pages:
# 		pages.append(page)
# print(pages)


# # ---------------Pega IMGS---------------
for pag in pages:

# 	print_data={
# 		'editionId':"57949",
# 		'pageSetId':"3214701"
# }
	printPage = s.request('GET',printURL, params = print_data,headers=header)
	print('pag  '+str(pag)+'   status code:'+str(printPage.status_code))
	print(printPage.url)
	data = printPage.text
	data = json.loads(data)
	print(data)
 	# pagImgURL = data.get('Data').get('Src')
# 	img = requests.request('GET',pagImgURL)
# 	print('pag  '+str(pag)+'   status code:'+str(img.status_code))
# 	fOut = open(endere+'/'+str(pag)+'.png','wb')
# 	fOut.write(img.content)
# 	fOut.close()


# https://sunflower.digitalpages.com.br/html/getDownloadUrl?editionId=57949&pageSetId=3214718

# https://sunflower.digitalpages.com.br/html/getDownloadUrl?editionId=57949&pageSetId=3214720