# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class TerraSpider(ZeSpider):

    name = 'terra'
    allowed_domains = ['terra.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": { 
                "name": [ 
                    "meta[property='og:title']::attr(content)",
                    "meta[property='twitter:title']::attr(content)",
                    "meta[name=title]::attr(content)",
                    "[itemprop=name]::text", 
                    ".title::text" 
                ], 
                "image": [ 
                    'meta[property="og:image"]::attr(content)',
                    'meta[property="twitter:image"]::attr(content)',
                    "[itemprop=image]::attr(content)"
                ], 
                "description": [ 
                    "meta[name='description']::attr(content)", 
                    "meta[property='twitter:description']::attr(content)",
                    "meta[property='og:description']::attr(content)",
                    "meta[name=description]::attr(content)",
                    "[property=description]::attr(content)", 
                    "[property='og:description']::attr(content)" 
                ], 
                "author": [
                    ".authorName::text",
                    "[itemprop=author]::text", 
                    # "[itemprop=creator] [itemprop=name]::text",
                ], 
                "datePublished": [
                    "[itemprop=datePublished]::attr(content)",
                    "[property='article:published_time']::attr(content)"
                ], 
                "dateModified": [
                    "[itemprop=dateModified]::text", 
                    "[itemprop=dateModified]::attr(datetime)" 
                ], 
                "articleBody": [
                    "[itemprop=articleBody]",
                    ".content", 
                    "#article_content" 
                ], 
                "keywords": [
                    "meta[property='keywords']::attr(content)",
                    "[itemprop=keywords]::text", 
                    "[name=news_keywords]::attr(content)"
                ]
            }
        }
    }]
