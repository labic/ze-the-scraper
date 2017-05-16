# -*- coding: utf-8 -*-
import logging; logger = logging.getLogger(__name__)
from scrapy.exceptions import NotConfigured
from ze.exceptions import EmptyFields


class BasePipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings, stats=crawler.stats)
        
    def __init__(self, settings, stats): raise NotImplementError


class DropItemsPipeline(BasePipeline):
    
    def __init__(self, settings, stats):
        self.stats = stats
        self.settings = {
            'enabled': settings.getbool('DROP_ITEM_PIPELINE_ENABLED'), 
            'filters': settings.get('DROP_ITEM_PIPELINE_FILTERS')
        }
        if not self.settings['enabled']:
            raise NotConfigured('Drop Item Pepeline is not enabled, check settings values')
    
    def process_item(self, item, spider):
        empty_fields = { k: not item.get(k, False) for k in item.fields.keys() \
                        if item.fields[k].get('required', False)}
        
        if any(empty_fields.values()): 
            fields_name = [k for k in empty_fields.keys() if empty_fields[k]]
            for field_name in fields_name:
                self.stats.inc_value('item_dropped_reasons_count/EmptyFields/%s/%s' % \
                                    (spider.name, field_name))
            raise EmptyFields('Item with empty fields "%s" in url: %s' % (fields_name, item['url']))
        else:
            return item