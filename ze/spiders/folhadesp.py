# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class FolhaDeSaoPauloSpider(ZeSpider):

    name = 'folhadesp'
    allowed_domains = ['folha.uol.com.br']
    parses = [{
        "ze.items.creativework.NewsArticleItem": {
            "parse_method": "parse_news_article_item", 
            "fields": { 
                "name": [ 
                    "[itemprop=headline]::text", 
                    "[itemprop=alternativeHeadline]::attr(content)", 
                    "article header h1::text" 
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
                    ".author p::text"
                ], 
                "datePublished": [
                    "[itemprop=datePublished]::text",
                    "article time::text"
                ], 
                "dateModified": [
                    "[itemprop=dateModified]::text"
                ], 
                "articleBody": [
                    "[itemprop=articleBody]",
                    ".content" 
                ], 
                "keywords": [
                    "[itemprop=keywords]::text", 
                    "[itemprop=keywords]::attr(content)"
                ]
            }
        }
    }]
