# -*- coding: utf-8 -*-
from . import ZeSpider


class r7tvSpider(ZeSpider):

    name = 'r7tv'
    allowed_domains = ['r7.com']
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
                        ".title::text"
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
                        "[property='og:description']::attr(content)"
                    ]
                }
            },
            "author": {
                "default": "SBT Notícias",
                "selectors": {
                    "css": [
                        "[itemprop=author]::text",
                        "[itemprop=creator] [itemprop=name]::text",
                        ".author_name::text",
                        '.BOX.FG1EA9D2.FS16.BOLD.TEXTUPP::text'
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::text",
                        "[property='article:published_time']::attr(content)",
                        '.published_at::attr(datetime)'
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        "[itemprop=dateModified]::text",
                        "[itemprop=dateModified]::attr(datetime)"
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        "[itemprop=articleBody]",
                        ".content",
                        "#article_content"
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
            },
        }
    }]
