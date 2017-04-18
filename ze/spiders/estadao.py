# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class EstadaoSpider(ZeSpider):

    name = 'estadao'
    allowed_domains = ['estadao.com.br']
    parses = [{
        "ze.items.creativework.NewsArticleItem": {
            "parse_method": "parse_news_article_item", 
            "fields": { 
                "name": [ 
                    "[itemprop=headline]::text", 
                    ".titulo-principal::text" 
                ], 
                "image": [ 
                    "[itemprop=image]::attr(content)" 
                ], 
                "description": [ 
                    "[itemprop=description]::text", 
                    ".linha-fina::text" 
                ], 
                "author": [
                    "[itemprop=author]::text", 
                    ".autor::text"
                ], 
                "datePublished": [
                    "[itemprop=datePublished]::text",
                    ".data::text"
                ],
                "dateModified": [
                    "[itemprop=dateModified]::text"
                ], 
                "articleBody": [
                    "[itemprop=articleBody]",
                    ".main-news .content",
                    ".conteudo-materia",
                ], 
                "keywords": [
                    "[itemprop=keywords] a::text", 
                    ".tags a::text", 
                    ".tags a span::text" 
                ]
            }
        }
    }]
