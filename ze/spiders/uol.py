# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class UolSpider(ZeSpider):

    name = 'uol'
    allowed_domains = ['uol.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name": [
                    "[itemprop=name]::text", 
                    ".post-title::text", 
                    "#main-content h1::text", 
                ], 
                "image": [ 
                    "[itemprop=image]::attr(content)" 
                ], 
                "description": [
                    "[itemprop=description]::text", 
                    ".post-sub-title::text"
                ],
                "author": [
                    "[itemprop=author]::text", 
                    ".post-meta span::text", 
                    ".autores::text", 
                ],
                "datePublished": [
                    "[itemprop=datePublished]::text" 
                ],
                "dateModified": [
                    "[itemprop=dateModified]::text" 
                ],
                "articleBody": [
                    "[itemprop=articleBody]",
                    ".entry"
                ], 
                "keywords": [
                    "[itemprop=keywords] a::text", 
                    "[class^=pagina-atual]" 
                ]
            }
        }
    }]
