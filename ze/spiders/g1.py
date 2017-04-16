# -*- coding: utf-8 -*-

import ze
from ze.items.newsarticle import NewsArticleItem

class EstadaoArticlesSpider(ze.spiders.ZeSpider):

    name = 'g1'
    allowed_domains = ['g1.globo.com']

    def load_article_item(self, response):
        l = ze.items.ItemLoader(item=NewsArticleItem(), response=response)

        l.add_css('name', '[itemprop=headline]::text')
        l.add_fallback_css('name', '.content-head__title::text')
        l.add_css('author', '[itemprop=creator]::text')
        # l.add_css('publisher', '[itemprop=publisher]::attr(content)')
        l.add_css('description', '[itemprop=alternativeHeadline]::text')
        l.add_fallback_css('description', '.content-head__subtitle::text')
        l.add_css('datePublished', '[itemprop=datePublished]::attr(datetime)')
        l.add_css('dateModified', '[itemprop=dateModified]::attr(datetime)')
        l.add_css('articleBody', '.mc-body')
        l.add_css('keywords', '.entities__list-itemLink::text')
        l.add_value('url', response.url)
        
        if 'blog' in response.url:
            l.add_value('sources_types', ('portal', 'blog'))
        else:
            l.add_value('sources_types', ('portal'))

        yield l.load_item()