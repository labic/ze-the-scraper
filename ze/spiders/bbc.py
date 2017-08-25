# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class BBCSpider(ZeSpider):

    name = 'bbc'
    allowed_domains = ['bbc.com']
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
                    '.byline__name::text'
         
                ],
                "datePublished": [
                    '[itemprop=datePublished]::attr(content)',
                    '.date::attr(data-seconds)'
                ],
                "dateModified": [
                    '[itemprop=dateModified]::attr(content)'
                ],
                "articleBody": [
                    '[itemprop=articleBody]',
                    '[property=articleBody]',
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
