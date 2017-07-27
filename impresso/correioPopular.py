# correioPopular

import requests
import sys
import urllib
import json

payload = {	'email':'labic.imprensa@gmail.com',
			'senha':'Naovaiter',
			'x':'0',
			'y':'0'
			}
queryString = {'j':'1'}
URL = 'http://correio.rac.com.br/jornal_digital/autenticacao-ws/autentica-pdf.php'

req = requests.post(URL, data=json.dumps(payload), params = queryString)

print(req.status_code)
print(req.content)

j=1
curl 'http://correio.rac.com.br/jornal_digital/autenticacao-ws/autentica-pdf.php?j=1' -H 'Host: correio.rac.com.br' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Content-Type: multipart/form-data; boundary=---------------------------1826725119376570943753115959' -H 'Referer: http://correio.rac.com.br/jornal_impresso' -H 'Cookie: __gads=ID=43cf5356a062616b:T=1490107763:S=ALNI_MbzWwo44GqSXvaQK3PIH-oP8aAsIg; __utma=34357666.848043881.1490107764.1501004303.1501006892.12; __utmz=34357666.1500921664.10.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _recadastrar22=true; _fw_plugins=4235503379; _fw_fonts=2007011668; _everfw=590a2fbf9ecbd; _ga=GA1.3.848043881.1490107764; _fw_userName=labic.imprensa%40gmail.com; _fw_signId=; _fw_email=labic.imprensa%40gmail.com; _fw_plan=; _fw_planId=; _fw_planValid=true; __utmc=34357666; PHPSESSID=0bt9ob91cr6fmotmf2o8h96gt5; __utmb=34357666.10.10.1501006892; __utmt=1; nav40191=61a1bcd73a525e3d31aa4dade09|2_207_5:4:1:17:3:11:7:10:14:15:2:16:9:8_1:2:1:1234-1235-1236-1237-1231:2:41:8:BR:196-36-61-62-65:220-221-225-227-259:4:5:8:1000102' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' --data-binary $'-----------------------------1826725119376570943753115959\r\n\r\nContent-Disposition: form-data; name="email"\r\n\r\nlabic.imprensa@gmail.com\r\n-----------------------------1826725119376570943753115959\r\n\r\nContent-Disposition: form-data; name="senha"\r\n\r\nNaovaiter\r\n-----------------------------1826725119376570943753115959\r\n\r\nContent-Disposition: form-data; name="x"\r\n\r\n0\r\n-----------------------------1826725119376570943753115959\r\n\r\nContent-Disposition: form-data; name="y"\r\n\r\n0\r\n-----------------------------1826725119376570943753115959--\r\n'


POST /jornal_digital/autenticacao-ws/autentica-pdf.php?j=1 HTTP/1.1
Host: correio.rac.com.br
'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
# Accept-Language: en-US,en;q=0.5
# Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------17831865491675864493958038888
# Content-Length: 509
Referer: http://correio.rac.com.br/jornal_impresso
# 'Cookie': __gads=ID=43cf5356a062616b:T=1490107763:S=ALNI_MbzWwo44GqSXvaQK3PIH-oP8aAsIg; __utma=34357666.848043881.1490107764.1501004303.1501006892.12; __utmz=34357666.1500921664.10.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _recadastrar22=true; _fw_plugins=4235503379; _fw_fonts=2007011668; _everfw=590a2fbf9ecbd; _ga=GA1.3.848043881.1490107764; _fw_userName=labic.imprensa%40gmail.com; _fw_signId=; _fw_email=labic.imprensa%40gmail.com; _fw_plan=; _fw_planId=; _fw_planValid=true; __utmc=34357666; PHPSESSID=0bt9ob91cr6fmotmf2o8h96gt5; __utmb=34357666.4.10.1501006892; __utmt=1; nav40191=61a1bcd73a525e3d31aa4dade09|2_207_5:4:1:17:3:11:7:10:14:15:2:16:9:8_1:2:1:1234-1235-1236-1237-1231:2:41:8:BR:196-36-61-62-65:220-221-225-227-259:4:5:8:1000102
'Connection': 'keep-alive'
'Upgrade-Insecure-Requests': '1'
header = {	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
			'Connection': 'keep-alive',
			'Upgrade-Insecure-Requests': '1'
		}