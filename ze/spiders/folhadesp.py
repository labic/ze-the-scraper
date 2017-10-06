# -*- coding: utf-8 -*-
from . import ZeSpider


class FolhaDeSaoPauloSpider(ZeSpider):

    name = 'folhadesp'
    allowed_domains = ['folha.uol.com.br']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        ".news header h1::text",
                        "[itemprop=name]::text",
                        "[itemprop='headline']::text",
                        "[itemprop=alternativeHeadline]::attr(content)"
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        'meta[property="og:image"]::attr(content)',
                        "[itemprop=image]::attr(content)",
                        "[property='og:image']::attr(content)"
                    ]
                }
            },
            "description": {
                "selectors": {
                    "css": [
                        ".documentDescription::text",
                        "[itemprop=description]::text",
                        '[property="og:description"]::attr(content)'
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        ".news .author p b",
                        "[itemprop=author] b::text",
                        ".news__byline p strong::text",
                        '.post-autor::text'
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        ".news time::attr(datetime)",
                        "[itemprop=datePublished]::text",
                        '[property="article:published_time"]::attr(content)'
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        "[itemprop=dateModified]::text",
                        '[property="article:modified_time"]::attr(content)'
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        ".news .content",
                        "[itemprop=articleBody]",
                        ".single-post-content"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        "meta[name=keywords]::attr(content)",
                        "[itemprop=keywords]::text",
                        "[itemprop=keywords]::attr(content)"
                    ]
                }
            }
        }
    }]
