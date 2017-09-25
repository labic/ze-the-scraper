# -*- coding: utf-8 -*-
from . import ZeSpider


class GloboSpider(ZeSpider):

    name = 'globo'
    allowed_domains = [
                        # 'globo.com'
                        ]
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name":{
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
                        "[itemprop=author] [itemprop=name]::attr(content)",
                        "[itemprop=author]::text",
                        "[itemprop=creator]::text",
                        "#credito-materia::text",
                        ".autorDataHora strong::text"

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
                        ".data::text",
                        ".published::text",
                        ".autorDataHora::text"

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
                        # ".conteudo",
                        "#texto",
                        'internas-conteudo-primeiro-parag',
                        # '$div > p.internas-conteudo-primeiro-parag'
                        '.col-xs-12.col-md-8.col-md-width-mod'

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
