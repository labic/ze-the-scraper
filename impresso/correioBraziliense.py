#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import sys
import urllib
import json
import ast
import os
import dateparser
from bs4 import BeautifulSoup, Comment
from subprocess import call

# from scrapy.selector import Selector
# from scrapy.http import HtmlResponse
# import numpy as np
# -------------------------------------READ INPUT JSON------------------------------
termos=[]
dataIn=''
with open('input.json') as fIn:
	fileInput = json.load(fIn)
	dataIn = fileInput.get('data')
	dataIn = dateparser.parse(dataIn)
	termos = fileInput.get('termos') 
fIn.close()
# print(termos)
# print(dataIn)
ano = dataIn.year
mes = dataIn.month
dia = dataIn.day




# return dateparser.parse(value, settings={'TIMEZONE': '+0300','DATE_ORDER': 'DMY'})
# ano = 2017
# mes = 7
# dia = 25
pag=1
diaStr = str(dia).zfill(2)
mesStr = str(mes).zfill(2)
anoStr = str(ano)
currentAddress = os.path.dirname(os.path.abspath('__file__'))
endere=currentAddress+'/impressoes/correio Braziliense/'+anoStr+mesStr+diaStr

if not os.path.exists(endere):
    os.makedirs(endere)

# -----------------INFORMAÇÕES NECESSÁRIAS--------------

senha = 'Naovaitercoxinh4!'
senha_errada ='ioioioiooioi'
issue_orinal = '20252017071100000000001001'

loginURL = 'http://www.cbdigital.com.br/apps,1,120/flip-auth'
printURL='http://www.cbdigital.com.br/flip/1/1627/127882/original_prez-1400-*.jpg'
searchURL='http://www.cbdigital.com.br/apps,1,4/flip-search'
# access_token = 'G8J_q4BIkAUbddUcdMvWXkh2pNeHsJTLsYx6yXQxvgI40kGfLt1f_auOM_u-9iNuuqSilAwYFWdjqHENXatzWQ!!'


login_data={
		'e':'labic.imprensa@gmail.com',
		'p':'labic2752'
}
# -----------------------------------------------------------
# ------------------------LOGIN---------------------------
s=requests.session()
login = s.request('GET',loginURL,params=login_data)
print('login st.cd.: '+str(login.status_code))
dadoImportante = json.loads(login.text).get('ok')
# ---------------------------------------------

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
		'i':'null',
		'o':'0',
		'q':'temer'
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
		print(img.status_code)

		fOut = open(endere+'/'+str(npag)+'.jpg','wb')
		fOut.write(img.content)
		fOut.close()

		print(str(id_edicao)+'  '+str(id_pagina)+'  sc:'+str(img.status_code))
print(len(dados))
# pagImgURL = soup.select('img')[0]['src']

