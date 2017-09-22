# -*- coding: utf-8 -*-
from . import ZeSpider


class GovAcreSpider(ZeSpider):

    name = 'govac'
    allowed_domains = ['ac.gov.br']
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
                        'h3.tituloMateria::text',
                        '.page-title::text',
                        #Secretaria de educação
                        'title::text',
                    ]
                }
            },
            "image": {
                "selectors": {
                    "css": [
                        'meta[property="og:image"]::attr(content)',
                        '[itemprop="image"] img::attr(src)',
                        '.conteudoMateria figure img::attr(src)',
                        'article.item-page p img::attr(src)',
                        # 'title::text',

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
                        '.conteudoMateria figure figcaption::text'
                    ]
                }
            },
            "author": {
                "selectors": {
                    "css": [
                        '[itemprop=author]::text',
                        '.autor-post ::text',
                        '.createdby::text   '
                    ]
                }
            },
            "datePublished": {
                "selectors": {
                    "css": [
                        '[itemprop=datePublished]::attr(content)',
                        '.data::text',
                        '.data-post::text',
                        '.create::text'
                    ]
                }
            },
            "dateModified": {
                "selectors": {
                    "css": [
                        '[itemprop=dateModified]::attr(content)',
                        '.node-body p em::text',
                        '.post-date::text',
                        '.data::text'
                    ]
                }
            },
            "articleBody": {
                "selectors": {
                    "css": [
                        '[itemprop=articleBody]',
                        '[class=card-content]',
                        'article.item-page'
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
