# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class EBCSpider(ZeSpider):

    name = 'ebc'
    allowed_domains = ['ebc.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name": [
                    "meta[property='og:title']::attr(content)",
                    "meta[name=title]::attr(content)",
                    '[itemprop=headline]::text',
                    '.title-post::text'
                ],
                "image": [
                    'meta[property="og:image"]::attr(content)',
                    '[itemprop="image"] img::attr(src)',
                    '.node-noticia figure img::attr(src)'
                ],
                "description": [
                    "meta[property='og:description']::attr(content)",
                    "meta[name=description]::attr(content)",
                    '[itemprop=description]::attr(content)',
                    '[itemprop=description]::text'
                ],
                "author": [
                    '[itemprop=author]::text',
                    '[class*=autor]::text',
                    '.node-info span strong::text'
         
                ],
                "datePublished": [
                    '[itemprop=datePublished]::attr(content)',
                    '.date::text'
                ],
                "dateModified": [
                    '[itemprop=dateModified]::attr(content)'
                ],
                "articleBody": [
                    '[itemprop=articleBody]',
                    '[property=articleBody]',
                    '.node-noticia .content'
                ],
                "keywords": [
                    '[itemprop=keywords] a::text',
                    '[rel=tag]::text',
                    '[onclick*=montaURL]::text'
                ]
            }
        }
    }]
