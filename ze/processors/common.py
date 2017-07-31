# -*- coding: utf-8 -*-

from urllib.parse import urlparse
import logging; logger = logging.getLogger(__name__)

import dateparser

tabela_meses = {'janeiro':1,
                'fevereiro':2,
                'março':3,
                'abril':4,
                'maio':5,
                'junho':6,
                'julho':7,
                'agosto':8,
                'setembro':9,
                'outubro':10,
                'novembro':11,
                'dezembro':12}

class CleanString(object):

    def __call__(self, value, loader_context):
        return value.strip('\t\n')

class ValidURL(object):
    
    def __call__(self, value, loader_context):
        try:
            result = urlparse(value)
            if all((result.scheme, result.netloc, result.path)):
                return value
            else:
                return None
        except:
            return None

class ParseDate(object):

    def __init__(self, field):
        self.field = field

    def __call__(self, value, loader_context):
        spider_name = loader_context.get('spider_name')

        print('------------------------------------------------------------------------------------\n'+str(value)+'\n--------------------------------------------------------------------')

        if spider_name == 'r7':
            value=value.split('(')[1].split(')')[0]

        if spider_name == 'correiobraziliense':
            return dateparser.parse(value, settings={'TIMEZONE': '+0300','DATE_ORDER': 'DMY'})

        if spider_name == 'zh':
             #CASO SEJA DATEPUBLISHED
            value=value.split('|')[0].replace(' - ',' ')\
                                        .replace('h', ':') \
                                        .replace('min', '')
            return dateparser.parse(value, settings={'TIMEZONE': '+0300','DATE_ORDER': 'DMY'})

        if spider_name == 'diariodepernambuco':
            return dateparser.parse(value)

        if spider_name =='correiopopular':
            value=value.split('Atualizado')[0].replace(' - ',' ')\
                                        .replace('h', ':') \
                                        .replace('min', '')\
                                        .replace('Publicado','')\
                                        .replace('Atualizado','')
            print('value'+value)
            return dateparser.parse(value, settings={'TIMEZONE': '+0300'})
        if spider_name=='jconline':
            value=value.split('Atualizado')[0].replace(' - ',' ')\
                                        .replace('h', ':') \
                                        .replace('min', '')\
                                        .replace('Publicado','')\
                                        .replace('Atualizado','')\
                                        .replace('em','')\
                                        .strip(',')\
                                        .replace('às','')
            print('value'+value)
            return dateparser.parse(value, settings={'TIMEZONE': '+0300'})


        # if spider_name =='gestaoescolar':
        #     # value = value.strip(' de ')split('')
        #     return(dateparser.parse(value, settings={'TIMEZONE': '+0300'}))


        # value = value.replace('Atualizado:', '') \
        #              .replace('Atualizado', '') \
        #              .replace(' | ', ' ') \
        #              .replace('h', ':') \
        #              .replace('h ', ':') \
        #              .replace(', ', ' ') \
        #              .replace('  ', ' ') \
        #              .strip()

        try:
            print(dateparser.parse(value, settings={'TIMEZONE': '+0300'}))
            return dateparser.parse(value, settings={'TIMEZONE': '+0300'})
        except Exception as e:
            logger.warning('Date not processed: %s' % value)
            return None

        return value
