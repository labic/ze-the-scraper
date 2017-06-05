# -*- coding: utf-8 -*-

import dateparser
import logging; logger = logging.getLogger(__name__)


class CleanString(object):
    
    def __call__(self, value, loader_context):
        return value.strip('\t\n')


class ParseDate(object):
    
    def __call__(self, value, loader_context):
        value = value.replace('Atualizado:', '') \
                     .replace(' | ', ' ') \
                     .replace('h', ':') \
                     .replace('h ', ':') \
                     .replace(', ', ' ') \
                     .replace('-03', '') \
                     .replace('  ', ' ') \
                     .strip()
        
        try:
            return dateparser.parse(value, settings={'TIMEZONE': '+0300'})
        except Exception as e:
            logger.warning('Date not processed: %s' % value)
            return None
        
        return value
