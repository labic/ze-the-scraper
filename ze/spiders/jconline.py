# -*- coding: utf-8 -*-
from . import ZeSpider


class JCOnlineSpider(ZeSpider):

    name = "jconline"
    allowed_domains = ["jconline.ne10.uol.com.br"]
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        ".titulo-materia::text",
                        ".titulo-noticia a::attr(title)",
                        "[itemprop=headline]::text",
                        "title::text"
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        'meta[property="og:image"]::attr(content)',
                        "[itemprop=image]::attr(src)",
                        "#noticia img.bordaimg::attr(src)",
                        "[class*='wp-image]::attr(src)"
                    ]
                }
            },
            "description": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        "[itemprop=description]::attr(content)",
                        "[itemprop=description]::text",
                        "meta[name=description]::attr(content)",
                        "p.mg_sutia::text"
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        "[itemprop=author]::text",
                        ".author a::text",#não tem autor da matéria no site
                        "[id*=post] header strong::text",#"pra blog"
                        '[property="article:author"]::attr(content)',#para especial
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        "[itemprop=datePublished]::attr(content)",
                        ".data-materia::text",
                        ".data-post div::text",
                        ".data-materia::text",
                        '[property="article:published_time"]::attr(content)',
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        "[itemprop=dateModified]::attr(content)"
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        "[itemprop=articleBody]",
                        "#noticia_corpodanoticia",#pegar o que ta entre <p></p>,
                        "#texto-noticia",#fazer negocio de pegar xhr
                        ".noticia_corpodanoticia",
                        "#conteudo-iss .container .row"
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        "[itemprop=keywords] a::text",
                        "meta[name=keymwords]::attr(content)",
                        "li.keywords a::text",
                        '[property="article:tag"]::attr(content)'
                    ]
                }
            }
        }
    }]
