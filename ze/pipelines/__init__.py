# -*- coding: utf-8 -*-
import re
from functools import reduce
from collections import ChainMap
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
        if settings.getbool('DROP_ITEM_PIPELINE_ENABLED'):
            self.stats = stats
            self.validation_methods = settings.get('DROP_ITEM_PIPELINE_VALIDATION_METHODS')
        else:
            raise NotConfigured('Drop Item Pepeline is not enabled, check settings values')
    
    def process_item(self, item, spider):
        for validation_method in self.validation_methods:
            self[validation_method](item, spider)
        
        return item
    
    def drop_items_with_empty_fields(self, item, spider):
        # FIXME when use spider all, get the real name of the spiders that load item
        empty_fields = { k: not item.get(k, False) for k in item.fields.keys() \
                        if item.fields[k].get('required', False)}
        
        if any(empty_fields.values()): 
            fields_name = [k for k in empty_fields.keys() if empty_fields[k]]
            for field_name in fields_name:
                self.stats.inc_value('item_dropped_reasons_count/EmptyFields/%s/%s' % \
                                    (spider.name, field_name))
            raise EmptyFields('Item with empty fields "%s" in url: %s' % (fields_name, item['url']))
    
    def drop_items_that_not_match_regex(self, item, spider):
        # TODO add Validatable attr to item fields 
        if hasattr(spider, 'regex'):
            if not re.search(spider.regex, item.get('articleBody', '')) \
            and not re.search(spider.regex, item.get('name', '')):
                raise MissingSearchQueryKeywords('Item of url %s don\'t have search query keyword %s' % \
                                                (item['url'], spider.search['query']))


class ItemsSideValues(object):
    
    def process_item(self, item, spider):    
        # FIXME find a better place and how to add the tags of search to keywords
        if hasattr(spider, 'tags'):
            # URGENT change jobs script 
            repls = ('[',''), (']',''),('"','')
            tags = reduce(lambda a, kv: a.replace(*kv), repls, spider.tags)
            keywords = [t.strip().lower() for t in tags.split(',')]
            
            if 'keywords' not in item:
                item['keywords'] = keywords
            else: 
                item['keywords'] = list(set(item['keywords'] + keywords))
        
        return item