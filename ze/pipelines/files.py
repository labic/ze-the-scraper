# -*- coding: utf-8 -*-

from google.cloud import storage as GoogleCloudStorage

from twisted.internet import defer, threads

from scrapy.pipelines.files import FilesPipeline as ScrapyFilesPipeline
from scrapy.pipelines.files import FSFilesStore, S3FilesStore


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
    
    def __init__(self, store_uri, download_func=None, settings=None):
        self.STORE_SCHEMES = {
            '': FSFilesStore,
            'file': FSFilesStore,
            's3': S3FilesStore,
            'gs': GSFilesStore
        }
        # TODO: Move?
        self.media_items_fields = settings.get('MEDIA_ITEMS_FIELDS')
        self.media_base_url = settings.get('MEDIA_BASE_URL')
        self.image_base_path = settings.get('IMAGE_BASE_PATH')
        self.image_base_url = '%s%s' % (self.media_base_url, self.image_base_path)
        
        super(FilesPipeline, self).__init__(store_uri, download_func, settings)
