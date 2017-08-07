import requests
import sys
import urllib
import json
import ast
import os
import dateparser

from bs4 import BeautifulSoup, Comment
from subprocess import call


senha = 'Naovaiter'
senha_errada ='ioioioiooioi'

loginURL = 'http://flipzh.clicrbs.com.br/jornal-digital/flip/loginEdicao.do'
# printURL='http://digital.em.com.br/flip/1/2134/124533/original_prez-1600-*.jpg'
searchURL='http://flipzh.clicrbs.com.br/jornal-digital/flip/jornal/skins/king/jsp/pesquisa.jsp'
# imgURL='http://flipzh.clicrbs.com.br/jornal-digital/files/flip/RBS/1885/up24/15017132743301.jpg'
login_data={

	'username':'labic.imprensa@gmail.com',
	'senha':senha
}


def imprime_jornal(termo,diaStr,mesStr,anoStr):
	
	search_data = {
			'edicao':"3258",
			'search':"true",
			'linkedicao':"pub/gruporbs/",
			'apenasEssa':"true",
			'keywords':"temer"
	}

	search_params = {
			'idForm':"3258",
			'acervo':"false",
			'labicinkedicao':"pub/gruporbs/"
	}

	print_data={
			'accessToken':'bJb-I87mK--FSs0bFF84dNQAstfdnGNzb1VLKM-WZGFa5nAXur2jvpIAfXbgiFITgMmfBpgRWo9Pk9BoCPReSg!!',
			'issue':'2025'+anoStr+mesStr+diaStr+'00000000001001',
			'page':'2',
			'paper':'Letter',
			'scale':'false',
			'scaleToLandscape':'false',
			'useContentProxy':'true'

	}


	search = s.request('POST',searchURL,params = search_params, data = search_data)
	print('search '+str(search.status_code))
	# print(search.content)
	soup = BeautifulSoup(search.text,'html.parser')
	selector = '#item_pesquisa'
	pages=[]
	for el in soup.select(selector):
		print(el['onclick'])
		temp={}
		temp['edicao']=el.select('strong')[0].get_text().replace(' Edição número ','')
		print(temp['edicao'])
	exit()

	for pag in pages:
		id_edicao = pag.get('id_edicao')
		id_pagina = pag.get('id_pagina')
		npag = pag.get('numeracao')
		data = pag.get('attrs').get('flip_ordem_i')
		ano_img = str(data)[0:4]
		mes_img = str(data)[4:6]
		dia_img = str(data)[6:8]
		print('dia '+diaStr+' '+dia_img)
		print('mes '+mesStr+' '+mes_img)
		print('ano '+anoStr+' '+ano_img)

		if(dia_img==diaStr and mes_img==mesStr and ano_img==anoStr):
			print(dia_img+'/'+mes_img+'/'+ano_img)
			print('foi')
			printURL = 'http://digital.em.com.br/flip/1/'+str(id_edicao)+'/'+str(id_pagina)+'/original_prez-1600-*.jpg'
			img = requests.request('GET',printURL)

			fOut = open(endere+'/'+str(npag)+'.jpg','wb')
			fOut.write(img.content)
			fOut.close()

			print(str(data)+'  '+str(id_edicao)+'  '+str(id_pagina)+'  sc:'+str(img.status_code))
	print(len(pages))



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
endere=currentAddress+'/impressoes/Estado de Minas/'+anoStr+mesStr+diaStr
if not os.path.exists(endere):
    os.makedirs(endere)

# -----------------LOGIN-------------------
s = requests.session()
login = s.request('GET',loginURL, params = login_data)
print('s.c.:'+str(login.status_code))
print(login.content)
for termo in termos:
	imprime_jornal(termo,diaStr,mesStr,anoStr)

