# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class CartaCapitalSpider(ZeSpider):

    name = 'cartacapital'
    allowed_domains = ['cartacapital.com.br', 'cartaeducacao.com.br']
    parses = [{
        "ze.items.creativework.NewsArticleItem": {
            "parse_method": "parse_news_article_item", 
            "fields": { 
                "name": [ 
                    "[itemprop=headline]::text", 
                    ".documentFirstHeading::text" 
                ], 
                "image": [ 
                    "[itemprop=image]::attr(content)" 
                ], 
                "description": [ 
                    "[itemprop=description]::text", 
                    ".documentDescription::text" 
                ], 
                "author": [
                    "[itemprop=author]::text", 
                    ".documentAuthor a::text"
                ], 
                "datePublished": [
                    "[itemprop=datePublished]::text",
                    ".documentPublished::text"
                ], 
                "dateModified": [
                    "[itemprop=dateModified]::text"
                ], 
                "articleBody": [
                    "[itemprop=articleBody]",
                    "#content-core",
                    ".td-post-content",
                ], 
                "keywords": [
                    "[itemprop=keywords]::text", 
                    "[property=rnews:keywords] a::text", 
                    "#category .link-category a::text" 
                ]
            }
        }
    }]
