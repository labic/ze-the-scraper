# -*- coding: utf-8 -*-

import subprocess
import json
import scrapy
from scrapy.loader import ItemLoader
from ze.items.article import ArticleItem, ArticleItemLoader

class VejaSpider(scrapy.Spider):

    name = 'veja'
    allowed_domains = ['veja.abril.com.br']
    start_urls = []
    config = {
        'searchlUrl': 'http://veja.abril.com.br/?infinity=scrolling',
        'args': None
    }
    DURATIONS = {
        'PT24H': 'h24',
        'P1D': 'd1',
        'P2D': 'd2',
        'P3D': 'd3',
        'P4D': 'd4',
        'P5D': 'd5',
        'P6D': 'd6',
        'P1W': 'w1',
        'P2W': 'w2',
        'P3W': 'w3',
        'P1M': 'm1',
        'P2M': 'm2',
        'P3M': 'm3',
        'P4M': 'm4',
        'P5M': 'm5',
        'P6M': 'm6',
        'P7M': 'm7',
        'P8M': 'm8',
        'P9M': 'm9',
    }


    def __init__(self, url=None, query=None, editorial=None, subject=None, when=None, contentType=None, googler=False, *args, **kwargs):
        super(VejaSpider, self).__init__(*args, **kwargs)
        
        self.config['args'] = {
            'source': 'url', 
            'url': url, 
            'formdata': {
                'action': 'infinite_scroll',
                'page': '1',
                'currentday': '29.03.17',
                'order': 'DESC',
                'query_args[paged]': '0',
                'query_args[category_name]': 'educacao',
                'query_args[p]': '0',
                'query_args[second]': '',
                'query_args[minute]': '',
                'query_args[hour]': '',
                'query_args[day]': '',
                'query_args[monthnum]': '0',
                'query_args[year]': '0',
                'query_args[w]': '0',
                'query_args[tag]': '',
                'query_args[cat]': '515646675',
                'query_args[tag_id]': '',
                'query_args[author]': '',
                'query_args[author_name]': '',
                'query_args[feed]': '',
                'query_args[sentence]': '',
                'query_args[title]': '',
                'query_args[fields]': '',
                'query_args[post_type][0]': 'post',
                'query_args[post_type][1]': 'video',
                'query_args[post_type][2]': 'blog_post',
                'query_args[post_type][3]': 'special_post',
                'query_args[posts_per_page]': '10',
                'query_args[cache_results]': 'false',
                'query_args[update_post_term_cache]': 'true',
                'query_args[lazy_load_term_meta]': 'false',
                'query_args[update_post_meta_cache]': 'true',
                'query_args[nopaging]': 'false',
                'query_args[comments_per_page]': '10',
                'query_args[no_found_rows]': 'false',
                'query_args[order]': 'DESC',
                'query_args[extra][is_tag]': 'false',
                'query_args[extra][is_category]': 'true',
                'query_args[extra][is_admin]': 'false',
                'last_post_date': '2017-03-19 12:24:15',
            },
        }
        
        if url:
            self.start_urls = [self.config['args']['url']]
        if googler:
            results = json.loads(subprocess.check_output(
                ['python ../libs/googler.py -n 100 -w %s %s --json' % ('veja.abril.com.br', query)], 
                shell=True,
                stderr=subprocess.STDOUT,
            ).decode('utf-8'))
            self.start_urls = [r['url'] for r in results]
        else:
            self.config['args']['source'] = 'searchlUrl'


    def start_requests(self):
        if self.config['args']['source'] == 'url':
            yield scrapy.Request(self.config['args']['url'], callback=self.parse_article)
        if self.config['args']['source'] == 'searchlUrl':
            yield scrapy.FormRequest(url=self.config['searchlUrl'],
                                     formdata=self.config['args']['formdata'],
                                     callback=self.parse_article_urls)
        

    def parse_article_urls(self, response):
        self.logger.info(response.body)
        for i, url in enumerate(response.css('.link-title::attr(href)').extract()):
            yield scrapy.Request(url, meta={'index': i}, callback=self.parse_article)


    def parse_article(self, response):
        l = ArticleItemLoader(item=ArticleItem(), response=response)

        l.add_css('name', '[itemprop=headline]::text')
        l.add_fallback_css('name', '.article-title::text')
        l.add_css('authors', '[itemprop=author]::text')
        l.add_fallback_css('authors', '.article-author span strong::text')
        l.add_css('description', '[itemprop=description]::text')
        l.add_fallback_css('description', '.article-subtitle::text')
        l.add_css('date_published', '[itemprop=datePublished]::text')
        l.add_fallback_css('date_published', '.article-date span::text')
        l.add_css('date_modified', '[itemprop=dateModified]::text')
        l.add_fallback_css('date_modified', '.article-date span::text')
        l.add_css('keywords', '[itemprop=keywords] a::text')
        l.add_fallback_css('keywords', '.article-tags a::text')
        l.add_css('text', '[itemprop=articleBody]')
        l.add_fallback_css('text', '.article-content')
        l.add_value('url', response.url)
        
        if 'blog' in response.url:
            l.add_value('sources_types', ('portal', 'blog'))
        else:
            l.add_value('sources_types', ('portal'))

        yield l.load_item()