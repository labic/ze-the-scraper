# -*- coding: utf-8 -*-

import time
from urllib.parse import urlparse
import logging; logger = logging.getLogger(__name__)

from bs4 import BeautifulSoup
from twisted.internet import defer

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline as ScrapyImagesPipeline
from scrapy.utils.log import failure_to_exc_info
from scrapy.utils.request import referer_str

from .files import FilesPipeline


class ImagesPipeline(ScrapyImagesPipeline, FilesPipeline):
    
    def get_media_requests(self, item, info):
        images_fields = info.media_fields.get('images')
        if images_fields:
            images_urls = []; append_images_urls = images_urls.append
            for image_field, extract_format in images_fields.items():
                if image_field in item:
                    if extract_format == 'url':
                        append_images_urls((item[image_field].strip(), 
                                            (image_field, extract_format)))
                    
                    if extract_format == 'urls':
                        for image_url in item[image_field]:
                            append_images_urls((image_url.strip(), 
                                                (image_field, extract_format)))
                    
                    if extract_format == 'html':
                        html = BeautifulSoup(item[image_field], 'html.parser')
                        for img in html.findAll('img'):
                            append_images_urls((img['src'].strip(), 
                                                (image_field, extract_format)))
            
            for image_url, image_field in images_urls:
                if 'scheme' in urlparse(image_url):
                    info.urls_fields.setdefault(image_url, 
                                                set()).add(image_field)
                    yield Request(image_url,
                                  meta={'image_field': image_field, 'info': info})
        else:
            logger.info('Don\'t have set images fields in MEDIA_ITEMS_FIELDS \
                        setting to %s class' %item.__class__.__name__)
    
    def media_to_download(self, request, info):
        def _onsuccess(result):
            if not result:
                return  # returning None force download

            last_modified = result.get('last_modified', None)
            if not last_modified:
                return  # returning None force download

            age_seconds = time.time() - last_modified
            age_days = age_seconds / 60 / 60 / 24
            if age_days > self.expires:
                return  # returning None force download

            referer = referer_str(request)
            logger.debug(
                'File (uptodate): Downloaded %(medianame)s from %(request)s '
                'referred in <%(referer)s>',
                {'medianame': self.MEDIA_NAME, 'request': request,
                 'referer': referer},
                extra={'spider': info.spider}
            )
            self.inc_stats(info.spider, 'uptodate')

            checksum = result.get('checksum', None)
            
            return {
                'checksum': checksum, 
                # TODO: Refactor this!
                'image_fields': info.urls_fields[request.url],
                'url': request.url, 
                'path': '%s%s' % (self.image_base_url, path), }
        
        path = self.file_path(request, info=info)
        dfd = defer.maybeDeferred(self.store.stat_file, path, info)
        dfd.addCallbacks(_onsuccess, lambda _: None)
        dfd.addErrback(
            lambda f:
            logger.error(self.__class__.__name__ + '.store.stat_file',
                         exc_info=failure_to_exc_info(f),
                         extra={'spider': info.spider})
        )
        return dfd
    
    def item_completed(self, results, item, info):
        fields_results = {}
        
        for ok, r in results:
            if ok and 'image_fields' in r:
                for image_field, extract_format in list(r['image_fields']):
                    key = '%s_%s_%s' % (image_field, extract_format, r['path'])
                    if not fields_results.get(key):
                        fields_results.setdefault(key, []).append(r)
        
        for key, results in fields_results.items():
            if ok:
                field, extract_format, _ = key.split('_')
                
                if extract_format == 'url':
                    item[field] = r['url']
                
                if extract_format == 'urls':
                    item[field] = [result['path'] for result in fields_results[key]]
                
                if extract_format == 'html':
                    for r in fields_results[key]:
                        item[field] = item[field].replace(r['url'], r['path'])
        
        return item
