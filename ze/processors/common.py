
            value = value.split('(')[1].split(')')[0]
        
        value = value.replace('Atualizado:', '') \
                     .replace('Atualizado', '') \
                     .replace(' | ', ' ') \
                     .replace('h', ':') \
                     .replace('h ', ':') \
                     .replace(', ', ' ') \
                     .replace('  ', ' ') \
                     .strip()
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
