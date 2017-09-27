# -*- coding: utf-8 -*-
from . import ZeSpider


class GovernoSantaCatarinaSpider(ZeSpider):

    name = 'govsc'
    allowed_domains = ['sc.gov.br']
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
                        '[itemprop="headline"] a::text'
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
                        '.date b::text'
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        '[itemprop=datePublished]::attr(content)',
                        '.entry-date::text',
                        '[property="article:published_time"]::attr(content)',
                        '[itemprop="datePublished"]::attr(datetime)'
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        '[itemprop=dateModified]::attr(content)',
                        '[property="article:modified_time"]::attr(content)',
                        '[itemprop="dateModified"]::attr(datetime)'

                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        '[itemprop=articleBody]',
                        '.noticia',
                        'article.article-main'
                    ]
                }
            },
            "keywords": {
                "selectors": {
                    "css": [
                        '[itemprop=keywords] a::text',
                        '[rel=tag]::text',
                        '.categories a::text'
                    ]
                }
            }
        }
    }]
