# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class VejaSpider(ZeSpider):

    name = 'veja'
    allowed_domains = ['veja.abril.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
<<<<<<< be35545610f507141a39dbbea316f378cf9b30e4
            "fields": { 
                "name": [ 
                    "[itemprop=name]::text", 
                    ".article-title::text" 
                ], 
                "image": [ 
                    "[itemprop=image]::attr(content)", 
                    "[property='og:image']::attr(content)" 
                ], 
                "description": [ 
                    "[itemprop=description]::text", 
                    ".article-subtitle::text",  
                ], 
=======
            "fields": {
                "name": [
                    "[itemprop=name]::text",
                    ".article-title::text"
                ],
                "image": [
                    "[itemprop=image]::attr(content)",
                    "[property=og:image]::attr(content)"
                ],
                "description": [
                    "[itemprop=description]::text",
                    ".article-subtitle::text",
                ],
>>>>>>> Modifiquei em, gestaoescola, valor economico
                "author": [
                    "[itemprop=author]::text",
                    ".article-author span strong::text",
                ],
                "datePublished": [
                    "[itemprop=datePublished]::text",
                    ".article-date span::text"
                    ".entry-date::text"
                ],
                "dateModified": [
                    "[itemprop=dateModified]::text",
                    ".article-date span::text"
                ],
                "articleBody": [
                    "[itemprop=articleBody]",
                    ".article-content"
                ],
                "keywords": [
                    "[itemprop=keywords]::text",
                    ".article-tags a::text"
                ]
            }
        }
    }]
