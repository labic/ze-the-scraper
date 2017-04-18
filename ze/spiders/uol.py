# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class EstadaoArticlesSpider(ZeSpider):

    name = 'uol'
    allowed_domains = ['uol.com.br']
    parses = [{
        "ze.items.creativework.NewsArticleItem": {
            "parse_method": "parse_news_article_item",
            "fields": {
                "name": [
                    "h1::text"
                ], 
                "image": [ 
                    "[itemprop=image]::attr(content)" 
                ], 
                "description": [
                    ".definicao::text"
                ],
                "author": [
                    ".autores::text"
                ],
                "datePublished": [
                    ".data::text"
                ],
                "dateModified": [
                    ".data::text"
                ],
                "articleBody": [
                    ".conteudo-materia"
                ], 
                "keywords": [
                    "[itemprop=keywords] a::text"  
                ]
            }
        }
    }]
