# -*- coding: utf-8 -*-
import ze.utils.file

# Scrapy settings for ze module
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ze-the-scraper'
SPIDER_MODULES = ['ze.spiders']
NEWSPIDER_MODULE = 'ze.spiders'
COMMANDS_MODULE = 'ze.commands'

DUPEFILTER_DEBUG = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/56.0.2924.76 Chrome/56.0.2924.76 Safari/537.36'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN=16
CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
# COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
GOOGLE_SEARCH_MIDDLEWARE_ENABLED=True
GOOGLE_SEARCH_MIDDLEWARE_LIB='google_rest'
GOOGLE_SEARCH_MIDDLEWARE_API_KEY=None
GOOGLE_SEARCH_MIDDLEWARE_CUSTOM_SEARCH_ENGINE_ID=None
GOOGLE_SEARCH_MIDDLEWARE_CACHE_EXPIRATION_SECS=10800
GOOGLE_SEARCH_MIDDLEWARE_MAX_INDEX=None

SPIDER_MIDDLEWARES = {
    'ze.middlewares.spider.searchengines.GoogleSearchMiddleware': 40,
    'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,
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

# ROTATING_PROXY_LIST = ze.utils.file.load_lines('./proxies-list.txt')
DROP_ITEM_PIPELINE_ENABLED=False
DROP_ITEM_PIPELINE_VALIDATION_METHODS=[
    'drop_items_with_empty_fields',
    'drop_items_that_not_match_regex',
]
# Google Cloud Application
GOOGLE_CLOUD_ENABLED=True
# Google Cloud Application Credentions used for many pipelines
GOOGLE_CLOUD_APPLICATION_CREDENTIALS_JSON=''
# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
EXTENSIONS={
    'ze.extensions.google.GoogleCloud': 10
}

# MongoDB pipeline configuration
MONGO_ENABLED=False
MONGO_URI=None
MONGO_DATABASE=None
# Google Cloud BigQuery pipeline configuration
GOOGLE_CLOUD_BIGQUERY_ENABLED=False
GOOGLE_CLOUD_BIGQUERY_DATASET=''
# Google Cloud Datastore pipeline configuration
GOOGLE_CLOUD_DATASTORE_ENABLED=False
# Google Cloud Pub/Sub pipeline configuration
GOOGLE_CLOUD_PUBSUB_ENABLED=False
# Configure item pipelines
ITEM_PIPELINES={
    'ze.pipelines.DropItemsPipeline': 10,
    'ze.pipelines.databases.MongoPipeline': 200,
    'ze.pipelines.google.cloud.GooglePubSubPipeline': 300,
    'ze.pipelines.google.cloud.GoogleDatastorePipeline': 400,
    'ze.pipelines.google.cloud.GoogleBigQueryPipeline': 500,
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
HTTPCACHE_IGNORE_HTTP_CODES=[403, 500]
HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
