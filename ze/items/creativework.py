# -*- coding: utf-8 -*-

from scrapy import Field
from ze.items import CreativeWorkItem
from scrapy.loader.processors import TakeFirst, MapCompose
from ze.processors.article import ArticleProcessor
from ze.processors.common import CommonProcessor
from ze.processors.html import CleanHTML

class ArticleItem(CreativeWorkItem):

    articleBody = Field(
        input_processor=MapCompose(
            CleanHTML(),
        ),
        output_processor=TakeFirst(),
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
