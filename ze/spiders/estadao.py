# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class EstadaoSpider(ZeSpider):

    name = 'estadao'
    allowed_domains = ['estadao.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name": [
                    "meta[property='og:title']::attr(content)",
                    "meta[name=title]::attr(content)",
                    "[itemprop=name]::text", 
                    ".titulo-principal::text", 
                    ".titulo::text", 
                    ".n--noticia__title::text", 
                    "article h1::text", 
                ],
                "image": [
                    "meta[property='og:description']::attr(content)",
                    "meta[name=description]::attr(content)",
                    'meta[property="og:image"]::attr(content)',
                    "[itemprop=image]::attr(content)",
                    "[property='og:image']::attr(content)"
                ],
                "description": [
                    "[itemprop=description]::text", 
                    ".linha-fina::text", 
                    ".n--noticia__subtitle::text", 
                    "article p::text", 
                ],
                "author": [
                    "[itemprop=author]::text", 
                    ".autor::text", 
                    ".author::text", 
                    ".n--noticia__state span::text",
                ], 
                "datePublished": [
                    "[itemprop=datePublished]::text",
                    ".data::text", 
                    '.n--noticia__state p:nth-child(2)::text'
                ],
                "dateModified": [
                    "[itemprop=dateModified]::text"
                ],
                "articleBody": [
                    "[itemprop=articleBody]",
                    ".main-news .content",
                    ".conteudo-materia",
                    ".content", 
                    ".main-news .content",
                    ".conteudo-materia",
                    ".entry"
                ],
                "keywords": [
                    "[itemprop=keywords] a::text", 
                    ".tags a::text", 
                    ".tags a span::text", 
                    "[itemprop=keywords] a::text", 
                    ".tags a::text", 
                    ".tags a span::text",  
                    "[itemprop=keywords] a::text",
                    ".tags a::text",
                    ".tags a span::text"
                ]
            }
        }
    }]
