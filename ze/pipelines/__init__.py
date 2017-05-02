# -*- coding: utf-8 -*-

import os
import json
import logging; logger = logging.getLogger(__name__)
from collections import namedtuple
from google.cloud import bigquery
from google.cloud.bigquery.schema import SchemaField
from google.cloud import pubsub
from google.cloud.exceptions import BadRequest
from pymongo import MongoClient

class BasePipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings, stats=crawler.stats)
        
    def __init__(self, settings, stats): raise NotImplementError


class MongoPipeline(BasePipeline):

    def __init__(self, settings, stats):
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
        try:
            self.db[item.__class__.__name__].insert(dict(item))
            self.stats.inc_value('items/mongodb/insert_count')
        except Exception as e:
            logger.error('Failed insert item to MongoDB: %s', e)
            self.stats.inc_value('items/mongodb/insert_erros_count')
            pass
        
        return item


class GooglePubSubPipeline(BasePipeline):

    def __init__(self, settings, stats):
        self.google_cloud_enabled = settings.getbool('GOOGLE_CLOUD_ENABLED')
        self.topics = {}
        
        self.stats = stats
        self.stats.set_value('google/pubsub/published_count', 0)
        self.stats.set_value('google/pubsub/erros_count', 0)

        if self.google_cloud_enabled:
            self.client = pubsub.Client()
            logger.info('Google Cloud Pub/Sub client initiated with success')
        else:
            logger.warning('Google Cloud is not enabled, check Google Cloud extension configuration')

    def process_item(self, item, spider):
        if self.google_cloud_enabled:
            try:
                topic_name = 'ze-the-scraper.%s' % item.__class__.__name__
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
                logger.error('Failed publish item to Google Cloud Pub/Sub: %s', e)
                self.stats.inc_value('google/pubsub/erros_count')
        
        return item


class GoogleBigQueryPipeline(BasePipeline):
    
    def __init__(self, settings, stats):
        self.google_cloud_enabled = settings.getbool('GOOGLE_CLOUD_ENABLED')
        
        if self.google_cloud_enabled:
            self.client = bigquery.Client()
            self.dataset = self.client.dataset(settings.get('GC_BIGQUERY_DATASET'))
            self.tables = {}
            self.schemas = {}
            
            self.stats = stats
            self.stats.set_value('google/bigquery/insert_count', 0)
            self.stats.set_value('google/bigquery/erros_count', 0)
            logger.info('Google Cloud BigQuery client initiated with success')
        else:
            logger.warning('Google Cloud BigQuery is not enabled, check Google Cloud extension configuration')
    
    def process_item(self, item, spider):
        if self.google_cloud_enabled:
            try:
                table_name = item.__class__.__name__
                table = self.tables.get(table_name)
                if not table:
                    table_schema = self.build_table_schema(item)
                    table = self.dataset.table(table_name, table_schema)
                    
                    if not table.exists():
                        table.create()
                    
                    self.tables[table_name] = table
                
                errors = table.insert_data([[item.get(c.name, None) for c in table.schema]])
                
                self.stats.inc_value('google/bigquery/insert_count') if not errors else None
                self.stats.inc_value('google/bigquery/erros_count') if errors else None
                if errors: 
                    logger.error(errors)
                    raise BadRequest
            except Exception as e:
                logger.error('Failed publish item to Google Cloud BigQuery: %s', e)
                self.stats.inc_value('google/bigquery/erros_count')
        
        return item
    
    def build_table_schema(self, item):
        
        def _parse_schema_fields(schema_field):
            schema_fields_list = schema_field.get('fields')
            schema_fields = []
            
            if schema_fields_list:
                for sf in schema_fields_list:
                    schema_fields.append(_parse_schema_fields(sf))
            
            return SchemaField(
                schema_field['name'], 
                schema_field['field_type'], 
                schema_field.get('mode', 'NULLABLE'), 
                schema_field.get('description', None), 
                schema_fields if schema_fields_list else None,
            )
        
        table_schema = []
        for field_key in item.fields:
            if item.fields[field_key].get('schemas'):
                if item.fields[field_key]['schemas'].get('avro'):
                    schema_field = item.fields[field_key]['schemas'].get('avro')
                    if schema_field:
                        schema_field['name'] = field_key
                        table_schema.append(_parse_schema_fields(schema_field))
        
        return table_schema