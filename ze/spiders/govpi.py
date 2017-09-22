# -*- coding: utf-8 -*-
from . import ZeSpider


class GovernoPiauiSpider(ZeSpider):

    name = 'govpi'
    allowed_domains = ['pi.gov.br']
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
                        '.entry-title::text',
                        '.conteudo_interna h3::text',
                        'h1 a::text'
                    ]
                }
            },
            "image": {
                    # "url": {
                    #     "selectors": {
                    #         "css": [
                    #             "meta[property='og:description']::attr(content)",
                    #             "meta[name=description]::attr(content)",
                    #             'meta[property="og:image"]::attr(content)',
                    #             '[itemprop="image"]::attr(src)',
                    #             '.lazy::attr("data-lazy-src")',
                    #             '.article-description img::attr(src)'                            ]
                    #     },
                    #     "contexts": {
                    #         "format": "http://www.pe.gov.br{}"
                    #     }
                    # }
                    "selectors": {
                        "css": [
                            "meta[property='og:description']::attr(content)",
                            "meta[name=description]::attr(content)",
                            'meta[property="og:image"]::attr(content)',
                            '[itemprop="image"]::attr(src)',
                            '.lazy::attr("data-lazy-src")',
                            '.text_post_section img::attr(src)'                            ]
                    },
            },
            "description": {
                "selectors": {
                    "css": [
                        '[itemprop=description]::attr(content)',
                        '[itemprop=description]::text',
                        '[name="description"]::attr(content)',
                        '.entry-content h2::text',
                        '.linha-fina::text',
                        '.entry-content blockquote p::text',
                        '[property="og:description"]::attr(content)'
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        '[name=author]::attr(content)',
                        '[itemprop=author]::text',
                        '.author a::text',
                        '.texto p:last-child::text'
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
                        '.event_date::text'
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
                        'div.clear',
                        '#content',
                        '.text_post_section'
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
