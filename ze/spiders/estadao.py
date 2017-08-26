# -*- coding: utf-8 -*-
from . import ZeSpider


class EstadaoSpider(ZeSpider):

    name = 'estadao'
    allowed_domains = ['estadao.com.br']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        "[itemprop=name]::text", 
                        ".titulo-principal::text", 
                        ".titulo::text", 
                        ".n--noticia__title::text", 
                        "article h1::text", 
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        'meta[property="og:image"]::attr(content)',
                        "[itemprop=image]::attr(content)",
                        "[property='og:image']::attr(content)"
                    ]
                }
            },
            "description": {
                "selectors": {
                    "css": [
                        "[itemprop=description]::text", 
                        ".linha-fina::text", 
                        ".n--noticia__subtitle::text", 
                        "article p::text", 
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        "[itemprop=author]::text", 
                        ".autor::text", 
                        ".author::text", 
                        ".n--noticia__state span::text",
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::text",
                        ".data::text", 
                        '.n--noticia__state p:nth-child(2)::text'
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        "[itemprop=dateModified]::text"
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        "[itemprop=articleBody]",
                        ".main-news .content",
                        ".conteudo-materia",
                        ".content", 
                        ".main-news .content",
                        ".conteudo-materia",
                        ".entry"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
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
        }
    }]
