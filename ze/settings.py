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

PROJECT_NAME = 'ze-the-scraper'
SPIDER_MODULES = ['ze.spiders']
NEWSPIDER_MODULE = 'ze.spiders'

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
# SPIDER_MIDDLEWARES = {
#     'ze.middlewares.somemiddkeware': 100,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

# ROTATING_PROXY_LIST = ze.utils.file.load_lines('./proxies-list.txt')

GOOGLE_CLOUD_ENABLED = True
# Google Cloud Application Credentions used for many pipelines
GOOGLE_APPLICATION_CREDENTIALS_JSON = ''
# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'ze.extensions.google.GoogleCloud': 10
}

# MongoDB pipeline configuration
MONGO_ENABLED = False
MONGO_URI = None
MONGO_DATABASE = None

# Google Cloud BigQuery pipeline configuration
GOOGLE_CLOUD_BIGQUERY_ENABLED = False
GOOGLE_CLOUD_BIGQUERY_DATASET = ''
# Google Cloud Datastore pipeline configuration
GOOGLE_CLOUD_DATASTORE_ENABLED = False
# Google Cloud Pub/Sub pipeline configuration
GOOGLE_CLOUD_PUBSUB_ENABLED = False
# Configure item pipelines
ITEM_PIPELINES = {
    # 'ze.pipelines.MongoPipeline': 200,
    # 'ze.pipelines.GooglePubSubPipeline': 300,
    'ze.pipelines.GoogleDatastorePipeline': 400,
    # 'ze.pipelines.GoogleBigQueryPipeline': 500,
}

# SPIDER_CONTRACTS = {
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
# HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
# HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
# HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
