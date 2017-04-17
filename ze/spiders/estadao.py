# -*- coding: utf-8 -*-

import ze
from ze.items.article import NewsArticleItem

class EstadaoSpider(ze.spiders.ZeSpider):

    name = 'estadao'
    allowed_domains = ['estadao.com.br']

    def load_article_item(self, response):
        l = ze.items.ItemLoader(item=NewsArticleItem(), response=response)

        l.add_css('name', '[itemprop=headline]::text')
        l.add_fallback_css('name', '.titulo-principal::text')
        l.add_css('author', '[itemprop=author]::text')
        l.add_css('description', '[itemprop=description]::text')
        l.add_fallback_css('description', '.linha-fina::text')
        l.add_css('datePublished', '[itemprop=datePublished]::text')
        l.add_fallback_css('datePublished', '.data::text')
        l.add_css('dateModified', '[itemprop=dateModified]::text')
        l.add_css('keywords', '[itemprop=keywords] a::text')
        l.add_fallback_css('keywords', '.tags a::text')
        l.add_fallback_css('keywords', '.tags a span::text')
        l.add_css('articleBody', '[itemprop=articleBody]')
        l.add_fallback_css('articleBody', '.main-news .content')
        l.add_value('url', response.url)
        
        if 'blog' in response.url:
            l.add_value('sources_types', ('portal', 'blog'))
        else:
            l.add_value('sources_types', ('portal'))

        yield l.load_item()
