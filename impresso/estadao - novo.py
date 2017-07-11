#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import sys
import urllib
import json
import ast


from subprocess import call
# from scrapy.selector import Selector
# from scrapy.http import HtmlResponse
# import numpy as np

ano = 2017
mes = 7
dia = 1
pag=1
diaStr = str(dia).zfill(2)
mesStr = str(mes).zfill(2)
anoStr = str(ano)

senha = 'Naovaitercoxinh4!'
senha_errada ='ioioioiooioi'
issue_orinal = '20252017071100000000001001'

loginURL = 'http://acesso.estadao.com.br/login/autenticar'
printURL='http://services.pressreader.com/se2skyservices/print/GetImageByRegion/'
searchURL='http://services.pressreader.com/se2skyservices/search/GetArticles/'
access_token = 'G8J_q4BIkAUbddUcdMvWXkh2pNeHsJTLsYx6yXQxvgI40kGfLt1f_auOM_u-9iNuuqSilAwYFWdjqHENXatzWQ!!'

login_data={
		'conectado':'1',
		'emaillog':'labic.imprensa@gmail.com',
		'login':'1',
		'passwordlog':senha_errada
}
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
# opções para dia
# Today , Last3Days
search_data = {
		'OrderBy':'Relevance',
		'PageSize':'20',
		'Range':'Today',
		'RowNumber':'0',
		'SearchIn':'ALL',
		'SearchText':'temer',
		'StartDate':'',
		'StopDate':'',
		'accessToken':access_token
}

login = requests.request('GET',loginURL,params = login_data)
print('login '+str(login.status_code))

search = requests.request('GET',searchURL,params = search_data)
print('search '+str(search.status_code))

data = search.text
data = json.loads(data)
data = data.get('Items')
pages=[]
for found in data:
	page = found.get('Page')
	if page not in pages:
		pages.append(page)
print(pages)


# ---------------Pega IMGS---------------
for pag in pages:

	print_data={
		'accessToken':'bJb-I87mK--FSs0bFF84dNQAstfdnGNzb1VLKM-WZGFa5nAXur2jvpIAfXbgiFITgMmfBpgRWo9Pk9BoCPReSg!!',
		'issue':'2025'+anoStr+mesStr+diaStr+'00000000001001',
		'page':str(pag),
		'paper':'Letter',
		'scale':'false',
		'scaleToLandscape':'false',
		'useContentProxy':'true'
	}

	printPage = requests.request('GET',printURL,params = print_data)
	data = printPage.text
	data = json.loads(data)
	pagImgURL = data.get('Data').get('Src')
	img = requests.request('GET',pagImgURL)
	print(str(pag)+str(img.status_code))
	fOut = open(str(pag)+'.png','wb')
	fOut.write(img.content)
	fOut.close()


