# -*- coding: utf-8 -*-

import ze
from ze.items.article import NewsArticleItem

class VejaSpider(ze.spiders.ZeSpider):
    
    name = 'veja'
    allowed_domains = ['veja.abril.com.br']
    start_urls = []
    
    def load_article_item(self, response):
        """ parse_article_with invalid url
        @url http://veja.abril.com.br/noticias-sobre/educacao/
        @returns items 0
        """
        l = ze.items.ItemLoader(item=NewsArticleItem(), response=response)
        
        l.add_css('name', '[itemprop=headline]::text')
        l.add_fallback_css('name', '.article-title::text')
        l.add_css('author', '[itemprop=author]::text')
        l.add_fallback_css('author', '.article-author span strong::text')
        l.add_css('description', '[itemprop=description]::text')
        l.add_fallback_css('description', '.article-subtitle::text')
        l.add_css('datePublished', '[itemprop=datePublished]::text')
        l.add_fallback_css('datePublished', '.article-date span::text')
        l.add_css('dateModified', '[itemprop=dateModified]::text')
        l.add_fallback_css('dateModified', '.article-date span::text')
        l.add_css('keywords', '[itemprop=keywords] a::text')
        l.add_fallback_css('keywords', '.article-tags a::text')
        l.add_css('articleBody', '[itemprop=articleBody]')
        l.add_fallback_css('articleBody', '.article-content')
        l.add_value('url', response.url)
        
        if 'blog' in response.url:
            l.add_value('sources_types', ('portal', 'blog'))
        else:
            l.add_value('sources_types', ('portal'))
        
        yield l.load_item()