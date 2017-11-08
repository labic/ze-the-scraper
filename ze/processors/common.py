# -*- coding: utf-8 -*-
from urllib.parse import urlparse

import logging; logger = logging.getLogger(__name__)

from datetime import datetime
import dateparser

__all__ = ('CleanString', 'FormatString', 'ValidURL', 'ParseDate')


class CleanString(object):

    def __call__(self, value, loader_context):
        return value.strip().strip('\t\n')


class FormatString(object):

    def __call__(self, values, loader_context):
        format_string = loader_context.get('format', '{}')
        for value in values:
            yield format_string.format(value)


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
        print('SPIDER: ', spider_name)

        if spider_name == 'r7':
            if '(' in value:
                value=value.split('(')[1].split(')')[0]

        if spider_name == 'correiobraziliense':
            return dateparser.parse(value, settings={'TIMEZONE': '+0300','DATE_ORDER': 'DMY'})

        if spider_name == 'bbc':
            return datetime.fromtimestamp(int(value))

        if spider_name == 'mundoeducacao':
            if 'em' in value:
                value = value.split('em')[1]
                value = value.replace(' em','').replace('às','')

            return dateparser.parse(value, settings={'TIMEZONE': '+0300','DATE_ORDER': 'DMY'})

        # if spider_name == 'band':
        #     # if 'em' in value:
        #     #     value = value.split('em')[1]
        #     #     value = value.replace(' em','').replace('às','')

        #     return dateparser.parse(value, settings={'TIMEZONE': '+0300','DATE_ORDER': 'DMY'})


        if (self.field == 'datePublished'):
            if spider_name == 'zh':
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
                return dateparser.parse(value, settings={'TIMEZONE': '+0300'})

            if spider_name =='brasilescola':
                value=value.split(',')[0].replace(' - ',' ')\
                                            .replace('h', ':') \
                                            .replace('min', '')\
                                            .replace('Publicado','')\
                                            .replace('Atualizado','')
                return dateparser.parse(value, settings={'TIMEZONE': '+0300'})
            if spider_name =='ig':
                if '|' in value:
                    value=value.split('|')[1].replace(' - ',' ')\
                                            .replace('h', ':') \
                                            .replace('min', '')\
                                            .replace('Publicado','')\
                                            .replace('Atualizado','')
                return dateparser.parse(value, settings={'TIMEZONE': '+0300'})

            if spider_name=='jconline':
                value=value.split('Atualizado')[0].replace(' - ',' ')\
                                                .replace('h', ':') \
                                                .replace('min', '')\
                                                .replace('Publicado','')\
                                                .replace('Atualizado','')\
                                                .replace('em','')\
                                                .strip(',')\
                                                .replace('às','')\
                                                .replace('T0', ' ')\
                                                .replace('Z', ' ')
                return dateparser.parse(value, settings={'TIMEZONE': '+0300'})

            if spider_name =='atarde':
                value=value.split('|')[0].replace(' - ',' ')\
                                            .replace('h', ':') \
                                            .replace('min', '')
                return dateparser.parse(value, settings={'TIMEZONE': '+0300'})

            if spider_name == 'veja':
                value = value.split(' - ')[1].replace('Publicado','')\
                                            .replace('h', ':') \
                                            .replace('min', '')\
                                            .replace('em','')\
                                            .replace(',','')
                return dateparser.parse(value, settings={'TIMEZONE': '+0300'})
            if spider_name == 'terra':
                value = value.replace('|','').split('atualizado')[0].replace('Publicado','')\
                                            .replace('h', ':') \
                                            .replace('min', '')\
                                            .replace('em','')\
                                            .replace(',','')
                return dateparser.parse(value, settings={'TIMEZONE': '+0300'})

            if spider_name=='estadao':
                value1 = value.split('|')[1]
                value1 = value1.replace('h',':')
                value = value.split('|')[0]+value1
                return dateparser.parse(value, settings={'TIMEZONE': '+0300'})

            if spider_name=='tvcultura':
                if '|' in value:
                    value = value.split('|')[2]
                else:
                    value=value.replace('<small>','').replace('</small>','').replace('<time>','').replace('</time>','')
                return dateparser.parse(value, settings={'TIMEZONE': '+0300'})

            if spider_name == 'epoca':
                value = value.split(' - Atualizado')[0].replace('h',':')
                return dateparser.parse(value, settings={'TIMEZONE': '+0300'})

            # if spider_name == 'globo':
                # return dateparser.parse(value, settings={'TIMEZONE': '+0300','DATE_ORDER': 'DMY'})



            if spider_name =='exame':
                return dateparser.parse(value)
            if spider_name =='sbt':
                return dateparser.parse(value)
            if spider_name =='sejabixo':
                return dateparser.parse(value.split('em')[1])
            if spider_name =='senado':
                value = value.split(' - ')[0]
                return dateparser.parse(value, settings={'TIMEZONE': '+0300'})



                #GOVERNAMENTAL - ESTADOS
            if spider_name == 'govac':
                if 'Criado' in value:
                    value=value.split(',')[1]
                else:
                    value=value.split(',')[0]
                return dateparser.parse(value, settings={'TIMEZONE': '+0300','DATE_ORDER': 'DMY'})

            if spider_name == 'govce':
                if 'em' in value:
                    value=value.split('em')[1]
                value=value.split(',')[0]
                return dateparser.parse(value, settings={'TIMEZONE': '+0300','DATE_ORDER': 'DMY'})

            if spider_name == 'govgo':
                if '-' in value:
                    value=value.split('publicação:')[1].replace('-','')
                return dateparser.parse(value, settings={'TIMEZONE': '+0300','DATE_ORDER': 'DMY'})

            if spider_name == 'govpa':
                # value=value.split('publicação:')[1].replace('-','')
                return dateparser.parse(value, settings={'TIMEZONE': '+0300','DATE_ORDER': 'DMY'})


            if spider_name == 'govpb':
                value=value.split('Fotos')[0].replace(' - ',' ')
                return dateparser.parse(value, settings={'TIMEZONE': '+0300','DATE_ORDER': 'DMY'})

            if spider_name == 'govrj':
                value=value.split('Atualizado em')[0].replace(' - ',' ')
                return dateparser.parse(value, settings={'TIMEZONE': '+0300','DATE_ORDER': 'DMY'})

            if spider_name == 'govto':
                value=value.split('-')[0]
                return dateparser.parse(value, settings={'TIMEZONE': '+0300','DATE_ORDER': 'DMY'})


        if (self.field == 'dateModified'):
            if spider_name == 'zh':
                value=value.split('|')[1].replace(' - ',' ')\
                                            .replace('h', ':') \
                                            .replace('min', '')\
                                            .replace('Atualizada','')\
                                            .replace('em','')
                return dateparser.parse(value, settings={'TIMEZONE': '+0300','DATE_ORDER': 'DMY'})

            # if spider_name == 'globo':
            #     value=value.split('|')[1].replace(' - ',' ')\
            #                                 .replace('h', ':') \
            #                                 .replace('min', '')\
            #                                 .replace('Atualizada','')\
            #                                 .replace('em','')
            #     return dateparser.parse(value, settings={'TIMEZONE': '+0300','DATE_ORDER': 'DMY'})


            if spider_name == 'diariodepernambuco':
                return dateparser.parse(value)

            if spider_name =='correiopopular':
                value=value.split('Atualizado')[0].replace(' - ',' ')\
                                            .replace('h', ':') \
                                            .replace('min', '')\
                                            .replace('Publicado','')\
                                            .replace('Atualizado','')
                return dateparser.parse(value, settings={'TIMEZONE': '+0300'})

            if spider_name == 'terra':
                value = value.split('|')[0]+value.split('|')[2]
                value=value.replace('atualizado','')\
                                            .replace('h', ':') \
                                            .replace('min', '')\
                                            .replace('em','')\
                                            .replace(',','')\
                                            .replace('às','')
                return dateparser.parse(value, settings={'TIMEZONE': '+0300'})

            if spider_name =='senado':
                value = value.split(' - ')[1].replace('ATUALIZADO EM','')
                return dateparser.parse(value, settings={'TIMEZONE': '+0300'})

            # if spider_name=='govce':
            #     value=value.split('em')[1]
            #     return dateparser.parse(value, settings={'TIMEZONE': '+0300'})

            if spider_name == 'govrj':
                if 'Atualizado em' in value:
                    value=value.split('Atualizado em')[1].replace(' - ',' ')
                return dateparser.parse(value, settings={'TIMEZONE': '+0300','DATE_ORDER': 'DMY'})


        value = value.replace('Atualizado:', '') \
                     .replace('Atualizado', '') \
                     .replace(' | ', ' ') \
                     .replace('h', ':') \
                     .replace('h ', ':') \
                     .replace(', ', ' ') \
                     .replace('  ', ' ') \
                     .strip()

        try:
            return dateparser.parse(value, settings={'TIMEZONE': '+0300'})
        except Exception as e:
            logger.warning('Date not processed: %s' % value)
            return None

        return value
