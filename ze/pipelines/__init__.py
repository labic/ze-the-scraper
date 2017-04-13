# -*- coding: utf-8 -*-

import os
import logging
import json
from pymongo import MongoClient
from google.cloud import pubsub
import scrapy

logger = logging.getLogger(__name__)

class MongoPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings = crawler.settings)


    def __init__(self, settings):
        self.mongo_uri = settings.get('MONGO_URI'),
        self.mongo_db = settings.get('MONGO_DATABASE', 'ze-the-scraper')
        self.client = None


    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        # TODO: Get collection name via item name
        self.db['NewsArticle'].insert(dict(item))
        return item


class GooglePubSubPipeline(object):
    topic = None
    credentials_json_file = '../service-account.json'


    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings)
 

    def __init__(self, settings):
        self.google_cloud_enabled = settings.getbool('GOOGLE_CLOUD_ENABLED')

        if self.google_cloud_enabled:
            self.pubsub = pubsub.Client()
            logger.info('Google Cloud Pub/Sub client initiated with success')
        else:
            logger.error('Google Cloud is not enabled, check Google Cloud extension configuration')


    def open_spider(self, spider):
        if self.google_cloud_enabled:
            try:
                # TODO: Create topic for using spider and item nam
                self.topic = self.pubsub.topic('ze-the-scraper.'+spider.name+'.newsarticle')
                if not self.topic.exists():
                    self.topic.create()
            except Exception as e:
                logger.error('Failed to get or create topic in Google Cloud Pub/Sub: %s' % e)

    def process_item(self, item, spider):
        if self.google_cloud_enabled:
            try:
                self.topic.publish(json.dumps(dict(item)))
            except Exception as e:
                logger.error('Failed publish item to Google Cloud Pub/Sub: %s' % e)
            
        return item