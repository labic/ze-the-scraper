# -*- coding: utf-8 -*-
import os

# Scrapy settings for ze module
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = os.getenv('BOT_NAME', 'ze-the-scraper')
SPIDER_MODULES = os.getenv('SPIDER_MODULES', 'ze.spiders')
NEWSPIDER_MODULE = os.getenv('SPIDER_MODULES', 'ze.spiders')
COMMANDS_MODULE = os.getenv('COMMANDS_MODULE', 'ze.commands')
ENVIROMENT = os.getenv('ENVIROMENT', 'development')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
DUPEFILTER_DEBUG = True

SPIDERS_AUTH = os.getenv('SPIDERS_AUTH', {'somespider': {'user': 'USER', 'pass': 'PASS'}})

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/56.0.2924.76 Chrome/56.0.2924.76 Safari/537.36'

# Configure maximum concurrent requests performed by Scrapy
CONCURRENT_REQUESTS = os.getenv('CONCURRENT_REQUESTS', 32)

# Configure a delay for requests for the same website
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = os.getenv('CONCURRENT_REQUESTS_PER_DOMAIN', 16)
CONCURRENT_REQUESTS_PER_IP = os.getenv('CONCURRENT_REQUESTS_PER_IP', 16)

# Enable or Disable cookies
COOKIES_ENABLED = os.getenv('COOKIES_ENABLED', False)

# Disable Telnet Console
TELNETCONSOLE_ENABLED = os.getenv('TELNETCONSOLE_ENABLED', False)

# Enable or disable extensions
EXTENSIONS={
    'ze.extensions.google.GoogleCloud': 10,
}
# ROTATING_PROXY_LIST = ze.utils.file.load_lines('./proxies-list.txt')
# Google Cloud Application
GOOGLE_CLOUD_ENABLED = os.getenv('GOOGLE_CLOUD_ENABLED', False)
# Google Cloud Application Credentions used for many pipelines
GOOGLE_CLOUD_APPLICATION_CREDENTIALS_JSON = os.getenv('GOOGLE_CLOUD_APPLICATION_CREDENTIALS_JSON', None)

FEED_EXPORTERS = {
    'avro': 'ze.exporters.AvroItemExporter',
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
DELTAFETCH_ENABLED = os.getenv('DELTAFETCH_ENABLED', False)
SEARCH_MIDDLEWARE_ENABLED = os.getenv('SEARCH_MIDDLEWARE_ENABLED', True)
# Search source gcse_api and googler. Ex: SEARCH_MIDDLEWARE_SOURCES='gcse_api,googler'
SEARCH_MIDDLEWARE_SOURCES = os.getenv('SEARCH_MIDDLEWARE_SOURCES', 'googler')
SEARCH_MIDDLEWARE_GCSE_API_KEY = os.getenv('SEARCH_MIDDLEWARE_GCSE_API_KEY', None)
SEARCH_MIDDLEWARE_GCSE_CX = os.getenv('SEARCH_MIDDLEWARE_GCSE_CX', None)
SEARCH_MIDDLEWARE_GCSE_MAX_INDEX = os.getenv('SEARCH_MIDDLEWARE_GCSE_MAX_INDEX', None)

SPIDER_MIDDLEWARES = {
    'ze.middlewares.spider.searchengines.GoogleSearchMiddleware': 40,
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,
    # 'scrapy_deltafetch.DeltaFetch': 100,
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 500,
    'scrapy.spidermiddlewares.referer.RefererMiddleware': 700,
    'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware': 800,
    'scrapy.spidermiddlewares.depth.DepthMiddleware': 900,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
    # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
# }

ITEM_PIPELINES={
    'ze.pipelines.ItemsSideValues': 0,
    'ze.pipelines.DropItemsPipeline': 10,
    # 'ze.pipelines.images.ImagesPipeline': 20,
    'ze.pipelines.databases.MongoPipeline': 200,
    'ze.pipelines.google.cloud.GooglePubSubPipeline': 300,
    'ze.pipelines.google.cloud.GoogleDatastorePipeline': 400,
    'ze.pipelines.google.cloud.GoogleBigQueryPipeline': 500,
}
DROP_ITEM_PIPELINE_ENABLED = os.getenv('DROP_ITEM_PIPELINE_ENABLED', False)
DROP_ITEM_PIPELINE_VALIDATIONS = os.getenv('DROP_ITEM_PIPELINE_VALIDATIONS', 'not_match_regex, empty_required_fields')
# MongoDB pipeline configuration
MONGO_ENABLED = os.getenv('MONGO_ENABLED', False)
MONGO_URI = os.getenv('MONGO_URI', 'mongo://localhost:2700/scrapy')
# Google Cloud BigQuery pipeline configuration
GOOGLE_CLOUD_BIGQUERY_ENABLED = os.getenv('GOOGLE_CLOUD_BIGQUERY_ENABLED', False)
GOOGLE_CLOUD_BIGQUERY_DATASET  = os.getenv('GOOGLE_CLOUD_BIGQUERY_DATASET', None)
# Google Cloud Datastore pipeline configuration
GOOGLE_CLOUD_DATASTORE_ENABLED = os.getenv('GOOGLE_CLOUD_BIGQUERY_ENABLED', False)
# Google Cloud Pub/Sub pipeline configuration
GOOGLE_CLOUD_PUBSUB_ENABLED = os.getenv('GOOGLE_CLOUD_PUBSUB_ENABLED', False)
GOOGLE_CLOUD_STORAGE_BUCKET = os.getenv('GOOGLE_CLOUD_STORAGE_BUCKET', None)
# Configure item pipelines
MERGE_DUPLICATES = os.getenv('MERGE_DUPLICATES', True)

MEDIA_ALLOW_REDIRECTS = os.getenv('MEDIA_ALLOW_REDIRECTS', True)
MEDIA_BASE_URL = os.getenv('MEDIA_BASE_URL', 'https://sub.domain.net')
MEDIA_ITEMS_FIELDS={
    'ArticleItem': { 
        'images': { 
            'image': 'urls',
            'articleBody': 'html',
        },
        'files': None
    },
    'NewsArticleItem': { 
        'images': None,
        'files': { 
            'url': 'url',
        }
    }
}
FILES_STORE = os.getenv('FILES_STORE', '../data/files')
FILES_BASE_URL_PATH = os.getenv('FILES_STORE', '/dev')

IMAGES_STORE = os.getenv('IMAGES_STORE', '../data/images')
IMAGES_URLS_FIELD = os.getenv('IMAGES_URLS_FIELD', '/dev')
IMAGES_URLS_FIELD = 'images_to_download_urls'
IMAGES_RESULT_FIELD = 'images_downloaded_urls'
IMAGES_THUMBS={
    'small': (50, 50),
    'big': (270, 270),
}

# SPIDER_CONTRACTS={
#     'scrapy.contracts.default.UrlContract': 10,
#     'scrapy.contracts.default.ReturnsContract': 20,
#     'scrapy.contracts.default.ScrapesContract': 30,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED=True
HTTPCACHE_EXPIRATION_SECS=21600
HTTPCACHE_DIR='httpcache'
HTTPCACHE_IGNORE_HTTP_CODES=[400, 401, 402, 403, 404, 500, 503]
HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
