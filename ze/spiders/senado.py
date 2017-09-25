# -*- coding: utf-8 -*-
from . import ZeSpider


class SenadoSpider(ZeSpider):
    name = 'senado'
    allowed_domains = ['senado.leg.br']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        "[itemprop=headline]::text",
                        "#tituloNoticia h2::text"
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        'meta[property="og:image"]::attr(content)',
                        '[itemprop="image"] img::attr(src)',
                        '.imagem img::attr("src")',

                    ]
                }
            },
            "description": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        '[itemprop=description]::attr(content)',
                        '[itemprop=description]::text'
                    ]
                }
            },
            "audio": {
                "item": "ze.items.creativework.AudioObjectItem",
                "fields": {
                    "url": {
                        "selectors": {
                            "css": [
                                '#downloadAudio a ::attr(href)',
                                '.Control--download ::attr(href)'
                            ]
                        }
                    }
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        '[itemprop=author]::text',
                        '[class*=autor]::text',
                        '#materia > p small::text',
                        '.ByLine-autor a::text'
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        '[itemprop=datePublished]::attr(content)',
                        '.datahoraNoticia::text',
                        '#materia span.text-muted::text',
                        '.ByLine-data::text'
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        '[itemprop=dateModified]::attr(content)',
                        '#materia span.text-muted::text',
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        '[itemprop=articleBody]',
                        '[property=articleBody]',
                        '#textoMateria',
                        '#content'
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        '[itemprop=keywords] a::text',
                        '[rel=tag]::text',
                        '[name=keywords]::attr(content)'
                    ]
                }
            },
        }
    }]
