# -*- coding: utf-8 -*-

from ze.spiders import ZeSpider

class CorreioBrasilienseSpider(ZeSpider):

    name = 'correiobraziliense'
    allowed_domains = ['correiobraziliense.com.br']
    parses = [{
        "ze.items.creativework.ArticleItem": {
            "fields": {
                "name":[
                    '[itemprop=headline]::text',
                    '.title-post::text'
                ],
                "image":[
                    # '[itemprop="image" img::attr(src)]',
                    '.lazy::attr("data-lazy-src")'
                ],
                "description":[
                    '[itemprop=description]::attr(content)',
                    '[itemprop=description]::text'
                ],
                "author":[
                    '[itemprop=author]::text',
                    '.author a::text',
                    '.autor_casa::text'
                ],
                "datePublished":[
                    '[itemprop=datePublished]::attr(content)',
                    '.entry-date::text'

                ],
                "dateModified":[
                    '[itemprop=dateModified]::attr(content)'
                ],
                "articleBody":[
                    '[itemprop=articleBody]',
                    '.entry-content'

                ],
                "keywords":[
                    '[itemprop=keywords] a::text',
                    '[rel=tag]::text',
                    '[onclick*=montaURL]::text'
                ]
            }
        }
    }]
