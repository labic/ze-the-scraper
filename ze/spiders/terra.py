# -*- coding: utf-8 -*-
from . import ZeSpider


class TerraSpider(ZeSpider):

    name = 'terra'
    allowed_domains = ['terra.com.br']
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
                        ".title::text" ,
                        ".tit_noticiaDetail::text",
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
                        "meta[name='description']::attr(content)",
                        "meta[property='twitter:description']::attr(content)",
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        "[property=description]::attr(content)",
                        "[property='og:description']::attr(content)",
                        ".summary::text"
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        ".author [itemprop=name]::attr(content)",
                        ".authorName::text",
                        "[itemprop=author]::text",
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::attr(content)",
                        "[property='article:published_time']::attr(content)",
                        ".dateDetail::text"
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        "[itemprop=dateModified]::text",
                        "[itemprop=dateModified]::attr(datetime)",
                        ".dateDetail::text"

                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        "[itemprop=articleBody]",
                        ".content",
                        "#article_content",
                        ".noticiaDetail2"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        "meta[property='keywords']::attr(content)",
                        "[itemprop=keywords]::text",
                        "[name=news_keywords]::attr(content)"
                    ]
                }
            }
        }
    }]
