# -*- coding: utf-8 -*-

import re

class ArticleProcessor():

    @staticmethod
    def process_authors(value):
        strings_to_clean = ('O Estado de S.Paulo', 'O Estado de S. Paulo',
        u'estadão.com.br', 'por ', 'Por ', 'RIO', '\n', '\t', '\"', '*',
        ' - ', '/', ',')
        # TODO: Tratar essa página
        # http://politica.estadao.com.br/noticias/panama-papers,panama-papers-revelam-107-offshores-ligadas-a-personagens-da-lava-jato,10000024501
        for string in strings_to_clean:
            value = value.replace(string, '')

        return [a.strip()
                for a in re.split(', | e ', value)]

    @staticmethod
    def process_keywords(value):
        return value.strip().replace(' -', '').replace(',', '').lower()
