# -*- coding: utf-8 -*-
from . import ZeSpider


class GovernoParaSpider(ZeSpider):

    name = 'govpa'
    allowed_domains = ['agenciapara.com.br']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name": {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        '[itemprop=headline]::text',
                        '.title-post::text',
                        '.entry-title::text'
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        'meta[property="og:image"]::attr(content)',
                        '[itemprop="image"]::attr(src)',
                        '.lazy::attr("data-lazy-src")'
                    ]
                }
            },
            "description": {
                "selectors": {
                    "css": [
                        '[itemprop=description]::attr(content)',
                        '[itemprop=description]::text',
                        '[name="description"]::attr(content)',
                        '.entry-content h2::text',
                        '.linha-fina::text',
                        '.entry-content blockquote p::text'
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        '[name=author]::attr(content)',
                        '[itemprop=author]::text',
                        '.author a::text',
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        '[itemprop=datePublished]::attr(content)',
                        '.entry-date::text',
                        '.text-date::attr(datetime)',
                        '.data:first-child::text',
                        '.conteudo_interna .col-md-9 .data::text',
                        # "meta[property='og:title']::attr(content)",
                        '.data::text'

                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        '[itemprop=dateModified]::attr(content)'
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        '[itemprop=articleBody]',
                        '.noticia',
                        'div.clear'
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        '[itemprop=keywords] a::text',
                        '[rel=tag]::text',
                        '[name="keywords"]::attr(content)',
                    ]
                }
            }
        }
    }]
