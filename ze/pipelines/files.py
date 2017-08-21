# -*- coding: utf-8 -*-

import logging; logger = logging.getLogger(__name__)

from google.cloud import storage as GoogleCloudStorage
from bs4 import BeautifulSoup
from twisted.internet import defer, threads
from twisted.internet.defer import Deferred, DeferredList

from scrapy import Request
from scrapy.pipelines.files import FilesPipeline as ScrapyFilesPipeline
from scrapy.pipelines.files import FSFilesStore, S3FilesStore
from scrapy.utils.misc import arg_to_iter


class GSFilesStore(object):

    def __init__(self, uri):
        assert uri.startswith('gs://')
        client = GoogleCloudStorage.Client()
        bucket, self.prefix = uri[5:].split('/', 1)
        self.bucket = client.bucket(bucket)

    def stat_file(self, path, info):
        key_name = '%s%s' % (self.prefix, path)
        blob = self.bucket.get_blob(key_name)
        
        return {'checksum': blob.etag, 
                'last_modified': blob.updated.timestamp()}

    def persist_file(self, path, buf, info, meta=None, headers=None):
        """Upload file to Google Cloud storage"""
        key_name = '%s%s' % (self.prefix, path)
        buf.seek(0)
        blob = GoogleCloudStorage.Blob(key_name, self.bucket)
        
        return threads.deferToThread(
                blob.upload_from_string, data=buf.getvalue(),
                content_type=headers['Content-Type'])


class FilesPipeline(ScrapyFilesPipeline):
    
    STORE_SCHEMES = {
        '': FSFilesStore,
        'file': FSFilesStore,
        's3': S3FilesStore,
        'gs': GSFilesStore
    }
    
    def __init__(self, store_uri, download_func=None, settings=None):
        self.media_items_fields = settings.get('MEDIA_ITEMS_FIELDS')
        self.media_base_url = settings.get('MEDIA_BASE_URL')
        self.image_base_path = settings.get('IMAGES_BASE_PATH')
        self.image_base_url = '%s%s' % (self.media_base_url, self.image_base_path)
        
        super(FilesPipeline, self).__init__(store_uri, download_func, settings)
    
    
    def process_item(self, item, spider):
        info = self.spiderinfo
        # TODO: Refactor this!
        qualname = type(item).__qualname__
        media_fields = self.media_items_fields.get(qualname, None)
        
        if media_fields:
            info.media_fields = media_fields
            info.urls_fields = {}
            
            requests = arg_to_iter(self.get_media_requests(item, info))
            dlist = [self._process_request(r, info) for r in requests]
            dfd = DeferredList(dlist, consumeErrors=1)
            return dfd.addCallback(self.item_completed, item, info)
        else:
            logger.warning('Don\'t have MEDIA_ITEMS_FIELDS to %s'%spider.name)
            return item
    
    def get_media_requests(self, item, info):
        files_fields = info.media_fields.get('files')
        if files_fields:
            files_urls = []; append_files_urls = files_urls.append
            for file_field, extract_format in files_fields.items():
                if file_field in item:
                    if extract_format == 'url':
                        append_files_urls((item[file_field], 
                                          (file_field, extract_format)))
                    
                    if extract_format == 'urls':
                        for file_url in item[file_field]:
                            append_files_urls((file_url, 
                                              (file_field, extract_format)))
                    
                    if extract_format == 'html':
                        html = BeautifulSoup(item[file_field], 'html.parser')
                        for img in html.findAll('img'):
                            append_files_urls((img['src'], 
                                              (file_field, extract_format)))
            
            
            for file_url, file_field in files_urls:
                info.urls_fields.setdefault(file_url, 
                                            set()).add(file_field)
                yield Request(file_url,
                              meta={'file_field': file_field, 'info': info})
        else:
            logger.info('Don\'t have set files fields in MEDIA_ITEMS_FIELDS \
                        setting to %s class' %item.__class__.__name__)