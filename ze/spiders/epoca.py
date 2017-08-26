# -*- coding: utf-8 -*-
from . import ZeSpider


class EpocaSpider(ZeSpider):

    name = 'epoca'
    allowed_domains = ['epoca.globo.com']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": { 
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        "[itemprop=name]::text", 
                        ".content-head__title::text" 
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
                        "[itemprop=alternativeHeadline]::text", 
                        ".content-head__subtitle::text" 
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        "[itemprop=author]::text", 
                        "[itemprop=creator]::text",
                        ".autor::text"
                    ]
                }
            }, 
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::attr(datetime)", 
                        "[itemprop=datePublished]::text", 
                        "meta[name='article:published_time']::attr(content)",
                        "meta[name=dtnoticia]::attr(content)",
                        "#info-edicao-acervo b::text",
                        ".data-materia .data::text",
                        ".published::text"
                    ]
                }
            }, 
            "dateModified": {
                "selectors": {
                    "css": [
                        "[itemprop=dateModified]::attr(datetime)" , 
                        "[itemprop=dateModified]::text", 
                        "meta[name='article:modified_time']::attr(content)",
                        "updated::text" 
                    ]
                }
            }, 
            "articleBody": {
                "selectors": {
                    "css": [
                    "[itemprop=articleBody]",
                    ".mc-body",
                    ".materia-conteudo",
                    ".entry-content",
                    ".conteudo",
                    "#texto"
                    ]
                }
            }, 
            "keywords": {
                "selectors": {
                    "css": [
                        "meta[name=keywords]::attr(content)",
                        "[itemprop=keywords]::text", 
                        ".entities__list-itemLink::text"
                    ]
                }
            }
        }
    }]
