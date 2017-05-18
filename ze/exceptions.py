# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem

class EmptyFields(DropItem):
    """Drop item from the item pipeline with empty fields"""
    pass

class MissingSearchQueryKeywords(DropItem):
    """Drop item from the item don't have the none of keywords in the fields"""
    pass