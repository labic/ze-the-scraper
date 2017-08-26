# -*- coding: utf-8 -*-
from . import ZeSpider


class UOLSpider(ZeSpider):

    name = 'uol'
    allowed_domains = ['uol.com.br']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        "[itemprop=name]::text", 
                        ".post-title::text", 
                        "#main-content h1::text", 
                        ".conteudo-pagina h1::text"
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        'meta[property="og:image"]::attr(content)',
                        "[itemprop=image]::attr(content)", 
                        "[property='og:image']::attr(content)" 
                    ]
                }
            }, 
            "description": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        "[itemprop=description]::text", 
                        ".post-sub-title::text",
                        ".definicao::text"
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        "[itemprop=author]::text", 
                        ".post-meta span::text", 
                        ".autores::text"
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::text" 
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
                        ".entry", 
                        "#texto-noticia", 
                        ".conteudo-materia" 
                    ]
                }
            }, 
            "keywords": {
                "selectors": {
                    "css": [
                        "[itemprop=keywords] a::text", 
                        "[class^=pagina-atual]" 
                    ]
                }
            }
        }
    }]
