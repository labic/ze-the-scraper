# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class IgSpider(ZeSpider):

    name = 'ig'
    allowed_domains = ['ig.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": { 
                "name": [ 
                    "meta[property='og:title']::attr(content)",
                    "meta[name=title]::attr(content)",
                    "[itemprop=name]::text", 
                    "#noticia-titulo-h1::text" 
                ], 
                "image": [ 
                    'meta[property="og:image"]::attr(content)',
                    "[itemprop=image]::attr(content)", 
                    "[property='og:image']::attr(content)" 
                ], 
                "description": [ 
                    "meta[property='og:description']::attr(content)",
                    "meta[name=description]::attr(content)",
                    "[itemprop=description]::text", 
                    "[property=description]::attr(content)", 
                    "[property='og:description']::attr(content)" 
                ], 
                "author": [
                    "[itemprop=author]::text", 
                    "[itemprop=creator] [itemprop=name]::text",
                    "#authors-box::text",
                    "#authors-box strong::text"
                ], 
                "datePublished": [
                    "[itemprop=datePublished]::text",
                    "[property='article:published_time']::attr(content)"
                ], 
                "dateModified": [
                    "[itemprop=dateModified]::text", 
                    "[itemprop=dateModified]::attr(datetime)" 
                ], 
                "articleBody": [
                    "[itemprop=articleBody]",
                    "#noticia" 
                ], 
                "keywords": [
                    "[itemprop=keywords]::text", 
                    "[name=news_keywords]::attr(content)"
                ]
            }
        }
    }]
