# -*- coding: utf-8 -*-
import re
import logging; logger = logging.getLogger(__name__)
from scrapy.exceptions import NotConfigured
from ze.exceptions import EmptyFields, MissingSearchQueryKeywords


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
        # FIXME when use spider all, get the real name of the spiders that load item
        empty_fields = { k: not item.get(k, False) for k in item.fields.keys() \
                        if item.fields[k].get('required', False)}
        
        if any(empty_fields.values()): 
            fields_name = [k for k in empty_fields.keys() if empty_fields[k]]
            for field_name in fields_name:
                self.stats.inc_value('item_dropped_reasons_count/EmptyFields/%s/%s' % \
                                    (spider.name, field_name))
            raise EmptyFields('Item with empty fields "%s" in url: %s' % (fields_name, item['url']))
        
        if hasattr(spider, 'search'):
            if spider.search.get('regex'):
                if not re.search(spider.search['regex'], item.get('articleBody', '')) \
                and not re.search(spider.search['regex'], item.get('name', '')):
                    raise MissingSearchQueryKeywords('Item of url %s don\'t have search query keyword %s' % \
                                                    (item['url'], spider.search['query']))
        
        return item