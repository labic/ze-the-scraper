# -*- coding: utf-8 -*-

import dateparser
import logging
logger = logging.getLogger(__name__)

class CommonProcessor():

    @staticmethod
    def process_date_time(value):

        value = value.replace('Atualizado:', '') \
                    .replace(' | ', ' ') \
                    .replace('h', ':') \
                    .replace('h ', ':') \
                    .replace(', ', '') \
                    .replace('  ', ' ') \
                    .strip()
        date_formats = (
            '%d %B %Y %H:%M',
            '%d de %B de %Y %Hh%M',
            '%d/%m/%Y %H:%M',
        )
        
        try:
            return dateparser.parse(value, 
                        date_formats=['%d %B %Y %H:%M'], 
                        languages=['pt']) \
                        .isoformat()
        except Exception as e:
            logger.warning('Date %s not processed with none of formats: %s' % (value, ', '.join(date_formats)))
            pass

        return value

    # @staticmethod
    # def process_clean(value):
    #     values_to_clean = {
    #         ,
    #         ',': '',
    #         ' - ': '',
    #         'por ': '',
    #     }
