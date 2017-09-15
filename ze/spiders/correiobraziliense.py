# -*- coding: utf-8 -*-
from . import ZeSpider


class CorreioBrasilienseSpider(ZeSpider):

    name = 'correiobraziliense'
    allowed_domains = ['correiobraziliense.com.br']
    items_refs = [{
        "item": "ze.items.creativework.ArticleItem",
        "fields": {
            "name":  {
                "selectors": {
                    "css": [
                        "meta[property='og:title']::attr(content)",
                        "meta[name=title]::attr(content)",
                        '[itemprop=headline]::text',
                        '.title-post::text',
                        '.news-tit::text'

                    ]
                }
            },
            "image":  {
                "selectors": {
                    "css": [
                        'meta[property="og:image"]::attr(content)',
                        '[itemprop="image"] img::attr(src)',
                        '.lazy::attr("data-lazy-src")'
                    ]
                }
            },
            "description":  {
                "selectors": {
                    "css": [
                        "meta[property='og:description']::attr(content)",
                        "meta[name=description]::attr(content)",
                        '[itemprop=description]::attr(content)',
                        '[itemprop=description]::text'
                    ]
                }
            },
            "author":  {
                "selectors": {
                    "css": [
                        # '[itemprop=author]::text',
                        # '[class*=autor]::text',
                        '.autor_casa::text',
                        '.autor_agencia::text',
                        '.author a::text',
                        '[onclick*=malito] span::text'
                    ]
                }
            },
            "datePublished":  {
                "selectors": {
                    "css": [
                        '[itemprop=datePublished]::attr(content)',
                        '.entry-date::text'
                    ]
                }
            },
            "dateModified":  {
                "selectors": {
                    "css": [
                        '[itemprop=dateModified]::attr(content)'
                    ]
                }
            },
            "articleBody":  {
                "selectors": {
                    "css": [
                        '[itemprop=articleBody]',
                        '.entry-content'
                    ]
                }
            },
            "keywords":  {
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
