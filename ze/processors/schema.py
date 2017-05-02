# -*- coding: utf-8 -*-

class AuthorProcessor():

    def __call__(self, values, context={}):
        return [{ 'type': None, 'name': v } for v in values]