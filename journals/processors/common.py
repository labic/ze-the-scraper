# -*- coding: utf-8 -*-

import re
from datetime import datetime
import logging as log

class CommonProcessor():

    @staticmethod
    def process_date_time(value):

        value = value.replace('Atualizado:', '').strip()

        formats = (
            '%d %B %Y | %Hh %M',
            '%d %B %Y | %H:%M',
            '%d de %B de %Y %Hh%M',
            '%d/%m/%Y, %Hh%M',
        )

        for f in formats:
            try:
                return datetime.strptime(value, f).isoformat()
            except Exception as e:
                log.info(e)
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
