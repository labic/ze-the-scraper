#
#	TA ENTRANDO COM LOGIN E SENHA YAY!!!!!!!!!!!!!!!!!1
#
#	FALTA:	acessar e baixar coisas
#
import requests
import sys
import urllib

from subprocess import call
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import numpy as np


ano = 2017
mes = 7
dia = 1
pag=1
diaStr = str(dia).zfill(2)
mesStr = str(mes).zfill(2)
anoStr = str(ano)

# searchURL='http://digital.estadao.com.br/consultas/BuscaTermo.asp?SessionId=14961071&edicao=20170710&pagina=1&publicacao=1&termo=temer'
searchURL='http://digital.estadao.com.br/consultas/BuscaTermo.asp'

teste1URL='http://digital.estadao.com.br/home.asp'

printURL='http://services.pressreader.com/se2skyservices/print/GetImageByRegion/?accessToken=bJb-I87mK--FSs0bFF84dNQAstfdnGNzb1VLKM-WZGFa5nAXur2jvpIAfXbgiFITgMmfBpgRWo9Pk9BoCPReSg!!&useContentProxy=true&issue=20252017071100000000001001&page=2&paper=Letter&scale=false&scaleToLandscape=false'

print_data={
		'accessToken':'bJb-I87mK--FSs0bFF84dNQAstfdnGNzb1VLKM-WZGFa5nAXur2jvpIAfXbgiFITgMmfBpgRWo9Pk9BoCPReSg!!',
		'issue':'20252017071100000000001001',
		'page':'2',
		'paper':'Letter',
		'scale':'false',
		'scaleToLandscape':'false',
		'useContentProxy':'true'

}

search_data={
		'SessionId':'14961095',
		'edicao':'20170710',
		'pagina':'1',
		'publicacao':'1',
		'termo':'bom'
}


search = requests.request('POST',searchURL,params = search_data)
printPage = requests.request('GET',printURL,params = print_data)

print(printPage.status_code)




f = open('respostaDaSearch', 'wb')
f.write(search.content)
f.close()

# print(search.content)
body = search.content
completo_pagina=Selector(text=body).xpath('//pagina/text()').extract()
completo_caderno=Selector(text=body).xpath('//caderno/text()').extract()
lista=[]
print (completo_pagina)
print(completo_caderno)
lista_primeiro=[]
lista_economia=[]
lista_segundo=[]
lista = np.column_stack((completo_caderno, completo_pagina))
for idx,x in enumerate(completo_caderno):
	pagina = completo_pagina[idx]
	if (x=='Primeiro Caderno'):
		if pagina not in lista_primeiro:
			lista_primeiro.append(int(pagina))
	if (x=='Economia & Negócios'):
		if pagina not in lista_economia:
			lista_economia.append(int(pagina))
	if (x=='Caderno 2'):
		if pagina not in lista_segundo:
			lista_segundo.append(int(pagina))

print(lista_primeiro)

listas = {'A':lista_primeiro,'B':lista_economia,'C':lista_segundo}

for cad,lista in listas.items():
	print('oi'+cad)
	print(lista)
	for x in lista:
		print('oi'+x)

		pag=x
		pagStr =str(pag)
		URL ='http://digital.estadao.com.br/eds/'+anoStr+'/'+mesStr+'/'+diaStr+'/'+cad+'/paginas/ampliadas/'+cad+pagStr+'.swf'

		page = requests.request('GET',URL)
		print(page.status_code)
		if(page.status_code==200):

			f = open('estadao/'+cad+pagStr+'.swf', 'wb')
			f.write(page.content)
			f.close()
			call(["swfrender", 'estadao/'+cad+pagStr+'.swf','-o',cad+pagStr+'.png'])
		else:
			break

# http://digital.estadao.com.br/eds/2017/07/10/C/paginas/ampliadas/C3.swf

# print (type(page.content))



# URLS IMPORTANTES!!!!!!!!!!!!!!!!1
# http://services.pressreader.com/se2skyservices/search/GetArticles/?accessToken=5hYKWlekOaROe8zokRHX_7-40ikXDFO75bA-tUxa5OYRW2iG4kmtvrLs3m0vs7SmmQsn_z0JhXBP6Xrn-kUTPg!!&SearchText=temer&Range=Last3Days&SearchIn=ALL&StartDate=&StopDate=&OrderBy=Relevance&RowNumber=0&PageSize=20

# https://cdn2-img.pressreader.com/pressdisplay/docserver/getimage.aspx?file=20252017071100000000001001&page=3&scale=194&left=0&top=400&right=200&bottom=600&layer=fg&ticket=ALc4r36YRCk81gNzUVDGDB8%3D



# http://images2.pressdisplay.com/pressdisplay/docserver/getimage.aspx?Et49k2V7vpdop37IEf2eCy2Hul7ifVAWL/Co+vG1IP97u9/pW/vt378lxvVsmGjvrYd4o7WqRgjrj9EUYA73utLG9ILy0YcpJqFPhjwnRiji3YEYqzisLKvGKtha3i36