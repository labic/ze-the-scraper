# -*- coding: utf-8 -*-
from ze.spiders import ZeSpider

class ValorEconomicoSpider(ZeSpider):

    name = 'valor'
    allowed_domains = ['valor.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name": [
                    "meta[property='og:title']::attr(content)",
                    "meta[name=title]::attr(content)",
                    '[itemprop=headline]::text',
                    '.materia h1::text',
                    '.title1::text'
                ],
                "image": [
                    'meta[property="og:image"]::attr(content)',
                    '[itemprop="image"] img::attr(src)',
                    '.image img::attr(src)'
                ],
                "description": [
                    "meta[property='og:description']::attr(content)",
                    "meta[name=description]::attr(content)",
                    '[itemprop=description]::attr(content)',
                    '[itemprop=description]::text',
                    '.resumo h2::text'
                ],
                "author": [
                    '[itemprop=author]::text',
                    '.autor-nome::text',
                    '.node-author-inner strong::text'
                ],
                "datePublished": [
                    '[itemprop=datePublished]::attr(content)',
                    '.data::text',
                    'span.date::text',
                ],
                "dateModified": [
                    '[itemprop=dateModified]::attr(content)',
                    '.node-body p em::text'
                ],
                "articleBody": [
                    '[itemprop=articleBody]',
                    '.node-body'
                ],
                "keywords": [
                    '[itemprop=keywords] a::text',
                    '[rel=tag]::text',
                    '[onclick*=montaURL]::text',
                    '.tags a::text'
                ]
            }
        }
    }]
    # ,{
    #     "ze.items.thingitagible.ItemList": {
    #         # http://www.valor.com.br/hojenovalor?dia=03&mes=06&ano=2017
    #         "urls": ["http://www.valor.com.br/hojenovalor?dia={DAY}&mes={MONTH}&ano={YEAR}"],
    #         "fields": {
    #             "itemListElement": {
    #                 "selectors": [],
    #                 "type": "ze.items.creativework.NewsArticle",
    #                 "required": True
    #             },
    #             "itemListOrder": {
    #                 "selectors": [],
    #                 "default": "Unordered"
    #             },
    #             "numberOfItems": {
    #                 "selectors": [],
    #                 "required": True
    #             },
    #             "name": {
    #                 "selectors": [],
    #                 "default:": "News Articles - ${name}",
    #                 "required": True
    #             },
    #         },
    #         "options": {
    #             "parse_url": True
    #         }
    #     }
    }
