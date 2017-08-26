# -*- coding: utf-8 -*-
from . import ZeSpider


class IstoESpider(ZeSpider):

    name = 'istoe'
    allowed_domains = ['istoe.com.br']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        "[itemprop=name]::text",
                        ".article-title::text"
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        'meta[property="og:image"]::attr(content)',
                        "[itemprop=image]::attr(content)",
                        "[property=og:image]::attr(content)"
                    ]
                }
            },
            "description": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        "[itemprop=description]::text",
                        ".article-subtitle::text"
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        # "[itemprop=author]::text",
                        # ".article-author span strong::text",
                        # '.author:not(figcaption)::text',
                        "[rel=author]::text"
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::text",
                        ".article-date span::text",
                        ".entry-date::text",
                        '.content-section time::attr(datetime)'
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        "[itemprop=dateModified]::text",
                        ".article-date span::text"
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        "[itemprop=articleBody]",
                        '.content-section.content',
                        ".article-content"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        "[itemprop=keywords]::text",
                        ".article-tags a::text"
                    ]
                }
            }
        }
    }]
