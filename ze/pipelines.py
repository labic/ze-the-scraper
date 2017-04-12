# -*- coding: utf-8 -*-

import os
import logging
import json
from pymongo import MongoClient
from google.cloud import pubsub


class MongoPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings = crawler.settings)


    def __init__(self, settings):
        self.mongo_uri = settings.get('MONGO_URI'),
        self.mongo_db = settings.get('MONGO_DATABASE', 'ze-the-scraper')


    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        # TODO: Get collection name via spider.name or use item name
        self.db['NewsArticle'].insert(dict(item))
        return item


class GooglePubSubPipeline(object):
    log = logging.getLogger('ze.pipelines.GooglePubSubPipeline')
    topic = None
    credentials_json_file = '../service-account.json'


    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings)
 

    def __init__(self, settings):
        self.credentials_exist = settings.getbool('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        
        if self.credentials_exist:
            with open(self.credentials_json_file, 'w') as outfile:
                outfile.write(settings.get('GOOGLE_APPLICATION_CREDENTIALS_JSON'))
            
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_json_file
            self.pubsub = pubsub.Client()
        else:
            self.log.error('GOOGLE_APPLICATION_CREDENTIALS_JSON not set in  settings')


    def open_spider(self, spider):
        if self.credentials_exist:
            self.topic = self.pubsub.topic('ze-the-scraper.'+spider.name+'.newsarticle')
            if not self.topic.exists():
                self.topic.create()


    def close_spider(self, spider):
        if self.credentials_exist:
            os.remove(self.credentials_json_file)


    def process_item(self, item, spider):
        if self.credentials_exist:
            self.topic.publish(json.dumps(dict(item)))
        return item
