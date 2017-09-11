# -*- coding: utf-8 -*-
from . import ZeSpider


class GovernoDestritoFederalSpider(ZeSpider):

    name = 'govdf'
    allowed_domains = ['df.gov.br']
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
                        '.entry-date::text'
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
                        '.noticia'
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        '[itemprop=keywords] a::text',
                        '[rel=tag]::text',
                        '[onclick*=montaURL]::text'
                    ]
                }
            }
        }
    }]
