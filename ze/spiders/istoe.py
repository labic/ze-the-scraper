# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class VejaSpider(ZeSpider):

    name = 'istoe'
    allowed_domains = ['istoe.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name": [
                    "meta[property='og:title']::attr(content)",
                    "meta[name=title]::attr(content)",
                    "[itemprop=name]::text",
                    ".article-title::text"
                ],
                "image": [
                    'meta[property="og:image"]::attr(content)',
                    "[itemprop=image]::attr(content)",
                    "[property=og:image]::attr(content)"
                ],
                "description": [
                    "meta[property='og:description']::attr(content)",
                    "meta[name=description]::attr(content)",
                    "[itemprop=description]::text",
                    ".article-subtitle::text",
                ],
                "author": [
                    # "[itemprop=author]::text",
                    # ".article-author span strong::text",
                    # '.author:not(figcaption)::text',
                    "[rel=author]::text",

                ],
                "datePublished": [
                    "[itemprop=datePublished]::text",
                    ".article-date span::text",
                    ".entry-date::text",
                    '.content-section time::attr(datetime)'
                ],
                "dateModified": [
                    "[itemprop=dateModified]::text",
                    ".article-date span::text"
                ],
                "articleBody": [
                    "[itemprop=articleBody]",
                    ".article-content"
                ],
                "keywords": [
                    "[itemprop=keywords]::text",
                    ".article-tags a::text"
                ]
            }
        }
    }]
