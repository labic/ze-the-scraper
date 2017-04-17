# -*- coding: utf-8 -*-

import os
import json
from google.cloud import pubsub
from pymongo import MongoClient
import scrapy
from scrapy.selector import Selector
import logging
logger = logging.getLogger(__name__)


class BasePipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings = crawler.settings)


class MongoPipeline(BasePipeline):

    def __init__(self, settings):
        self.mongo_uri = settings.get('MONGO_URI'),
        self.mongo_db = settings.get('MONGO_DATABASE', 'ze-the-scraper')
        self.client = None
        
        self.stats = stats
        self.stats.set_value('items/mongodb/insert_count', 0)
        self.stats.set_value('items/mongodb/insert_erros_count', 0)


    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.stats.set_value('items/mongodb/database_name', self.db.name)


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # TODO: Get collection name via item name
        try:
            self.db['NewsArticle'].insert(dict(item))
            self.stats.inc_value('items/mongodb/insert_count')
        except Exception as e:
            self.stats.inc_value('items/mongodb/insert_erros_count')
            pass
        
        return item


class GooglePubSubPipeline(object):

    def __init__(self, settings, stats):
        self.google_cloud_enabled = settings.getbool('GOOGLE_CLOUD_ENABLED')
        self.settings = {
            'project_name': settings.get('PROJECT_NAME')
        }
        self.topics = {}
        self.stats = stats
        self.stats.set_value('google/pubsub/published_count', 0)
        self.stats.set_value('google/pubsub/erros_count', 0)

        if self.google_cloud_enabled:
            self.client = pubsub.Client()
            logger.info('Google Cloud Pub/Sub client initiated with success')
        else:
            logger.warning('Google Cloud is not enabled, check Google Cloud extension configuration')


    def open_spider(self, spider):
        if self.google_cloud_enabled:
            try:
                # TODO: Use multiples topics {} and create topic for using spider and item nam
                self.topic = self.client.topic('ze-the-scraper.'+spider.name+'.newsarticle')
                if not self.topic.exists():
                    self.topic.create()
            except Exception as e:
                logger.error('Failed to get or create topic in Google Cloud Pub/Sub: %s' % e)


    def process_item(self, item, spider):
        if self.google_cloud_enabled:
            try:
                topic_name = '%s.%s.%s' % (self.settings['project_name'], spider.name, 'newsarticle')
                topic = None
                
                if topic_name in self.topics:
                    topic = self.topics[topic_name] 
                else:
                    self.topics[topic_name] = self.client.topic(topic_name)
                    
                    if not self.topics[topic_name].exists():
                        self.topics[topic_name].create()
                    
                    topic = self.topics[topic_name]
                
                topic.publish(json.dumps(dict(item)))
                
                self.stats.inc_value('google/pubsub/published_count')
            except Exception as e:
                logger.error('Failed publish item to Google Cloud Pub/Sub: %s' % e)
                self.stats.inc_value('google/pubsub/erros_count')
        return item
