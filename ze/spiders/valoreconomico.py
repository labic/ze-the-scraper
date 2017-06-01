# -*- coding: utf-8 -*-
from ze.spiders import ZeSpider

class ValorEconomicoSpider(ZeSpider):

    name = 'valor'
    allowed_domains = ['valor.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name": [
                    '[itemprop=headline]::text',
                    '.materia h1::text',
                    '.title1::text'
                ],
                "image": [
                    '[itemprop="image"] img::attr(src)',
                    '.image img::attr(src)'
                ],
                "description": [
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
