# -*- coding: utf-8 -*-

import ze
from ze.items.article import NewsArticleItem

class CartaCapitalSpider(ze.spiders.ZeSpider):

    name = 'cartacapital'
    allowed_domains = ['cartacapital.com.br', 'cartaeducacao.com.br']

    def load_article_item(self, response):
        l = ze.items.ItemLoader(item=NewsArticleItem(), response=response)
        l.context['spider'] = self.name
        
        l.add_css('name', '[itemprop=headline]::text')
        l.add_fallback_css('name', '.documentFirstHeading::text')
        l.add_css('author', '[itemprop=author]::text')
        l.add_css('author', '.documentAuthor a::text')
        l.add_css('description', '[itemprop=description]::text')
        l.add_fallback_css('description', '.documentDescription::text')
        l.add_css('datePublished', '[itemprop=datePublished]::text')
        l.add_fallback_css('datePublished', '.documentPublished::text')
        l.add_css('dateModified', '[itemprop=dateModified]::text')
        l.add_css('keywords', '[property="rnews:keywords"] a::text')
        l.add_fallback_css('keywords', '#category .link-category a::text')
        l.add_css('articleBody', '[itemprop=articleBody]')
        l.add_fallback_css('articleBody', '.td-post-content')
        l.add_fallback_css('articleBody', '#content-core')
        # TODO: Add publisher
        l.add_value('url', response.url)
        
        if 'blog' in response.url:
            l.add_value('sources_types', ('portal', 'blog'))
        else:
            l.add_value('sources_types', ('portal'))

        yield l.load_item()