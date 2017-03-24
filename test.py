# -*- coding: utf-8 -*-


import urllib.parse as urlparse
from urllib.parse import urlencode

config = {
    'url': 'http://busca.estadao.com.br/modulos/busca-resultado?&'
}
query, editorial, subject, when = None, 'Educação', 'enem', '01/01/2017-22/03/2017'

url_parts = list(urlparse.urlparse(config['url']))
params = {
    'modulo': 'busca-resultado',
    'config[busca][page]': 1,
    'config[busca][params]': []
}

if query:
    params['config[busca][params]'].append('q=' + query)
if editorial:
    params['config[busca][params]'].append('&editoria[]=' + editorial)
if subject:
    params['config[busca][params]'].append('&assunto[]=' + subject)
if when:
    params['config[busca][params]'].append('&quando=' + when)

params['config[busca][params]'] = '&'.join(params['config[busca][params]'])

url_parts[4] = urlencode(params)
print(urlparse.urlunparse(url_parts))