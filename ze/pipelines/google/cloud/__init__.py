# -*- coding: utf-8 -*-

import json
import logging; logger = logging.getLogger(__name__)

from scrapy.exceptions import NotConfigured
from ze.pipelines import BasePipeline
from google.cloud import bigquery
from google.cloud.bigquery.schema import SchemaField
from google.cloud import datastore
from google.cloud import pubsub
from google.cloud.exceptions import BadRequest


class GooglePubSubPipeline(BasePipeline):

    def __init__(self, settings, stats):
        google_cloud_enabled = settings.getbool('GOOGLE_CLOUD_ENABLED')
        enabled = settings.getbool('GOOGLE_CLOUD_PUBSUB_ENABLED')
        
        if google_cloud_enabled and enabled:
            self.stats = stats
            self.stats.set_value('google/pubsub/published_count', 0)
            self.stats.set_value('google/pubsub/erros_count', 0)
            
            self.client = pubsub.Client()
            self.topics = {}
            logger.info('Google Cloud Pub/Sub client initiated with success')
        else:
            raise NotConfigured('Google Cloud is not enabled, check settings values')

    def process_item(self, item, spider):
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
        google_cloud_enabled = settings.getbool('GOOGLE_CLOUD_ENABLED')
        enabled = settings.getbool('GOOGLE_CLOUD_BIGQUERY_ENABLED')
        
        if google_cloud_enabled and enabled:
            self.stats = stats
            self.stats.set_value('google/bigquery/insert_count', 0)
            self.stats.set_value('google/bigquery/erros_count', 0)
            
            self.client = bigquery.Client()
            self.dataset = self.client.dataset(settings.get('GOOGLE_CLOUD_BIGQUERY_DATASET'))
            self.tables = {}
            self.schemas = {}
            logger.info('Google Cloud BigQuery client initiated with success')
        else:
            raise NotConfigured('Google Cloud BigQuery is not enabled, check settings values')
    
    def process_item(self, item, spider):
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


class GoogleDatastorePipeline(BasePipeline):
    
    def __init__(self, settings, stats):
        google_cloud_enabled = settings.getbool('GOOGLE_CLOUD_ENABLED')
        enabled = settings.getbool('GOOGLE_CLOUD_DATASTORE_ENABLED')
        self.namespace = '__{0}__'.format(settings.get('ENVIROMENT', 'development')),
        
        if google_cloud_enabled and enabled:
            self.client = datastore.Client()
            # self.batch = self.client.batch()
            
            self.stats = stats
            self.stats.set_value('google/datastore/insert_count', 0)
            self.stats.set_value('google/datastore/erros_count', 0)
            logger.info('Google Cloud Datastore client initiated with success')
        else:
            raise NotConfigured('Google Cloud Datastore or Google Cloud or both is not enabled, check settings values')
        
    def process_item(self, item, spider):
        try:
            key = self.client.key(item.__class__.__name__, self.namespace)
            
            exclude_from_indexes = [k for k in item.fields \
                if item.fields[k].get('indexed', True) is False]
            
            entity = datastore.Entity(key, exclude_from_indexes)
            
            entity.update(self.seriealize(item))
            
            self.client.put(entity)
            self.stats.inc_value('google/datastore/insert_count')
        except Exception as e:
            self.stats.inc_value('google/datastore/erros_count')
            raise e
        
        return item
    
    def seriealize(self, item):
        for k in item.fields.keys():
            schemas = item.fields[k].get('schemas', {})
            datastore_schema = schemas.get('datastore')
            if datastore_schema:
                if datastore_schema['field_type'] is 'arrayValue':
                    if datastore_schema['values']['field_type'] is 'entityValue':
                        entity_values = []
                        for p, it in enumerate(item[k]):
                            e_key = self.client.key(''.join((k, str(p))))
                            entity_value = datastore.Entity(e_key)
                            entity_value.update(it)
                            entity_values.append(entity_value)
                        item[k] = entity_values
        
        return item