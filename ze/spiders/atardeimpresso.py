# -*- coding: utf-8 -*-
import re
from urllib.parse import urlparse

from scrapy import Spider
from scrapy.http import Request, FormRequest
from scrapy.selector import Selector

from ..items.creativework import NewsArticleItem

class CorreioPopularImpressoSpider(Spider):

    name = 'atardeimpresso'
    start_urls = ['http://edicaodigital.atarde.uol.com.br/index.xhtml']
    search_url = """http://digital.mflip.com.br/flip/jornal/skins/king/jsp/pesquisa.jsp?idForm={idForm}&acervo=true&linkedicao=pub/editoraatarde/"""
    export_pdf_url = """http://digital.mflip.com.br/flip/jornal/skins/king/jsp/exportar.jsp?idForm={idForm}&idEdicao={idEdicao}&ajaxContent=true"""

    def start_requests(self):
        for u in self.start_urls:
            yield Request(u, callback=self.auth,
                          meta={'dont_cache': True},)

    def auth(self, resp):
        auth = self.settings.get('SPIDERS_AUTH').get('atardeimpresso')
        view_state = resp.selector.css('[name="javax.faces.ViewState"]::attr(value)').extract()[0]

        return FormRequest.from_response(resp, callback=self.after_auth,
                                         formdata={
                                            'j_idt9:usuario': auth['j_idt9:usuario'],
                                            'j_idt9:j_idt15': auth['j_idt9:j_idt15'],
                                            'javax.faces.ViewState': view_state,
                                            'j_idt9:cmdAcessar': 'acessar',
                                            'j_idt9': 'j_idt9'},
                                          meta={'dont_cache': True},)

    def after_auth(self, resp):
        current_edition_url = re.findall('window.location.href = "(.*?)";',
                                         resp.body_as_unicode())[0]
        return Request(current_edition_url,
                       callback=self.go_to_search_edition,
                       meta={'dont_cache': True},)

    def go_to_search_edition(self, resp):
        edition_number = re.findall('getCurrentEdition\(\)\{(.*?);',
                                    resp.body_as_unicode(),
                                    re.DOTALL)[0].split('return ')[1]
        search_data = { 'idForm': edition_number }

        return Request(self.search_url.format(**search_data),
                       callback=self.search_in_edition,
                       meta={'dont_cache': True,
                             'edition_number': edition_number},)

    def search_in_edition(self, resp):
        search_data = {
            'edicao': resp.meta['edition_number'],
            'search': 'true',
            'linkedicao': 'pub/editoraatarde/',
            'apenasEssa': 'true',
            'keywords': 'temer'
        }

        return FormRequest.from_response(resp, callback=self.get_search_urls,
                                         formdata=search_data,
                                         meta={'dont_cache': True,
                                               'keywords': search_data['keywords'],
                                               'edition_number': search_data['edicao']},)

    def get_search_urls(self, resp):
        selector = resp.selector
        # print('\n--------------RESPOSTA-----------\n'+resp.text)
        pages_functions = selector.css('#item_pesquisa::attr(onclick)').extract()
        pages_ids = [re.findall('ipg=(.*?)&',f)[0] for f in pages_functions]


        for page_id in pages_ids:
            params = {'idForm': page_id,
                      'idEdicao': resp.meta['edition_number'],
                      'ajaxContent': 'true',}
            print('\n********PAGEID***********\n'+page_id)
            return FormRequest(self.export_pdf_url.format(**params),
                               headers=resp.headers,
                               callback=self.get_export_url,
                               meta={'edition_number': params['idEdicao'],
                                     'page_id': params['idForm'],})

    def get_export_url(self, resp):
        export_functions = resp.selector.css('[onClick]::attr(onclick)').extract()
        export_urls = [f.replace("abrePdf('","").replace("');","") \
                       for f in export_functions]

        for export_url in export_urls:
        	newArticleItem = NewsArticleItem()
        	newArticleItem['url'] = export_url

        	yield newArticleItem
