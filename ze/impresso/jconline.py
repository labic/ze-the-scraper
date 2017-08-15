#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import sys
import urllib
import json
import ast
import os
import dateparser
import unidecode
import datetime

from bs4 import BeautifulSoup, Comment
from subprocess import call
# 'http://jconlinedigital.ne10.uol.com.br/bibliotecas/php/Download.class.php?data=24%2F07%2F2017&publicacao=1&action=downloadEdicao'
{'capa':'CAP',
	'politica':'POL',
	'economia':'ECO',
	'cidades':'CID',
	'opiniao jc':'OPI'}
login = 'labic.imprensa@gmail.com'
senha = '205199'
senha_errada ='685388'

loginURL = 'http://jconlinedigital.ne10.uol.com.br/assinantes/auth.php'
searchURL = 'http://jconlinedigital.ne10.uol.com.br/bibliotecas/php/Busca.class.php'

login_headers={
				'Content-Type':'application/x-www-form-urlencoded',
				'Connection':'keep-alive',
				'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
				'X-Requested-With': 'XMLHttpRequest'
			}

login_data={	'email':login,
				'senha':senha
			}
search_params={
		'action':'listarResultados',
		'termo':'falta',
		'pagina':'1',
		'quantidadePorPagina':'50'

}
tipos=[]
# http://jconlinedigital.ne10.uol.com.br/restrito/edicoes/1/8/2017/1/politica/0801_01_POL_4/0801_01_POL_4.jpg

imgURL='http://jconlinedigital.ne10.uol.com.br/restrito/edicoes/2017/8/1/1/politica/0801_01_POL_03/0801_01_POL_03.jpg'
# 'http://jconlinedigital.ne10.uol.com.br/restrito/edicoes/'+str(ano)+'/'+str(mes)+'/'+str(dia)+'/1/'+caderno+'/'+mesStr+diaStr+'_01_'+CADERNO+'_'+pagStr+'/'+mesStr+diaStr+'_01_'+CADERNO+'_'+pagStr+'.jpg'
def imprime_jornal(termo):
	paraPrint=[]
	search_params['termo']=termo
	search = requests.request('GET',searchURL,params=search_params)
	# with open('search.json','wb') as fSearch:
	# 	fSearch.write(search.content)
	# fSearch.close()
	# print(dataStr)

	# print(search.text)
	results = json.loads(search.text)
	results=results.get('resultado')
	# results = json.loads(search.text).get('resultado')
	for result in results:
		if result.get('caderno') not in tipos:
			tipos.append(result.get('caderno'))
		if result.get('data')==dataStr:
			print(result.get('caderno'))
			temp={}
			temp['pag']=result.get('pagina').zfill(2)
			temp['cad']=unidecode.unidecode(result.get('caderno')).lower()
			temp['CAD']=temp['cad'].upper()[0:3]
			temp['dia']=result.get('data')[0:2]
			temp['mes']=result.get('data')[3:5]
			temp['ano']=result.get('data')[6:10]
			# temp['texto']=result.get('texto')
			paraPrint.append(temp)
			print(temp)
			imgURL= 'http://jconlinedigital.ne10.uol.com.br/restrito/edicoes/'+str(ano)+'/'+str(mes)+'/'+str(dia)+'/1/'+temp['cad']+'/'+mesStr+diaStr+'_01_'+temp['CAD']+'_'+temp['pag']+'/'+mesStr+diaStr+'_01_'+temp['CAD']+'_'+temp['pag']+'.jpg'
			img=requests.request('GET',imgURL)
			print(img.status_code)
			print(img.url)
			# fOut = open(endere+'/'+temp['cad']+temp['pag']+'.jpg','wb')
			# fOut.write(img.content)
			# fOut.close()
	print (tipos)

s = requests.session()
login = s.post(loginURL,data = login_data,headers = login_headers)
print('login '+str(login.status_code))
print(login.content)


# http://jconlinedigital.ne10.uol.com.br/restrito/edicoes/2017/8/1/1/cultura%201/0801_02_CUL_02/0801_02_CUL_02.jpg
# http://jconlinedigital.ne10.uol.com.br/restrito/edicoes/2017/8/1/1/cultura/0801_01_CUL_16/0801_01_CUL_16.jpg
termos=[]
dataIn=''
with open('input.json') as fIn:
	fileInput = json.load(fIn)
	dataIn = fileInput.get('data')
	dataIn = dateparser.parse(dataIn,settings={'DATE_ORDER': 'DMY'})
	termos = fileInput.get('termos')
fIn.close()

dataIn=datetime.datetime.today()
ano = dataIn.year
mes = dataIn.month
dia = dataIn.day

pag=1
diaStr = str(dia).zfill(2)
mesStr = str(mes).zfill(2)
anoStr = str(ano)
dataStr = diaStr+'/'+mesStr+'/'+anoStr
currentAddress = os.path.dirname(os.path.abspath('__file__'))
endere=currentAddress+'/impressoes/jconline/'+anoStr+mesStr+diaStr
if not os.path.exists(endere):
    os.makedirs(endere)

for termo in termos:
	print(termo)
	imprime_jornal(termo)

