#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import sys
import urllib
import json
import ast
import os
from bs4 import BeautifulSoup, Comment
from subprocess import call
# 'http://jconlinedigital.ne10.uol.com.br/bibliotecas/php/Download.class.php?data=24%2F07%2F2017&publicacao=1&action=downloadEdicao'

login = 'labic.imprensa@gmail.com'
senha = '205199'
senha_errada ='685388'

loginURL = 'http://jconlinedigital.ne10.uol.com.br/assinantes/auth.php'

login_headers={
				'Connection':'keep-alive',
				'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'
}
login_params={	'email':login,
				'senha':senha
			}

# login = requests.request('POST',loginURL,params = login_params,headers=login_headers)
# print('login '+str(login.status_code))
# print(login.content)
print('oi')
login = requests.post('http://jconlinedigital.ne10.uol.com.br/assinantes/auth.php?email=labic.imprensa%40gmail.com&senha=205199',headers = login_headers)
print('login '+str(login.status_code))
print(login.content)