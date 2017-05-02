# -*- coding: utf-8 -*-

class AuthorProcessor():

    def __call__(self, values, context={}):
        return_values = []
        for v in values:
            return_values.append({
                'type': 'Person',
                'name': v
            })
        
        return return_values