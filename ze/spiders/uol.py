# -*- coding: utf-8 -*-

import ze
from ze.items.article import NewsArticleItem

class EstadaoArticlesSpider(ze.spiders.ZeSpider):

    name = 'uol'
    allowed_domains = ['uol.com.br']

    def load_article_item(self, response):
        l = ze.items.ItemLoader(item=NewsArticleItem(), response=response)

        l.add_css('name', 'h1::text')
        l.add_css('author', '.autores::text')
        l.add_css('description', '.definicao::text')
        l.add_css('datePublished', '.data::text')
        l.add_css('dateModified', '.data::text')
        # l.add_css('keywords', '[itemprop=keywords] a::text')
        l.add_css('articleBody', '.conteudo-materia')
        l.add_value('url', response.url)

        yield l.load_item()
