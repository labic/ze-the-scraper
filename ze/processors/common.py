# -*- coding: utf-8 -*-

import dateparser
import logging
logger = logging.getLogger(__name__)
    
class ParseDate(object):
    
    def __call__(self, value, loader_context):
        value = value.strip() \
                    .replace('Atualizado:', '') \
                    .replace(' | ', ' ') \
                    .replace('h', ':') \
                    .replace('h ', ':') \
                    .replace(', ', '') \
                    .replace('  ', ' ')
        
        try:
            return dateparser.parse(value, settings={'TIMEZONE': '+0300'})
                        # date_formats=['%d %B %Y %H:%M'], 
                        # languages=['pt']) \
                        # .strftime('%Y-%m-%d %H:%M')
        except Exception as e:
            logger.warning('Date not processed: %s' % value)
            return None
        
        return value