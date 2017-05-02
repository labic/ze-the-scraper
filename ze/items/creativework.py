# -*- coding: utf-8 -*-

from scrapy import Field
from scrapy.loader.processors import TakeFirst, MapCompose
from ze.processors.article import ArticleProcessor
from ze.processors.common import CommonProcessor
from ze.processors.html import CleanHTML
from ze.items import CreativeWorkItem


class ArticleItem(CreativeWorkItem):

    articleBody = Field(
        serializer=dict, 
        input_processor=MapCompose(CleanHTML(),),
        output_processor=TakeFirst(), 
        schemas={
            'avro': {
                'field_type': 'STRING', 
            }, 
        }
    )
    articleSection = Field()
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
