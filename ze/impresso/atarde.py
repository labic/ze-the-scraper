import requests
import sys
import urllib
import json
import ast
import os
import dateparser
import datetime
import re

from bs4 import BeautifulSoup, Comment
from subprocess import call

s = requests.session()
# firstURL = 'http://digital.mflip.com.br/pub/editoraatarde/?key=ab_B34D9960F352AE3C3E7D6994B696DBA7C0CBE260C33B9FDE8BB42A55ED005EA82AE3973F19FFB76B89D74F981C25775C58A594BBADDDD37141B271FDE900C00FE47EC7F13111FE73B2DA090394165D7EB8CC84AF758A8AA8FA5305A2B43F725C56D558F5E75078CBA20056B4F8BEC7746EF4C9CFFA1E08B06003943A5D480578A8D378C7F7345C141FCBBC4E6E6AE4BA794704AA3ADB2EE6FBE497AB191EA49032B1C8F4D3F359666CC23B6A860D0F8663D7CBB57F258730C9EE1C918DD2AF98761F5DCE0BB1C9ECC28597BA9B6B2A89A48A16BF3B59E72764F66CF9897A72D7980AFE087F6601B0E8FF4D7880621C625A2A741763F0531CF79F4A811D10BD039F991264D6E6E76ECD27A8E94C5FFE88C3CD64D31E3A17E92267DCE45364C81A61AC33FF5F45929D2F36D90DA7087C645BF34FB6989F64C24BC923CCFD0F6F9FD38118ECB67AF6E1A96905FDE5013D009069D14D8C4B0B90911667CCAA6564814053240A658FED930A4A5C1010BE90C1D0FBBF9E99E58A7A34E32DB176DED36002E66EEB340AADB8F118A37A685D1F92100C31986DA72EDEA22A25FBF2A40C67F21EA46E36FE2EFDE4EDA7496AC97DC20336D2E63F75DA7E139883706538B1208B9354A37189B2E5AC942AE70B3AD7C5'

initURL='http://edicaodigital.atarde.uol.com.br/'
searchURL = 'http://digital.mflip.com.br/flip/jornal/skins/king/jsp/pesquisa.jsp'
preDownloadUrl = 'http://digital.mflip.com.br/flip/jornal/skins/king/jsp/exportar.jsp'


login_data = {
	'j_idt9':'j_idt9',
	'j_idt9:usuario':'labic.imprensa@gmail.com',
	'j_idt9:j_idt15':'GYRPXQ',
	'j_idt9:cmdAcessar':'acessar',
	'javax.faces.ViewState':'uOTZoy0dBCUnFk6KNEe42fNeNCVQuU669lAYfHL+oQk57qn1uzMGAQmak/BbVlJtH//1KJFgTetWKoVy13F3gq7kNxDnI9GfTHdJLWEWb3tSQgPLoU2FQX1ZZKyHCllhDoaUY9H01bpKEQMiVzNMLi4i+YN5qbgUKUoNwBf9WIKPZZbbLbkqTqP2Mt0I+cVMJsdWem2ocHJe58s9AT3ElqsIo9WR7uNid8WnMxFNs/1Xyzc6GV1Ts0kGjL8Cnh6BmI5jXQ2O2WSPoiLWSCQ3tmElb/qOH0CY6kweVsy/o/Fj+8SdNZWWCuszoEsULmMjFzxgc6yH0BJ5sBI+yIxynBhKUq80JLMPzX/3PJxR8whurC7Ukb7KE0odzYvNB7z+tumKwuCbIwP6beMQD8bU04rG0FCO+0VGu5OE7+hLhJp/tUSQnOr+FUyfoMEsj+d/qO7GjvIEow4do3F0rrtYBIgmkexlha3PSxLGAApEqrwfoiCbADBdtPizsBM8sXEHuXhdRRsNIIc5QVYN3Q5z8Q=='
}

search_data = {
		'edicao':"14464",
		'search':"true",
		'linkedicao':"pub/editoraatarde/",
		'apenasEssa':"true",
		'keywords':"temer"
}

search_params = {
		'idForm':"14464",
		'acervo':"false",
		'labicinkedicao':"pub/editoraatarde/"
}
preDownload_params={'idForm':'283720',
					'idEdicao':'14464',
					'ajaxContent':'true'	
}

# --------------------NA PÁGINA INICIAL-----------
# 
# 	Pega numero necessário, sei la o porquê, pro login
init = s.request('GET',initURL)
initSoup= BeautifulSoup(init.text,'html.parser')
initForm = initSoup.select('form#j_idt9')[0]['action']

loginURL = 'http://edicaodigital.atarde.uol.com.br'+initForm

# -----------------LOGIN---------------------------
# 
# 	Pega na RESPONSE do login uma key, que é usada depois 
login = s.request('POST',loginURL,data=login_data)
print(login.status_code)
firstURL = re.findall('window.location.href = "(.*?)";',login.text)[0]
print (firstURL)

# -------PRIMEIRA PAGINA PÓS-LOGIN
# 
# 	Pega número da edição do dia
first = requests.request('GET',firstURL)
firstSoup= BeautifulSoup(first.text,'html.parser')
editionNumber = re.findall('getCurrentEdition\(\)\{(.*?);',first.text,re.DOTALL)[0].split('return ')[1]
# re.findall('(?<=getCurrentEdition())(.*?)(?=})', s, flags=re.S)
print (editionNumber)


# ---------INPUT-----------------
# 
# 	Pega arquivo .json com lista de termos no modelo {termos:[termo1, termo2, ....]}
# 
# mudar essa parte se necessário
with open('input.json') as fIn:
	fileInput = json.load(fIn)

	termos = fileInput.get('termos') 

# --------SETUP-----------
# 
# 	Pega a data de hoje pra colocar no nome da pasta, cria a pasta se não tiver
today = datetime.datetime.now()
ano = today.year
mes = today.month
dia = today.day

diaStr = str(dia).zfill(2)
mesStr = str(mes).zfill(2)
anoStr = str(ano)

currentAddress = os.path.dirname(os.path.abspath('__file__'))
endere=currentAddress+'/impressoes/ATarde/'+anoStr+mesStr+diaStr
if not os.path.exists(endere):
    os.makedirs(endere)

# ----------SEARCH-----------------
# 
# 	Faz a pesquisa pra saber que paginas tem o termo necessário
pages=[]

for termo in termos:
	search_data['keywords']=termo
	search_data['edicao']=editionNumber
	search = requests.request('POST',searchURL,params = search_params, data = search_data)
	print('search '+str(search.status_code))
	soup = BeautifulSoup(search.text,'html.parser')
	selector = '#item_pesquisa'
	# ---------------coloca numa lista chamada pages as que achou
	for el in soup.select(selector):
		print(el['onclick'])
		temp={}
		# temp['edicao']=el.select('strong')[0].get_text().replace(' Edição número ','')
		temp['img_thumb']=el.select('img')[0]['src']
		temp['pagina']=re.findall('ipg=(.*?)&',el['onclick'])[0]
		temp['edicao']=editionNumber
		# print(temp['pagina'])
		print('edicao: '+temp['edicao'])
		print('pagina: '+temp['pagina'])
		if not any(page['pagina'] == temp['pagina'] for page in pages):
			pages.append(temp)


# -------DOWNLOAD
for page in pages:
	print(page['edicao'])
	# --Pré-Download--------------descobre as URLs dos PDFs de cada pagina

	preDownload_params['idForm']=page['pagina']
	preDownload_params['idEdicao']=page['edicao']

	preDownload = requests.request('GET',preDownloadUrl,params = preDownload_params)
	print(preDownload.status_code)
	preDownloadSoup = BeautifulSoup(preDownload.text,'html.parser')

	selector='[type="button"]'
	numPag=1
	for el in preDownloadSoup.select(selector):
		img_src=el.parent.select('img')[0]['src']
		if(img_src == page['img_thumb']):
			print(img_src)
		# numPag = re.findall('up(.*?)/',el.select('img')[0]['src'])[0]
			downloadURL=el['onclick'].replace("abrePdf('","").replace("');","")

			#-------------Download, baixa o PDF e salva 
			downloadPDF = requests.request('GET',downloadURL)
			with open(endere+'/'+str(page['pagina'])+'-'+str(numPag)+'.pdf', 'wb') as fOut:
				fOut.write(downloadPDF.content)
				print('imprimiu')
			fOut.close()

		numPag=numPag+1



