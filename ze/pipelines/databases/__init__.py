# -*- coding: utf-8 -*-

import logging; logger = logging.getLogger(__name__)
from pymongo import MongoClient

class BasePipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings, stats=crawler.stats)
        
    def __init__(self, settings, stats): raise NotImplementError


class MongoPipeline(BasePipeline):

    def __init__(self, settings, stats):
        self.settings = {
            'enabled': settings.getbool('MONGO_ENABLED'), 
        }
        
        if self.settings['enabled']:
            self.mongo_uri = settings.get('MONGO_URI'),
            self.mongo_db = settings.get('MONGO_DATABASE', 'ze-the-scraper')
            self.client = None
            
            self.stats = stats
            self.stats.set_value('items/mongodb/insert_count', 0)
            self.stats.set_value('items/mongodb/insert_erros_count', 0)
        else:
            logger.warning('MongoDB is not enabled, check MongoDB on settings')
        

    def open_spider(self, spider):
        if self.settings['enabled']:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]
            self.stats.set_value('items/mongodb/database_name', self.db.name)

    def close_spider(self, spider):
        if self.settings['enabled']:
            self.client.close()

    def process_item(self, item, spider):
        if self.settings['enabled']:
            try:
                self.db[item.__class__.__name__].insert(dict(item))
                self.stats.inc_value('items/mongodb/insert_count')
            except Exception as e:
                logger.error('Failed insert item to MongoDB: %s', e)
                self.stats.inc_value('items/mongodb/insert_erros_count')
                pass
        
        return item
