# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class EstadaoArticlesSpider(ZeSpider):

    name = 'g1'
    allowed_domains = ['g1.globo.com']
    parses = [{
        "ze.items.creativework.NewsArticleItem": {
            "parse_method": "parse_news_article_item", 
            "fields": { 
                "name": [ 
                    "[itemprop=headline]::text", 
                    ".content-head__title::text" 
                ], 
                "image": [ 
                    "[itemprop=image]::attr(content)" 
                ], 
                "description": [ 
                    "[itemprop=description]::text", 
                    "[itemprop=alternativeHeadline]::text", 
                    ".content-head__subtitle::text" 
                ], 
                "author": [
                    "[itemprop=author]::text", 
                    "[itemprop=creator]::text"
                ], 
                "datePublished": [
                    "[itemprop=datePublished]::text",
                    "[itemprop=datePublished]::attr(datetime)"
                ], 
                "dateModified": [
                    "[itemprop=dateModified]::text", 
                    "[itemprop=dateModified]::attr(datetime)" 
                ], 
                "articleBody": [
                    "[itemprop=articleBody]",
                    ".mc-body" 
                ], 
                "keywords": [
                    "[itemprop=keywords]::text", 
                    ".entities__list-itemLink::text"
                ]
            }
        }
    }]
