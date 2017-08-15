# -*- coding: utf-8 -*-

import requests
import sys
import urllib
import json
import ast
import os
import dateparser
import re

from bs4 import BeautifulSoup, Comment
from subprocess import call


senha = 'Naovaiter'
senha_errada ='ioioioiooioi'
pre_login_URL='http://flipzh.clicrbs.com.br/jornal-digital/pub/gruporbs/login.jsp'
loginURL = 'http://flipzh.clicrbs.com.br/jornal-digital/flip/loginEdicao.do'
# printURL='http://digital.em.com.br/flip/1/2134/124533/original_prez-1600-*.jpg'
searchURL='http://flipzh.clicrbs.com.br/jornal-digital/flip/jornal/skins/king/jsp/pesquisa.jsp'
imgURL='http://flipzh.clicrbs.com.br/jornal-digital/files/flip/RBS/1910/up65/15023262695051.jpg'
pre_download_url='http://flipzh.clicrbs.com.br/jornal-digital/flip/jornal/skins/king/jsp/imprimir.jsp'
login_data={

	'username':'labic.imprensa@gmail.com',
	'senha':senha
}
search_data = {
		'search':"true",
		'linkedicao':"pub/gruporbs/",
		'apenasEssa':"true",
}

search_params = {

		'acervo':"false",
		'labicinkedicao':"pub/gruporbs/"
}

pre_download_params = {
	'ajaxContent':'true',
}



termos=[]
dataIn=''
with open('input.json') as fIn:
	fileInput = json.load(fIn)
	dataIn = fileInput.get('data')
	dataIn = dateparser.parse(dataIn,settings={'DATE_ORDER': 'DMY'})
	termos = fileInput.get('termos') 
fIn.close()

ano = dataIn.year
mes = dataIn.month
dia = dataIn.day

pag=1
diaStr = str(dia).zfill(2)
mesStr = str(mes).zfill(2)
anoStr = str(ano)
currentAddress = os.path.dirname(os.path.abspath('__file__'))
endere=currentAddress+'/impressoes/ZH/'+anoStr+mesStr+diaStr
if not os.path.exists(endere):
    os.makedirs(endere)

# -----------------LOGIN-------------------
s = requests.session()
login = s.request('GET',loginURL, params = login_data)
print('s.c.:'+str(login.status_code))
print(login.content)
# for termo in termos:
# 	imprime_jornal(termo,diaStr,mesStr,anoStr)
termo=termos[0]



# print_data={
# 		'accessToken':'bJb-I87mK--FSs0bFF84dNQAstfdnGNzb1VLKM-WZGFa5nAXur2jvpIAfXbgiFITgMmfBpgRWo9Pk9BoCPReSg!!',
# 		'issue':'2025'+anoStr+mesStr+diaStr+'00000000001001',
# 		'page':'2',
# 		'paper':'Letter',
# 		'scale':'false',
# 		'scaleToLandscape':'false',
# 		'useContentProxy':'true'

# }

search_header={
	'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
}
pre_login=requests.request('GET',pre_login_URL)
pre_login_soup = BeautifulSoup(pre_login.text,'html.parser')
login_data['hash']=pre_login_soup.select('[name="hash"]')[0]['value']
login_data['folder']=pre_login_soup.select('[name="folder"]')[0]['value']
login_data['modelo']=pre_login_soup.select('[name="modelo"]')[0]['value']
# login_data['date']=pre_login_soup.select('[name="date"]')[0]['value']
# login_data['numero']=pre_login_soup.select('[name="numero"]')[0]['value']

login=requests.request('POST',loginURL,data=login_data)
editionNumber=BeautifulSoup(login.text,'html.parser').select('#edicaoId')[0]['value']
print('EditionNumber '+str(editionNumber))

search_data['edicao']=editionNumber
search_data['keywords']='eleição'
search_params['idForm']=editionNumber

	



search = s.request('POST',searchURL,params = search_params, data = search_data, headers=search_header)
print('search '+str(search.status_code))
print('search url'+search.url)
search
search_soup = BeautifulSoup(search.text,'html.parser')
print(len(search_soup.select('#item_pesquisa')))

selector = '#item_pesquisa'
pages=[]
for el in search_soup.select(selector):
	print(el['onclick'])
	temp={}
	# temp['edicao']=el.select('strong')[0].get_text().replace(' Edição número ','')
	temp['pagina']=re.findall('ipg=(.*?)&',el['onclick'])[0]
	temp['img_thumb']=el.select('img')[0]['src']
	temp['edicao']=editionNumber
	pages.append(temp)
	print(temp['edicao'])

for page in pages:

	pre_download_params['idForm']='anch'+str(page['pagina'])
	pre_download_params['idEdicao']=page['edicao']

	pre_download = requests.request('GET',pre_download_url,params = pre_download_params)
	print('pre download s.c. '+str(pre_download.status_code))
	pre_download_soup = BeautifulSoup(pre_download.text,'html.parser')

	selector='[type="button"]'
	numPag=1
	for el in pre_download_soup.select(selector):
		img_src=el.parent.select('img')[0]['src']
		if(img_src == page['img_thumb']):
			print(img_src)
		# numPag = re.findall('up(.*?)/',el.select('img')[0]['src'])[0]
			downloadURL='http://flipzh.clicrbs.com.br/jornal-digital/'+el['onclick'].replace("printLoad('","").replace("');","")

			#-------------Download, baixa o PDF e salva 
			downloadJPG = requests.request('GET',downloadURL)
			with open(endere+'/'+str(page['pagina'])+'-'+str(numPag)+'.JPG', 'wb') as fOut:
				fOut.write(downloadJPG.content)
				print('imprimiu')
			fOut.close()

		numPag=numPag+1

	

		# print(str(data)+'  '+str(id_edicao)+'  '+str(id_pagina)+'  sc:'+str(img.status_code))
# print(len(pages))



