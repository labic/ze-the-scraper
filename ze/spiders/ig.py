# -*- coding: utf-8 -*-

import ze
from ze.items.newsarticle import NewsArticleItem

class IgSpider(ze.spiders.ZeSpider):

    name = 'ig'
    allowed_domains = ['ig.com.br']

    def load_article_item(self, response):
        l = ze.items.ItemLoader(item=NewsArticleItem(), response=response)

        l.add_css('name', '[itemprop=headline]::text')
        l.add_fallback_css('name', '#noticia-titulo-h1::text')
        l.add_css('image', '[property="og:image"]::attr(content)')
        l.add_css('author', '[itemprop="creator"] [itemprop="name"]::text')
        l.add_fallback_css('author', '#authors-box::text')
        # l.add_fallback_css('author', '#authors-box strong::text')
        l.add_css('description', '[property="og:description"]::attr(content)')
        l.add_fallback_css('description', '[property="description"]::attr(content)')
        l.add_css('datePublished', '[property="article:published_time"]::attr(content)')
        l.add_fallback_css('datePublished', '[itemprop="datePublished"]::text')
        # l.add_css('dateModified', '[itemprop=dateModified]::text')
        l.add_css('keywords', '[name="news_keywords"]::attr(content)')
        l.add_css('articleBody', '[itemprop=articleBody]')
        l.add_fallback_css('articleBody', '#noticia')
        # TODO: Add publisher
        l.add_value('url', response.url)
        
        if 'blog' in response.url:
            l.add_value('sources_types', ('portal', 'blog'))
        else:
            l.add_value('sources_types', ('portal'))

        yield l.load_item()
