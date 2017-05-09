# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem


class BasePipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings, stats=crawler.stats)
        
    def __init__(self, settings, stats): raise NotImplementError


class DropItemsPipeline(object):
    
    def process_item(self, item, spider):
        empty_fields = { k: not item.get(k, False) for k in item.fields.keys() \
                        if item.fields[k].get('required', False)}
        
        if any(empty_fields): 
            raise DropItem('Item with some empty fields "%s" in url: %s' \
                            % (empty_fields, item['url']))
        else:
            return item