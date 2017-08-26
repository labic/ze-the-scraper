# -*- coding: utf-8 -*-
from . import ZeSpider


class ValorEconomicoSpider(ZeSpider):

    name = 'valor'
    allowed_domains = ['valor.com.br']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": { 
            "name": {
                "selectors": {
                    "css": [
                    "meta[property='og:title']::attr(content)",
                    "meta[name=title]::attr(content)",
                    '[itemprop=headline]::text',
                    '.materia h1::text',
                    '.title1::text'
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        'meta[property="og:image"]::attr(content)',
                        '[itemprop="image"] img::attr(src)',
                        '.image img::attr(src)'
                    ]
                }
            },
            "description": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        '[itemprop=description]::attr(content)',
                        '[itemprop=description]::text',
                        '.resumo h2::text'
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        '[itemprop=author]::text',
                        '.autor-nome::text',
                        '.node-author-inner strong::text'
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        '[itemprop=datePublished]::attr(content)',
                        '.data::text',
                        'span.date::text'
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        '[itemprop=dateModified]::attr(content)',
                        '.node-body p em::text'
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        '[itemprop=articleBody]',
                        '.node-body'
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        '[itemprop=keywords] a::text',
                        '[rel=tag]::text',
                        '[onclick*=montaURL]::text',
                        '.tags a::text'
                    ]
                }
            }
        }
    }]