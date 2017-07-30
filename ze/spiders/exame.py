# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class GloboSpider(ZeSpider):

    name = 'exame'
    allowed_domains = ['exame.abril.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": { 
                "name": [ 
                    "meta[property='og:title']::attr(content)",
                    "meta[name=title]::attr(content)",
                    "[itemprop=name]::text", 
                    ".content-head__title::text" 
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
                    ".content-head__subtitle::text" 
                ], 
                "author": [
                    "[itemprop=author]::text", 
                    "[itemprop=creator]::text",
                    ".article-author span::text"
                ], 
                "datePublished": [
                    "[itemprop=datePublished]::attr(datetime)", 
                    "[itemprop=datePublished]::text", 
                    "meta[property='bt:pubDate']::attr(content)",
                    # head > meta:nth-child(44)
                ], 
                "dateModified": [
                    "[itemprop=dateModified]::attr(datetime)" , 
                    "[itemprop=dateModified]::text", 
                    "meta[name='article:modified_time']::attr(content)",
                    "updated::text",
                ], 
                "articleBody": [
                    "[itemprop=articleBody]",
                    ".mc-body",
                    ".materia-conteudo",
                    ".entry-content",
                    ".conteudo",
                    ".article-content"
                ], 
                "keywords": [
                    "meta[name=keywords]::attr(content)",
                    "[itemprop=keywords]::text", 
                    ".entities__list-itemLink::text"
                ]
            }
        }
    }]
