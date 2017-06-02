# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class CorreioBrasilienseSpider(ZeSpider):

    name = 'correiobraziliense'
    allowed_domains = ['correiobraziliense.com.br']
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
                    '.lazy::attr("data-lazy-src")'
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
                    '.autor_casa::text',
                    '.author a::text',
                    '[onclick*=malito] span::text'
                ],
                "datePublished": [
                    '[itemprop=datePublished]::attr(content)',
                    '.entry-date::text'
                ],
                "dateModified": [
                    '[itemprop=dateModified]::attr(content)'
                ],
                "articleBody": [
                    '[itemprop=articleBody]',
                    '.entry-content'
                ],
                "keywords": [
                    '[itemprop=keywords] a::text',
                    '[rel=tag]::text',
                    '[onclick*=montaURL]::text'
                ]
            }
        }
    }]
