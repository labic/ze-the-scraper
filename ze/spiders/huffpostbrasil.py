# -*- coding: utf-8 -*-
from . import ZeSpider


class HuffPostBrasilSpider(ZeSpider):

    name = 'huffpostbrasil'
    allowed_domains = ['huffpostbrasil.com']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": { 
            "name": {
                "selectors": {
                    "css": [ 
                        "meta[property='og:title']::attr(content)",
                        "meta[property='twitter:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        "[itemprop=name]::text", 
                        ".headline__title::text" 
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        'meta[property="og:image"]::attr(content)',
                        'meta[property="twitter:image"]::attr(content)',
                        "[itemprop=image]::attr(content)"
                    ]
                }
            }, 
            "description": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[property='twitter:description']::attr(content)",
                        "meta[name='description']::attr(content)", 
                        "meta[name=description]::attr(content)",
                        "[property=description]::attr(content)"
                    ]
                }
            }, 
            "author": {
                "selectors": {
                    "css": [
                        "[itemprop=author]::text", 
                        "[itemprop=creator] [itemprop=name]::text",
                        ".author-card__details__name::text"
                    ]
                }
            }, 
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::text",
                        ".timestamp__date--published::text"
                    ]
                }
            }, 
            "dateModified": {
                "selectors": {
                    "css": [
                        "[itemprop=dateModified]::text", 
                        ".timestamp__date--modified::text"
                    ]
                }
            }, 
            "articleBody": {
                "selectors": {
                    "css": [
                        '[data-part="contents"]',
                        "[itemprop=articleBody]",
                        ".entry__body", 
                        ".post-contents"
                    ]
                }
            }, 
            "keywords": {
                "selectors": {
                    "css": [
                        "meta[property='keywords']::attr(content)",
                        "[itemprop=keywords]::text"
                    ]
                }
            },
        }
    }]
