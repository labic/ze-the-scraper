# -*- coding: utf-8 -*-
from . import ZeSpider


class IGSpider(ZeSpider):

    name = 'ig'
    allowed_domains = ['ig.com.br']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": { 
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        "[itemprop=name]::text", 
                        "#noticia-titulo-h1::text" 
                    ]
                }
            }, 
            "image": {
                "selectors": {
                    "css": [
                        'meta[property="og:image"]::attr(content)',
                        "[itemprop=image]::attr(content)", 
                        "[property='og:image']::attr(content)" 
                    ]
                }
            }, 
            "description": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        "[itemprop=description]::text", 
                        "[property=description]::attr(content)", 
                        "[property='og:description']::attr(content)" 
                    ]
                }
            }, 
            "author": {
                "selectors": {
                    "css": [
                        "[itemprop=author]::text", 
                        "[itemprop=creator] [itemprop=name]::text",
                        "#authors-box::text",
                        "#authors-box strong::text"
                    ]
                }
            }, 
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::text",
                        "[property='article:published_time']::attr(content)"
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
                        "#noticia" 
                    ]
                }
            }, 
            "keywords": {
                "selectors": {
                    "css": [
                        "[itemprop=keywords]::text", 
                        "[name=news_keywords]::attr(content)"
                    ]
                }
            }
        }
    }]
