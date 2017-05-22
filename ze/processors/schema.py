# -*- coding: utf-8 -*-
from slugify import Slugify; slugify = Slugify(to_lower=True)


class AuthorParse():

    def __call__(self, value, loader_context):
        strings_to_clean = ('O Estado de S.Paulo', 'O Estado de S. Paulo',
            u'estadão.com.br', 'por ', 'Por ', 'RIO', '\n', '\t', '\"', '*',
            ' - ', '/', 'DE BRASÍLIA', 'do UOL,', 'O Estado de S.Paulo')
        # TODO: Tratar essa página
        # http://politica.estadao.com.br/noticias/panama-papers,panama-papers-revelam-107-offshores-ligadas-a-personagens-da-lava-jato,10000024501
        
        for s in strings_to_clean:
            value = value.replace(s, '')
        
        value = value.title() if value.isupper() else value
        
        return { 'type': None, 'name': value }


class KeywordsParse():

    def __call__(self, values, loader_context):
        if loader_context['spider_name'] == 'folhadesp':
            values = values.replace('{tags|encode:html_reserved}', '')
        return [slugify(v) for v in values.split(',')]