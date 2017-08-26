# -*- coding: utf-8 -*-
from . import ZeSpider


class CorreioPopularSpider(ZeSpider):

    name = 'correiopopular'
    allowed_domains = ['correio.rac.com.br']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        '[itemprop=headline]::text',
                        '.news-title::text'
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        "meta[property='og:image']::attr(content)",
                        '[itemprop="image"] img::attr(src)',
                        '#foto_auto img::attr(src)'
                    ]
                }
            },
            "description": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        '[itemprop=description]::attr(content)',
                        '[itemprop=description]::text',
                        '.resumo h2::text'
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        '[itemprop=author]::text',
                        '.publish-by b::text'
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        '[itemprop=datePublished]::attr(content)',
                        "meta[name='DC.date.created']::attr(content)",
                        '.publish-time::text',#dateModified ta junto
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        '[itemprop=dateModified]::attr(content)',
                        '.publish-time::text',#datePublished ta junto
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        '[itemprop=articleBody]',
                        '.article-container'
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        '[itemprop=keywords] a::text',
                        '.tags-container a::text',
                    ]
                }
            }
        }
    }]
