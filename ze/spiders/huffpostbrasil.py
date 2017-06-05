# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class HuffPostBrasilSpider(ZeSpider):

    name = 'huffpostbrasil'
    allowed_domains = ['huffpostbrasil.com']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": { 
                "name": [ 
                    "meta[property='og:title']::attr(content)",
                    "meta[property='twitter:title']::attr(content)",
                    "meta[name=title]::attr(content)",
                    "[itemprop=name]::text", 
                    ".headline__title::text" 
                ], 
                "image": [ 
                    'meta[property="og:image"]::attr(content)',
                    'meta[property="twitter:image"]::attr(content)',
                    "[itemprop=image]::attr(content)"
                ], 
                "description": [ 
                    "meta[property='og:description']::attr(content)",
                    "meta[property='twitter:description']::attr(content)",
                    "meta[name='description']::attr(content)", 
                    "meta[name=description]::attr(content)",
                    "[property=description]::attr(content)"
                ], 
                "author": [
                    "[itemprop=author]::text", 
                    "[itemprop=creator] [itemprop=name]::text",
                    ".author-card__details__name::text"
                ], 
                "datePublished": [
                    "[itemprop=datePublished]::text",
                    ".timestamp__date--published::text"
                ], 
                "dateModified": [
                    "[itemprop=dateModified]::text", 
                    ".timestamp__date--modified::text"
                ], 
                "articleBody": [
                    "[itemprop=articleBody]",
                    ".entry__body", 
                    ".post-contents"
                ], 
                "keywords": [
                    "meta[property='keywords']::attr(content)",
                    "[itemprop=keywords]::text"
                ]
            }
        }
    }]
