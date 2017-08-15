# -*- coding: utf-8 -*-

import requests
import sys
import urllib
import json
import ast
import os
import dateparser
import re
import datetime

from bs4 import BeautifulSoup, Comment
from subprocess import call
senhaerrada = '65469161'
senha='labic2'


today = datetime.datetime.now()
termo='frente'

ano = today.year
mes = today.month
dia = today.day

pag=1
diaStr = str(dia).zfill(2)
mesStr = str(mes).zfill(2)
anoStr = str(ano)

s=requests.Session()
login_url='http://www.digital.diariodepernambuco.com.br/apps,1,120/flip-auth'
search_url='http://www.digital.diariodepernambuco.com.br/diariodepernambuco/'+diaStr+'/'+mesStr+'/'+anoStr+'/p1'
login_parameters={
	'e':'labic.imprensa@gmail.com',
	'p':senha
}
header={
	'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0",
	# 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	# 'Accept-Language': 'en-US,en;q=0.5',
	# 'Accept-Encoding': 'gzip, deflate',
	# 'Connection': 'keep-alive',
	# 'Upgrade-Insecure-Requests': '1',
	# 'Cache-Control':'max-age=0',
	# 'Referer':'http://www.digital.diariodepernambuco.com.br/diariodepernambuco/14/08/2017/p1',
	# 'Cookie':'_gads=ID=fe846d791e0619dc:T=1502395782:S=ALNI_MYRGLxszf7qwK3dE7MggyR8slrPHg; cX_S=j6c82mq8q8i5ap6k; nav34748=7cb6d316ded9f7ce1dadd25d109|2_227_5:4:1:3:11:14:2_1:2:1:2:42:61-97-101-116-122:4; cX_G=cx%3Axqppuolptxt37lhe0nl7kobs%3A3vsqf0dyysd2s; __utmt=1; envflipmode=search; __atuvc=29%7C32%2C25%7C33; __atuvs=5991bba2e441ac3100a; cX_P=j66vnknh51bz87v8; __utma=83706755.730908679.1502395776.1502395776.1502718966.2; __utmb=83706755.21.10.1502718966; __utmc=83706755; __utmz=83706755.1502395776.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utma=72984838.56649129.1502395788.1502720979.1502722978.4; __utmb=72984838.39.10.1502722978; __utmc=72984838; __utmz=72984838.1502719036.2.2.utmcsr=diariodepernambuco.com.br|utmccn=(referral)|utmcmd=referral|utmcct=/'


}

# today = dateparser.parse(dataIn,settings={'DATE_ORDER': 'DMY'})


# ano = today.year
# mes = today.month
# dia = today.day

# pag=1
# diaStr = str(dia).zfill(2)
# mesStr = str(mes).zfill(2)
# anoStr = str(ano)

currentAddress = os.path.dirname(os.path.abspath('__file__'))
endere=currentAddress+'/impressoes/ZH/'+anoStr+mesStr+diaStr
if not os.path.exists(endere):
    os.makedirs(endere)



login=s.request('GET',login_url,params=login_parameters, headers=header)
print(login.content)
print (login.url)
cookie=s.cookies.keys()
print('cookies')
print(login.headers)
search_params={'q':termo}
print(search_url)
# search=s.request('GET',search_url,params=search_params)
search = s.request('GET','http://www.digital.diariodepernambuco.com.br/diariodepernambuco/14/08/2017/p1?q=temer')
print(search.url)
print(search.status_code)


fSearch = open('searchpernambuco.html','wb')
fSearch.write(search.content)
fSearch.close()

# 19d3259c7871832000008