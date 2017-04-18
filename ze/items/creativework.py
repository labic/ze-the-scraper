# -*- coding: utf-8 -*-

from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose
from ze.processors.article import ArticleProcessor
from ze.processors.common import CommonProcessor
from ze.processors.html import CleanHTML

class ArticleItem(Item):
    name = Field(
        output_processor=TakeFirst(),
    )
    datePublished = Field(
        input_processor=MapCompose(
            CommonProcessor.process_date_time
        ),
        output_processor=TakeFirst(),
    )
    dateModified = Field(
        input_processor=MapCompose(
            CommonProcessor.process_date_time
        ),
        output_processor=TakeFirst(),
    )
    description = Field(
        output_processor=TakeFirst(),
    )
    author = Field(
        input_processor=MapCompose(
            ArticleProcessor.process_authors
        )
    )
    articleBody = Field(
        input_processor=MapCompose(
            CleanHTML(),
        ),
        output_processor=TakeFirst(),
    )
    image = Field()
    keywords = Field(
        input_processor=MapCompose(
            ArticleProcessor.process_keywords
        )
    )
    commentCount = Field(
        output_processor=TakeFirst(),
    )
    url = Field(
        output_processor=TakeFirst(),
    )
    sources_types = Field()


class NewsArticleItem(ArticleItem): pass
    
    