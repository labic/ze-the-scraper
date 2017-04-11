# -*- coding: utf-8 -*-

import os
import json
import pymongo
from google.cloud import pubsub

class MongoPipeline(object):
    # TODO: Get collection name of MongoDB via spider.name or use item name
    collection_name = 'ze'

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )


    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db


    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item


class GooglePubSubPipeline(object):
    topic = None
    credentials_json_file = '../service-account.json'


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            credentials_json=crawler.settings.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        )


    def __init__(self, credentials_json):
        with open(self.credentials_json_file, 'w') as outfile:
            outfile.write(credentials_json)
        
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_json_file
        self.pubsub = pubsub.Client()


    def open_spider(self, spider):
        self.topic = self.pubsub.topic('ze-the-scraper.'+spider.name+'.newsarticle')
        if not self.topic.exists():
            self.topic.create()


    def close_spider(self, spider):
        os.remove(self.credentials_json_file)


    def process_item(self, item, spider):
        self.topic.publish(json.dumps(dict(item)))
        return item

