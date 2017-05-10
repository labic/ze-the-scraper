# -*- coding: utf-8 -*-

import six
from scrapy import Field
from scrapy.loader.processors import TakeFirst, MapCompose
from ..processors.html import ImproveHTML
from ..items import CreativeWorkItem


class ArticleItem(CreativeWorkItem):
    
    def __init__(self, *args, **kwargs):
        self._values = {}
        # TODO: Refactor this!
        self.__class__.__name__ = 'Article'
        if args or kwargs:  # avoid creating dict for most common case
            for k, v in six.iteritems(dict(*args, **kwargs)):
                self[k] = v

    articleBody = Field(
        default=None, 
        required=True,
        input_processor=MapCompose(ImproveHTML(),),
        output_processor=TakeFirst(), 
        indexed=False, 
        schemas={
            'avro': {
                'field_type': 'STRING', 
            }, 
        }
    )
    articleSection = Field()
    headline = Field(
        CreativeWorkItem.fields['headline'],
        # TODO: Change to True, this involve change item fields on spiders
        required=False,
    )
    name = Field(
        CreativeWorkItem.fields['name'],
        # TODO: Change to False, this involve change item fields on spiders
        required=True,
    )
    pageEnd = Field()
    pageStart = Field()
    pagination = Field()
    wordCount = Field()


class NewsArticleItem(ArticleItem):

    dateline = Field()
    printColumn = Field()
    printEdition = Field()
    printPage = Field()
    printSection = Field()
