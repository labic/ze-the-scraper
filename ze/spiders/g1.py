# -*- coding: utf-8 -*-
from . import ZeSpider


class G1Spider(ZeSpider):

    name = 'g1'
    allowed_domains = ['g1.globo.com']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": { 
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        "[itemprop=name]::text", 
                        ".content-head__title::text", 
                        ".materia-titulo h1::text", 
                        ".entry-title::text" 
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
                        ".content-head__subtitle::text", 
                        ".materia-titulo h2::text"  
                    ]
                }
            }, 
            "author": {
                "selectors": {
                    "css": [
                        "[itemprop=author] [itemprop=name]::attr(content)",
                        "[itemprop=author]::text", 
                        "[itemprop=creator]::text", 
                        ".anunciante-publieditorial::text",
                        "#credito-materia::text",
                    ]
                }
            }, 
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::attr(datetime)", 
                        "[itemprop=datePublished]::text", 
                        "time[datetime]::text", 
                        "time::attr(datetime)" 
                    ]
                }
            }, 
            "dateModified": {
                "selectors": {
                    "css": [
                        "[itemprop=dateModified]::attr(datetime)" , 
                        "[itemprop=dateModified]::text", 
                        ".updated"
                    ]
                }
            }, 
            "articleBody": {
                "selectors": {
                    "css": [
                        "[itemprop=articleBody]",
                        ".materia-conteudo", 
                        ".entry-content", 
                        ".post-content"
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
