# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class CBNSpider(ZeSpider):

    name = 'cbn'
    allowed_domains = ['cbn.globoradio.globo.com']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": { 
                "name": [ 
                    "meta[property='og:title']::attr(content)",
                    "meta[name=title]::attr(content)",
                    "[itemprop=name]::text", 
                    "#materia_interna h1::text" 
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
                    "[itemprop=alternativeHeadline]::text", 
                    "#materia_interna h2::text" 
                ], 
                "author": [
                    "[itemprop=author]::text", 
                    "[itemprop=creator]::text"
                ], 
                "datePublished": [
                    "[itemprop=datePublished]::attr(datetime)", 
                    "[itemprop=datePublished]::text", 
                    "time[datetime]::text",  
                    "time::attr(datetime)",
                    ".datahora::text" 
                ], 
                "dateModified": [
                    "[itemprop=dateModified]::attr(datetime)" , 
                    "[itemprop=dateModified]::text", 
                    ".updated"
                ], 
                "articleBody": [
                    "[itemprop=articleBody]",
                    "#materia_interna"
                ], 
                "keywords": [
                    "[itemprop=keywords]::text", 
                    "meta[name=keywords]::attr(content)"
                ]
            }
        }
    }]
