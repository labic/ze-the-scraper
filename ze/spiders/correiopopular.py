# -*- coding: utf-8 -*-

#TODO:articleBody datePublished dateModified
from ze.spiders import ZeSpider

class CorreioPopularSpider(ZeSpider):

    name = 'correiopopular'
    allowed_domains = ['correio.rac.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name": [
                    "meta[property='og:title']::attr(content)",
                    "meta[name=title]::attr(content)",
                    '[itemprop=headline]::text',
                    '.news-title::text'
                ],
                "image": [
                    "meta[property='og:image']::attr(content)",
                    '[itemprop="image"] img::attr(src)',
                    '#foto_auto img::attr(src)'
                ],
                "description": [
                    "meta[property='og:description']::attr(content)",
                    "meta[name=description]::attr(content)",
                    '[itemprop=description]::attr(content)',
                    '[itemprop=description]::text',
                    '.resumo h2::text'
                ],
                "author": [
                    '[itemprop=author]::text',
                    '.publish-by b::text'
                ],
                "datePublished": [
                    '[itemprop=datePublished]::attr(content)',
                    "meta[name='DC.date.created']::attr(content)",
                    '.publish-time::text',#dateModified ta junto
                ],
                "dateModified": [
                    '[itemprop=dateModified]::attr(content)',
                    '.publish-time::text',#datePublished ta junto
                ],
                "articleBody": [
                    '[itemprop=articleBody]',
                    '.article-container'
                ],
                "keywords": [
                    '[itemprop=keywords] a::text',
                    '.tags-container a::text',
                ]
            }
        }
    }]
