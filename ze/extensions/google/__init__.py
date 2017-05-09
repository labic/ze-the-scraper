# -*- coding: utf-8 -*-

import os, logging; logger = logging.getLogger(__name__)
from scrapy.utils.project import data_path

class GoogleCloud(object):
    credentials_json_path = ''.join((data_path('auth/', True), 'google-service-account.json'))
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings)

    def __init__(self, settings):
        self.google_cloud_enabled = settings.getbool('GOOGLE_CLOUD_ENABLED')
        
        if self.google_cloud_enabled:
            credentials_json = settings.get('GOOGLE_CLOUD_APPLICATION_CREDENTIALS_JSON')
            if credentials_json:
                if not os.path.isfile(self.credentials_json_path):
                    with open(self.credentials_json_path, 'w') as outfile:
                        outfile.write(credentials_json)
                    
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials_json_path
                logger.info('Google Cloud extensions inited with success')
            else:
                logger.error('GOOGLE_CLOUD_APPLICATION_CREDENTIALS_JSON not is set in settings')
                settings.set('GOOGLE_CLOUD_ENABLED', False)
        else:
            logger.info('GOOGLE_CLOUD_ENABLED is False')

    def close_spider(self, spider):
        if self.google_cloud_enabled \
        and os.path.isfile(self.credentials_json_path):
            os.remove(self.credentials_json_path)
