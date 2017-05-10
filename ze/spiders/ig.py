# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class IgSpider(ZeSpider):

    name = 'ig'
    allowed_domains = ['ig.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": { 
                "name": [ 
                    "[itemprop=name]::text", 
                    "#noticia-titulo-h1::text" 
                ], 
                "image": [ 
                    "[itemprop=image]::attr(content)", 
                    "[property='og:image']::attr(content)" 
                ], 
                "description": [ 
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
