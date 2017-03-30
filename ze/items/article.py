# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from ze.processors.article import ArticleProcessor
from ze.processors.common import CommonProcessor

class ArticleItem(scrapy.Item):
    name = scrapy.Field(
        output_processor=TakeFirst(),
    )
    date_published = scrapy.Field(
        input_processor=MapCompose(
            CommonProcessor.process_date_time
        ),
        output_processor=TakeFirst(),
    )
    date_modified = scrapy.Field(
        input_processor=MapCompose(
            CommonProcessor.process_date_time
        ),
        output_processor=TakeFirst(),
    )
    description = scrapy.Field(
        output_processor=TakeFirst(),
    )
    authors = scrapy.Field(
        input_processor=MapCompose(
            ArticleProcessor.process_authors
        )
    )
    text = scrapy.Field(
        input_processor=MapCompose(
            ArticleProcessor.process_text
        ),
        output_processor=TakeFirst(),
    )
    images = scrapy.Field()
    keywords = scrapy.Field(
        input_processor=MapCompose(
            ArticleProcessor.process_keywords
        )
    )
    thumbnail_url = scrapy.Field(
        output_processor=TakeFirst(),
    )
    comment_count = scrapy.Field(
        output_processor=TakeFirst(),
    )
    url = scrapy.Field(
        output_processor=TakeFirst(),
    )
    sources_types = scrapy.Field()


class ArticleItemLoader(ItemLoader):
    def get_collected_values(self, field_name):
        return (self._values[field_name]
                if field_name in self._values
                else self._values.default_factory())

    def add_fallback_css(self, field_name, css, *processors, **kw):
        if not any(self.get_collected_values(field_name)):
            self.add_css(field_name, css, *processors, **kw)

    def add_fallback_xpath(self, field_name, css, *processors, **kw):
        if not any(self.get_collected_values(field_name)):
            self.add_xpath(field_name, css, *processors, **kw)
