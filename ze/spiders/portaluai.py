# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class PortalUAISpider(ZeSpider):

    name = 'portaluai'
    allowed_domains = ['uai.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name": [
                    "meta[property='og:title']::attr(content)",
                    "meta[name=title]::attr(content)",
                    '[itemprop=headline]::text',
                    '.title-post::text',
                    '.entry-title::text'
                ],
                "image": [
                    "meta[property='og:description']::attr(content)",
                    "meta[name=description]::attr(content)",
                    'meta[property="og:image"]::attr(content)',
                    '[itemprop="image"]::attr(src)',
                    '.lazy::attr("data-lazy-src")'
                ],
                "description": [
                    '[itemprop=description]::attr(content)',
                    '[itemprop=description]::text',
                    '.entry-content h2::text',
                    '.linha-fina::text',
                    '.entry-content blockquote p::text'
                ],
                "author": [
                    '[itemprop=author]::text',
                    '.author a::text',
                    '[href*="mailto"]::text',
                    '.news-data-pub__author span::text'
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
