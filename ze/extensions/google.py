import os, logging

logger = logging.getLogger(__name__)

class GoogleCloud(object):
    credentials_json_file = '../service-account.json'
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings=crawler.settings)

    def __init__(self, settings):
        self.google_cloud_enabled = settings.getbool('GOOGLE_CLOUD_ENABLED')
        
        if self.google_cloud_enabled:
            credentials_json = settings.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
            if credentials_json:
                with open(self.credentials_json_file, 'w') as outfile:
                    outfile.write(credentials_json)
                        
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials_json_file
                logger.info('Google Cloud extensions inited with success')
            else:
                logger.error('GOOGLE_APPLICATION_CREDENTIALS_JSON not is set in settings')
                settings.set('GOOGLE_CLOUD_ENABLED', False)
        else:
            logger.info('GOOGLE_CLOUD_ENABLED is False')


    def close_spider(self, spider):
        if self.google_cloud_enabled:
            os.remove(self.credentials_json_file)
