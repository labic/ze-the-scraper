# -*- coding: utf-8 -*-

import ze
from ze.items.newsarticle import NewsArticleItem

class FolhaDeSaoPauloSpider(ze.spiders.ZeSpider):

    name = 'folhadesp'
    allowed_domains = ['folha.uol.com.br']

    def load_article_item(self, response):
        l = ze.items.ItemLoader(item=NewsArticleItem(), response=response)

        l.add_css('name', '[itemprop=headline]::text')
        l.add_fallback_css('name', '[itemprop="alternativeHeadline"]::attr(content)')
        l.add_fallback_css('name', 'article header h1::text')
        l.add_css('image', '[itemprop="image"]::attr(content)')
        l.add_css('author', '[itemprop=author]::text')
        l.add_fallback_css('author', '.author p::text')
        l.add_css('description', '[itemprop=description]::text')
        l.add_css('datePublished', '[itemprop=datePublished]::text')
        l.add_fallback_css('datePublished', 'article time::text')
        l.add_css('dateModified', '[itemprop=dateModified]::text')
        l.add_css('keywords', '[itemprop="keywords"]::attr(content)')
        l.add_css('articleBody', '[itemprop=articleBody]')
        l.add_fallback_css('articleBody', '.content')
        # TODO: Add publisher
        l.add_value('url', response.url)
        
        if 'blog' in response.url:
            l.add_value('sources_types', ('portal', 'blog'))
        else:
            l.add_value('sources_types', ('portal'))

        yield l.load_item()