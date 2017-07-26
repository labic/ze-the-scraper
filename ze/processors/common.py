# -*- coding: utf-8 -*-

import dateparser
import logging; logger = logging.getLogger(__name__)


class CleanString(object):

    def __call__(self, value, loader_context):
        return value.strip('\t\n')


class ParseDate(object):
    
    def __init__(self, field):
        self.field = field

    def __call__(self, value, loader_context):
        spider_name = loader_context.get('spider_name')

        if spider_name == 'r7':
            value = value.split('(')[1].split(')')[0]
        
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
