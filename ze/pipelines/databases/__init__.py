# -*- coding: utf-8 -*-
import logging; logger = logging.getLogger(__name__)

from pymongo import MongoClient, ASCENDING, DESCENDING

from scrapy.exceptions import NotConfigured

from ...pipelines import BasePipeline


class MongoPipeline(BasePipeline):

    def __init__(self, settings, stats):
        self.settings = {
            'enabled': settings.getbool('MONGO_ENABLED'), 
            'merge_duplicates': settings.getbool('MERGE_DUPLICATES', False), 
        }
        
        if self.settings['enabled']:
            self.mongo_uri = settings.get('MONGO_URI'),
            self.client = None
            
            self.stats = stats
            self.stats.set_value('items/mongodb/insert_count', 0)
            self.stats.set_value('items/mongodb/insert_erros_count', 0)
        else:
            raise NotConfigured('MongoDB is not enabled, check settings values')

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client.get_default_database()
        self.stats.set_value('items/mongodb/database_name', self.db.name)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        try:
            item_name = item.__class__.__name__
            collection = self.db[item_name]
            
            if self.settings['merge_duplicates']:
                # TODO: Remove/Refactor
                if item_name == 'Article':
                    item_finded = False
                    for doc in collection.find({'url': item['url']})\
                                         .sort([('dateCreated', ASCENDING)]):
                        item_finded = True
                        for key in item.keys():
                            if not key in doc:
                                doc[key] = item[key]
                        doc['keywords'] = list(set(item.get('keywords', ())) | set(doc.get('keywords', ())))
                        
                        collection.save(doc)
                        self.stats.inc_value('items/mongodb/merged_count')
                    
                    if not item_finded:
                        collection.insert(dict(item))
            else:
                collection.insert(dict(item))
                self.stats.inc_value('items/mongodb/insert_count')
        except Exception as e:
            logger.error('Failed insert item to MongoDB: %s', e)
            self.stats.inc_value('items/mongodb/insert_erros_count')
            pass
        
        return item
